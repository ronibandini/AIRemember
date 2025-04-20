# AI Remember
# Literatura generativa con IA-LLM bajo el formato "I remember" de Joe Brainard
# Roni Bandini, Abril 2025, MIT License 
# https://bandini.medium.com/ai-remember-un-llm-generador-de-me-acuerdo-938dd863f8c0

import ollama
import time
import logging
import os
import random
import sys

# Configuración. Descargar en lo posible modelo uncensored y mantener temp y topP altos
modeloChat = ""  
temperatura = 1
topP = 1
tamanioVentanaContexto = 1024
sistema = "Sos un escritor..." # agregar los detalles del estilo, etc
archivoSustantivos = "sustantivos.csv" # file con palabras seed
archivoEjemplos = "meacuerdo.csv" # file con ejemplos del libro de Brainard o Perec, etc
archivoLog = "airemember.txt" # compilación final
modeloEvaluacion = "" # modelo para evaluar. Mejor si es diferente al modelo de generación
sistemaEvaluacion = "Sos un editor que responde puntuando textos del 0 al 10. Criterio: 2 puntos por ..., 2 puntos por evitar ..."
depurar = 0

# --- Seed ---
listaSustantivos = []
try:
    with open(archivoSustantivos, 'r', encoding="utf-8") as archivo:
        listaSustantivos = [linea.strip() for linea in archivo if linea.strip()]
    if not listaSustantivos:
        print(f"Error: El archivo '{archivoSustantivos}' está vacío o no contiene sustantivos válidos.")
        sys.exit(1)
    print(f"Cargados {len(listaSustantivos)} sustantivos desde '{archivoSustantivos}'.")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{archivoSustantivos}'.")
    sys.exit(1)
except Exception as e:
    print(f"Error inesperado al leer '{archivoSustantivos}': {e}")
    sys.exit(1)

# --- Ejemplos ---
listaEjemplos = []
try:
    with open(archivoEjemplos, 'r', encoding="utf-8") as archivo:
        listaEjemplos = [linea.strip() for linea in archivo if linea.strip()]
    if not listaEjemplos:
        print(f"Error: El archivo '{archivoEjemplos}' está vacío o no contiene ejemplos válidos.")
        sys.exit(1)
    print(f"Cargados {len(listaEjemplos)} ejemplos desde '{archivoEjemplos}'.")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{archivoEjemplos}'.")
    sys.exit(1)
except Exception as e:
    print(f"Error inesperado al leer '{archivoEjemplos}': {e}")
    sys.exit(1)

# Silenciar logs de librerías externas
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("ollama").setLevel(logging.WARNING)

# Logging para compilar el texto
logging.basicConfig(
    filename=archivoLog,
    level=logging.INFO,
    format="%(message)s",
    encoding="utf-8",
    filemode='a'
)
print(f"El libro se produce en '{archivoLog}'.")

# --- Funciones ---
def logInsert(respuesta, contador, sustantivosUsados, puntajeEvaluacion):
    entradaLog = (
        f"{respuesta.strip()} | "
        f"-- {contador} ({', '.join(sustantivosUsados)}) | "
        f"Puntuación: {puntajeEvaluacion}/10"
    )
    logging.info(entradaLog)

def validarFrase(frase):
    return frase.startswith("Me acuerdo") and "Nota:" not in frase

def evaluarTexto(texto):
    promptEvaluacion = (
        f"Evalúa la siguiente frase en una escala del 1 al 10. Retorna solo el número:\n\n"
        f"'{texto}'"
    )
    try:
        response = ollama.chat(
            model=modeloEvaluacion,
            options={
                "temperature": 0.2
            },
            messages=[
                {"role": "system", "content": sistemaEvaluacion},
                {"role": "user", "content": promptEvaluacion}
            ],
            stream=False
        )
        contenidoEvaluacion = response['message']['content'].strip()
        try:
            puntajeEvaluacion = int(contenidoEvaluacion)
            if 1 <= puntajeEvaluacion <= 10:
                return puntajeEvaluacion
            else:
                print(f"Error: La puntuación de evaluación está fuera del rango (1-10): {contenidoEvaluacion}")
                return None
        except ValueError:
            print(f"Error al convertir la puntuación de evaluación a entero: {contenidoEvaluacion}")
            return None
        except Exception as e:
            print(f"Error al evaluar el texto: {e}")
            return None

