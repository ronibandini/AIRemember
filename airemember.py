# AI Remember
# Roni Bandini, Abril 2025
# MIT License

import ollama
import time
import logging
import os
import random

# Config global
chatModel = "dolphin-llama3:8b"
temperature = 1
contextLimit = 50000
max_tokens = 500
SYSTEM = "Sos un oscuro escritor experimental argentino."

# Lista de ejemplos
ejemplos = [
    "Me acuerdo de la primera vez que me pagaron por tres libros vendidos, en una boleta rosada. Fue en una librería que no existe, en una unidad monetaria que no existe.",
    "Me acuerdo de que un día mi primo Henri visitó una fábrica de cigarrillos y se trajo de allí un cigarrillo tan largo como cinco unidos.",
    "Me acuerdo de que Reda Caire presentó su espectáculo en el cine de la porte de Saint-Cloud.",
    "Me acuerdo de que mi tío tenía un 11 cv con matrícula 7070 rl2",
    "Me acuerdo del cine Les Agriculteurs, y de los sillones de lujo del Caméra, y de los asientos de dos plazas del Panthéon",
    "Me acuerdo de Lester Young en el Club Saint-Germain; llevaba un traje de seda azul con forro de seda roja",
    "Me acuerdo de Ronconi, de Brambilla y de Jésus Moujica; y de Zaaf, el sempiterno «farolillo rojo»",
    "Me acuerdo de que Art Tatum llamó a uno de sus temas Sweet Lorraine porque había estado en Lorena durante la guerra del 14",
    "Me acuerdo del tac-tac",
    "Me acuerdo de un inglés manco que le ganaba al pingpong a todo el mundo en Château d´Oex.",
    "Me acuerdo de que un amigo de mi primo Henri se pasaba el día entero en bata cuando estaba preparando sus exámenes.",
    "Me acuerdo del Ciudadano del Mundo Garry Davis. Escribía a máquina en la place du Trocadéro",
    "Me acuerdo del pan amarillo que hubo durante un tiempo después de la guerra",
    "Me acuerdo de los primeros flippers, que, curiosamente, no tenían flippers",
    "Me acuerdo de las agujas de acero, y de las agujas de bambú que afilábamos sobre un rascador tras cada disco",
    "Me acuerdo de que en el Monopoly, la avenida de Breteuil es verde, la avenida Henri-Martin roja, y la avenida Mozart, naranja",
    "Me acuerdo de que Junot era el duque de Abrantes",
    "Me acuerdo de haber conseguido, en el Parc des Princes, un autógrafo de Louison Bobet",
	"Me acuerdo de cuando vendía sangre cada tres meses en la Segunda Avenida.",
	"Me acuerdo de haber intentado imaginarme a mi madre y a mi padre follando.",
	"Me acuerdo de pasar la mano por debajo de las mesas de los bares y notar todos los chicles.",
	"Me acuerdo de la silla detrás de la que solía pegar los mocos.",
	"Me acuerdo de fantasear con morir y con lo triste que estaría todo el mundo.",
	"Me acuerdo de que la vida era tan seria entonces como lo es ahora.",
	"Me acuerdo de un niño más pequeño que yo que vivía al final de la calle. A veces me escondía uno de sus juguetes en los calzoncillos y hacía que él lo cogiese.",
	"Me acuerdo de «Los negros tienen la polla enorme».",
	"Me acuerdo de «Los chinos tienen la polla chica».",
	"Me acuerdo de que mi padre se rascaba las pelotas un montón.",
	"Me acuerdo de decir «gracias» en ocasiones que no lo requieren.",
	"Me acuerdo de evitar mirar a los lisiados.",
	"Me acuerdo de que cuando empecé a fumar les escribí una carta a mis padres contándoselo. Nunca mencionaron la carta y seguí fumando.",
	"Me acuerdo de los pedos que huelen a huevo duro podrido.",
	"Me acuerdo de un día muy caluroso de verano en el que se me ocurrió poner cubitos de hielo en el acuario y se me murieron todos los peces.",
	"Me acuerdo del «pasado lila». (Él tiene un…).",
	"Me acuerdo de que en todo autobús siempre hay un soldado.",
	"Me acuerdo de una niña alemana muy guapa que, simplemente, no olía bien.",
	"Me acuerdo de las lavanderías por la noche, con todas las luces encendidas y nadie dentro.",
	"Me acuerdo de que me preguntaba por qué, si Jesús podía curar a los enfermos, no curaba a todos los enfermos.",
	"Me acuerdo de comer túneles y ciudades construidos con sandía.",
	"Me acuerdo del daño que puede hacer el rock & roll. Puede ser tan libre y sensual cuando tú no lo eres…",
	"Me acuerdo de querer dormir en el patio de atrás y de que se riesen de mí diciendo que no iba a aguantar la noche entera y de, al final, dormir fuera y no aguantar la noche entera.",
	"Me acuerdo de haber intentado chupármela una vez, pero no llegó a funcionar.",
	"Me acuerdo de haberme deshecho de todo lo que tenía en dos ocasiones.",
]

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("ollama").setLevel(logging.WARNING)

# Logging para compilar el libro
script_name = os.path.basename(__file__)
logging.basicConfig(
    filename="airemember.txt",
    level=logging.INFO,
    format="%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

def logInsert(answer, counter):
    log_entry = (
        f"{answer} | "
        f"-- {counter}"
    )
    logging.info(log_entry)

def recuerdo(question):
    global counter
    print("")
    answer = ""

    ejemplo_random = random.choice(ejemplos)
    prompt = f"Usando la estructura de este ejemplo: {ejemplo_random} {question} usando palabras, referencias y lugares inventados"
    

    stream = ollama.chat(
        model=chatModel,
        stream=True,
        keep_alive="5m",
        options={
            "temperature": temperature,
            "num_ctx": max_tokens,
        },
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt}
        ]
    )

    for chunk in stream:
        content = chunk["message"]["content"]
        print(content, end="", flush=True)
        answer += content

    counter += 1
    logInsert(answer, counter)
    return answer

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🧠 AI Remember, Roni Bandini, Abril 2025\n")
    counter = 0
    while True:
        recuerdo("Escribir una oración breve que empiece con: Me acuerdo")
        print(f"\n---# {counter}")


