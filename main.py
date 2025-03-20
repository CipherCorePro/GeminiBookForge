import importlib
from geschäftslogik import BuchGenerator
from datenzugriff import BuchRepository
import yaml
import google.generativeai as genai

# Konfiguration laden
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Google API Key konfigurieren
GOOGLE_API_KEY = config["api"]["key"]
genai.configure(api_key=GOOGLE_API_KEY)

# Modell initialisieren
MODELL_NAME = config["api"]["model"]
modell = genai.GenerativeModel(MODELL_NAME)


# BuchRepository und BuchGenerator initialisieren
buch_repository = BuchRepository(config["text"]["buch_datei"])
buch_generator = BuchGenerator(MODELL_NAME, buch_repository, tokenizer_name=config["text"]["tokenizer"])

# Gewichtungsstrategie dynamisch laden
gewichtungsstrategie = config["text"]["gewichtungsstrategie"]
plugin = importlib.import_module("plugin_weighting")
weighting = getattr(plugin, f"{gewichtungsstrategie}Weighting")()

# Beispielaufruf
prompt = "Schreibe den ersten Satz eines spannenden Fantasy-Romans."
generated_text = buch_generator.generieren(prompt, weighting, positionsbasierte_gewichtung_faktor=0.5)
print(generated_text)