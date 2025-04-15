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
    "Me acuerdo de haber conseguido, en el Parc des Princes, un autógrafo de Louison Bobet"
]

# Logging para compilar el libro
script_name = os.path.basename(__file__)
logging.basicConfig(
    filename="recuerdo.txt",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

def logInsert(chat_model, temperature, question, answer, elapsed):
    log_entry = (
        f"ChatModel: {chat_model} | "
        f"Temperature: {temperature} | "
        f"{question} | "
        f"{answer} | "
        f"Elapsed: {elapsed:.2f}s"
    )
    logging.info(log_entry)

def recuerdo(question):
    print("")
    answer = ""

    ejemplo_random = random.choice(ejemplos)
    prompt = f"{question} Usar la estructura de este ejemplo pero con palabras y referencias actuales: {ejemplo_random}"
    

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

    return answer

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🧠 AI Remember, Roni Bandini, Abril 2025\n")
    counter = 0
    while True:
        recuerdo("Escribir una oración breve que empiece con: Me acuerdo.")
        counter += 1
        print(f"\n---# {counter}")
