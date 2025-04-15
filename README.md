![4e756570-dc34-438c-a387-8f95f1fa5bf9](https://github.com/user-attachments/assets/0b444e5d-7650-47ca-bea9-365cd39c5b98)

# AI Remember
Software de IA generativa que escribe libros de formato I remember (George Perec y Joe Brainard) usando LLM

“Todos esos recuerdos se perderán como lágrimas en la lluvia” 
Roy Batty, Blade Runner

En 2011 participé del ciclo "Celebración de Perec" en el CCEBA con una performance sobre el libro de Esteban Feune de Colombí No Recuerdo, inspirado en Je me souviens de Georges Perec, inspirado a su vez en I Remember de Joe Brainard y varias veces desde entonces quise desarrollar un software para automatizar una escritura similar.

Un poco de insomnio y la casualidad de tener la Thinkpad cargada con modelos y librerías de IA fueron el disparador para este divertimento llamado AI Remember donde un modelo LLM va revelando sus recuerdos en base a una ecualización de instrucciones de sistema, prompt, contexto, temperatura y tokens. 

Serán textos inventados, pero aun así capaces de sugerir un recuerdo colectivo, probable y cautivante.

![Ejemplo2](https://github.com/user-attachments/assets/2a6a2192-5b2c-4682-8976-8763a23fb34f)


Para instalar el software es necesario:

1. Instalar Ollama https://ollama.com/download y Python https://www.python.org/downloads/
2. Descargar un modelo uncensored como Dolphin con ollama pull dolphin-llama3:8b
3. Descargar el script y ejecutarlo con python  llmrecuerda.py
