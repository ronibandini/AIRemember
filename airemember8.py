# AI Remember
# Literatura generativa con IA LLM bajo el formato "I remember" de Joe Brainard
# Roni Bandini, Abril 2025, MIT License
# https://www.instagram.com/ronibandini/ 
# https://x.com/RoniBandini

import ollama
import time
import logging
import os
import random
import sys

# Settings
chatModel = "dolphin-llama3:8b" # modelo uncensored
temperature = 1
topp=0.99
context_window_size = 1024
SYSTEM = "Sos un escritor de realismo sucio cyberpunk oulipo"
NOUN_FILE = "sustantivos.csv"
EXAMPLE_FILE = "meacuerdo.csv"
LOG_FILE = "airemember.txt"
EVALUATION_MODEL = "gemma3:4b-it-q4_K_M"
EVALUATION_SYSTEM = "Sos un editor que responde puntuando del 0 al 10. Criterio: 2 puntos por estilo, 2 puntos por usar menos de 20 palabras, 2 puntos por oraciones integramente en tiempo pasado, 2 puntos por evitar reflexiones, explicaciones de más y moralejas"
debug=0

# --- Sustantivos ---
sustantivos = []
try:
    with open(NOUN_FILE, 'r', encoding="utf-8") as f:
        sustantivos = [line.strip() for line in f if line.strip()]
    if not sustantivos:
        print(f"Error: El archivo '{NOUN_FILE}' está vacío o no contiene sustantivos válidos.")
        sys.exit(1)
    print(f"Cargados {len(sustantivos)} sustantivos desde '{NOUN_FILE}'.")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{NOUN_FILE}'.")
    sys.exit(1)
except Exception as e:
    print(f"Error inesperado al leer '{NOUN_FILE}': {e}")
    sys.exit(1)

# --- Ejemplos ---
ejemplos = []
try:
    with open(EXAMPLE_FILE, 'r', encoding="utf-8") as f:
        ejemplos = [line.strip() for line in f if line.strip()]
    if not ejemplos:
        print(f"Error: El archivo '{EXAMPLE_FILE}' está vacío o no contiene ejemplos válidos.")
        sys.exit(1)
    print(f"Cargados {len(ejemplos)} ejemplos desde '{EXAMPLE_FILE}'.")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{EXAMPLE_FILE}'.")
    sys.exit(1)
except Exception as e:
    print(f"Error inesperado al leer '{EXAMPLE_FILE}': {e}")
    sys.exit(1)

# Silenciar logs de librerías externas
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("ollama").setLevel(logging.WARNING)

# Logging para compilar el texto
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(message)s",
    encoding="utf-8",
    filemode='a'
)
print(f"El libro se produce en '{LOG_FILE}'.")

# --- Funciones ---
def logInsert(answer, counter, nouns_used, evaluation_score):
    log_entry = (
        f"{answer.strip()} | "
        f"-- {counter} ({', '.join(nouns_used)}) | "
        f"Puntuación: {evaluation_score}/10"
    )
    logging.info(log_entry)

def validar_frase(frase):
    return frase.startswith("Me acuerdo") and "Nota:" not in frase

def evaluar_texto(texto):
    prompt_evaluacion = (
        f"Evalúa la siguiente frase en una escala del 1 al 10. Retorna solo el número:\n\n"
        f"'{texto}'"
    )
    try:
        response = ollama.chat(
            model=EVALUATION_MODEL,
           options={
                "temperature": 0.2
            },
            messages=[
                {"role": "system", "content": EVALUATION_SYSTEM},
                {"role": "user", "content": prompt_evaluacion}
            ],
            stream=False
        )
        eval_content = response['message']['content'].strip()
        try:
            evaluation_score = int(eval_content)
            if 1 <= evaluation_score <= 10:
                return evaluation_score
            else:
                print(f"Error: La puntuación de evaluación está fuera del rango (1-10): {eval_content}")
                return None
        except ValueError:
            print(f"Error al convertir la puntuación de evaluación a entero: {eval_content}")
            return None
    except Exception as e:
        print(f"Error al evaluar el texto: {e}")
        return None

def recuerdo():
    global counter
    print("")
    answer = ""
    nouns_selected = []

    try:
        if not ejemplos or not sustantivos:
            print("Error interno: La lista de ejemplos o sustantivos está vacía.")
            return None, [], None

        ejemplo_random = random.choice(ejemplos)
        use_two_nouns = (counter % 3 == 2) and len(sustantivos) >= 2
        num_nouns = 2 if use_two_nouns else 1

        if num_nouns == 1:
            noun1 = random.choice(sustantivos)
            nouns_selected.append(noun1)
            prompt_nouns = f" '{noun1}'"
        else:
            noun1 = random.choice(sustantivos)
            possible_nouns = [s for s in sustantivos if s != noun1]
            if not possible_nouns:
                noun1 = random.choice(sustantivos)
                nouns_selected.append(noun1)
                prompt_nouns = f" '{noun1}'"
            else:
                noun2 = random.choice(possible_nouns)
                nouns_selected.extend([noun1, noun2])
                prompt_nouns = f"'{noun1}' y '{noun2}'"

        if debug==1:
            print(f"Seed: {prompt_nouns} ")
            print(f"Ejemplo: {ejemplo_random} ")

        prompt = (
            f"Escribir una oración de 10 a 25 palabras que empiece con: Me acuerdo. "
            f"Usar {prompt_nouns} y referencias tecnológicas. "
            f"Ejemplo de estilo: {ejemplo_random}. "
        )

        stream = ollama.chat(
            model=chatModel,
            stream=True,
            keep_alive="5m",
            options={
                "temperature": temperature,
                "num_ctx": context_window_size,
                # "top_p": topp
            },
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": prompt}
            ]
        )

        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                content = chunk["message"]["content"]
                print(content, end="", flush=True)
                answer += content

        if not answer.strip():
            print("\nAdvertencia: El modelo no generó respuesta.")
            return None, [], None

        counter += 1
        evaluation_score = evaluar_texto(answer)
        print(f"\nEvaluación del editor: {evaluation_score}/10")  
        print("")      
        return answer, nouns_selected, evaluation_score

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

    counter = 0
    try:
        while True:
            generated_answer, nouns_selected, evaluation_score = recuerdo()
            if generated_answer is not None:
                if validar_frase(generated_answer) and evaluation_score is not None:
                    logInsert(generated_answer, counter, nouns_selected, evaluation_score)
                else:
                    print(f"---! Frase descartada: no empieza con 'Me acuerdo', contiene 'Nota:' o error en la evaluación.")
            else:
                print("\n---! Error en la generación, intentando de nuevo...")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nDeteniendo...")
        print(f"Total de recuerdos generados y guardados en '{LOG_FILE}': {counter}")
        sys.exit(0)