def recuerdo():
    global contador
    print("")
    respuesta = ""
    sustantivosSeleccionados = []

    try:
        if not listaEjemplos or not listaSustantivos:
            print("Error interno: La lista de ejemplos o sustantivos está vacía.")
            return None, [], None

        ejemploAleatorio = random.choice(listaEjemplos)
        usarDosSustantivos = (contador % 3 == 2) and len(listaSustantivos) >= 2
        numeroSustantivos = 2 if usarDosSustantivos else 1

        if numeroSustantivos == 1:
            sustantivo1 = random.choice(listaSustantivos)
            sustantivosSeleccionados.append(sustantivo1)
            promptSustantivos = f" '{sustantivo1}'"
        else:
            sustantivo1 = random.choice(listaSustantivos)
            posiblesSustantivos = [s for s in listaSustantivos if s != sustantivo1]
            if not posiblesSustantivos:
                sustantivo1 = random.choice(listaSustantivos)
                sustantivosSeleccionados.append(sustantivo1)
                promptSustantivos = f" '{sustantivo1}'"
            else:
                sustantivo2 = random.choice(posiblesSustantivos)
                sustantivosSeleccionados.extend([sustantivo1, sustantivo2])
                promptSustantivos = f"'{sustantivo1}' y '{sustantivo2}'"

        if depurar == 1:
            print(f"Seed: {promptSustantivos} ")
            print(f"Ejemplo: {ejemploAleatorio} ")

        prompt = (
            f"Escribir una oración de 10 a 25 palabras que empiece con: Me acuerdo "
            f"Usar {promptSustantivos} . "
            f"Ejemplo de estilo: {ejemploAleatorio}. "
        )

        stream = ollama.chat(
            model=modeloChat,
            stream=True,
            keep_alive="5m",
            options={
                "temperature": temperatura,
                "num_ctx": tamanioVentanaContexto,
                "top_p": topP
            },
            messages=[
                {"role": "system", "content": sistema},
                {"role": "user", "content": prompt}
            ]
        )

        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                contenido = chunk["message"]["content"]
                print(contenido, end="", flush=True)
                respuesta += contenido

        if not respuesta.strip():
            print("\nAdvertencia: El modelo no generó respuesta.")
            return None, [], None

        contador += 1
        puntajeEvaluacion = evaluarTexto(respuesta)
        print(f"\nEvaluación del editor: {puntajeEvaluacion}/10")
        print("")
        return respuesta, sustantivosSeleccionados, puntajeEvaluacion

    except ImportError:
        print("\nError: La librería 'ollama' no está instalada.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError en la llamada a Ollama: {e}")
        return None, [], None


# --- Main  ---
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🧠 AI Remember, Roni Bandini, Abril 2025\n")

    contador = 0
    try:
        while True:
            respuestaGenerada, sustantivosSeleccionados, puntajeEvaluacion = recuerdo()
            if respuestaGenerada is not None:
                if validarFrase(respuestaGenerada) and puntajeEvaluacion is not None:
                    logInsert(respuestaGenerada, contador, sustantivosSeleccionados, puntajeEvaluacion)
                else:
                    print(f"---! Frase descartada: no empieza con 'Me acuerdo', contiene 'Nota:' o error en la evaluación.")
            else:
                print("\n---! Error en la generación, intentando de nuevo...")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nDeteniendo...")
        print(f"Total de recuerdos generados y guardados en '{archivoLog}': {contador}")
        sys.exit(0)