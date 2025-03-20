import gradio as gr
import os
import google.generativeai as genai
from dotenv import load_dotenv
import google.api_core.exceptions  # Für Google API spezifische Exceptions
from datenzugriff import BuchRepository
from geschäftslogik import BuchGenerator
import cProfile
import pstats
import nltk  # Importiere nltk
from nltk.corpus import stopwords  # 🔹 FEHLENDER IMPORT
from sklearn.feature_extraction.text import TfidfVectorizer
import logging
import yaml
import asyncio

# NEU: Überprüfe und lade die Stopwörter herunter
try:
    stopwords.words('german')
except LookupError:
    logging.info("Downloading stopwords for nltk...")
    nltk.download('stopwords')
# Logging-Konfiguration
logging.basicConfig(filename='buchgenerator.log', level=logging.INFO)

# Konfiguration laden
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Umgebungsvariablen laden
load_dotenv()

# Konfiguration
GOOGLE_API_KEY = config["api"]["key"]
if not GOOGLE_API_KEY:
    logging.error("Google API Key nicht gefunden. Bitte in der .env-Datei hinterlegen.")
    raise ValueError("Google API Key nicht gefunden. Bitte in der .env-Datei hinterlegen.")

genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = config["api"]["model"]
model = genai.GenerativeModel(MODEL_NAME)

BOOK_FILE = config["text"]["buch_datei"]
DEFAULT_PROMPT = "Schreibe den ersten Satz eines spannenden Fantasy-Romans."

# Initialisierung
buch_repository = BuchRepository(BOOK_FILE)
# NEU: Überprüfe und lade das punkt Modell herunter
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logging.info("Downloading punkt model for nltk...")
    nltk.download('punkt')
# NEU: Überprüfe und lade die Stopwörter herunter
try:
    stopwords.words('german')
except LookupError:
    logging.info("Downloading stopwords for nltk...")
    nltk.download('stopwords')
buch_generator = BuchGenerator(model, buch_repository, tokenizer_name=config["text"]["tokenizer"]) # Gemini Modell wird übergeben und tokenizer_name gesetzt

async def generate_text_ui(prompt, window_size, tokenizer_name, tiktoken_model, gewichtungsstrategie, dynamische_window_groesse, positionsbasierte_gewichtung_faktor, extra_stopwords, profile=False):
    """Generiert Text über die BuchGenerator-Klasse und gibt den generierten Text zurück."""
    try:
        # Text generieren
        progress = gr.Textbox(value="⏳ Text wird generiert...", interactive=False)
        yield progress.update(value="⏳ Starte Generierung...")
        for i in range(5):
            yield progress.update(value=f"⏳ Fortschritt: {i * 20}%")
            await asyncio.sleep(0.5)

        # NEU: Window-Größe dynamisch anpassen
        if dynamische_window_groesse and len(prompt) < 100:
            buch_generator.set_window_size(window_size * 2)  # Größere Window-Größe für kurze Prompts
        else:
            buch_generator.set_window_size(window_size)  # Standard Window-Größe für längere Prompts

        generated_text = buch_generator.generieren(prompt, gewichtungsstrategie, positionsbasierte_gewichtung_faktor)

        if profile:
            profiler = cProfile.Profile()
            profiler.enable()

        generated_text = buch_generator.generieren(prompt, gewichtungsstrategie, positionsbasierte_gewichtung_faktor)

        if profile:
            profiler.disable()
            stats = pstats.Stats(profiler)
            stats.sort_stats('cumulative').print_stats(10)

        yield progress.update(value="✅ Fertig!")
        yield generated_text, generated_text  # Gib generierten Text und gesamten Buchinhalt zurück

    except FileNotFoundError as e:
        logging.error(f"Fehler: Buchdatei nicht gefunden: {e}")
        yield f"Fehler: Buchdatei nicht gefunden: {e}", ""
    except IOError as e:
        logging.error(f"Fehler: Quota für die Gemini API überschritten. Bitte später erneut versuchen. Details: {e}")
        yield f"Fehler: Quota für die Gemini API überschritten. Bitte später erneut versuchen. Details: {e}", ""
    except ResourceExhausted as e:
        logging.error(f"Quota überschritten: {e}")
        yield f"🚨 Fehler: Quota überschritten. Versuche es später erneut!", ""
    except PermissionDenied as e:
        logging.error(f"Fehlende Berechtigung: {e}")
        yield f"🚨 Fehler: Fehlende API-Berechtigung!", ""
    except InvalidArgument as e:
        logging.error(f"Ungültige Anfrage: {e}")
        yield f"🚨 Fehler: Ungültige Eingabe!", ""
    except Exception as e:
        logging.error(f"Fehler: Unerwarteter Fehler bei der Generierung: {e}")
        yield f"Fehler: Unerwarteter Fehler bei der Generierung: {e}", ""

def load_book_ui():
    """Lädt den Buchinhalt über die BuchRepository-Klasse."""
    try:
        book_content = buch_repository.laden()
        yield book_content, ""
    except FileNotFoundError as e:
        logging.error(f"Fehler: Buchdatei nicht gefunden: {e}")
        yield f"Fehler: Buchdatei nicht gefunden: {e}", ""
    except IOError as e:
        logging.error(f"Fehler beim Schreiben/Lesen der Buchdatei: {e}")
        yield f"Fehler beim Schreiben/Lesen der Buchdatei: {e}", ""
    except google.api_core.exceptions as e:
        logging.error(f"Fehler: Quota für die Gemini API überschritten. Bitte später erneut versuchen. Details: {e}")
        yield f"Fehler: Quota für die Gemini API überschritten. Bitte später erneut versuchen. Details: {e}", ""
    except Exception as e:
        logging.error(f"Fehler: Unerwarteter Fehler beim Laden des Buches: {e}")
        yield f"Fehler: Unerwarteter Fehler beim Laden des Buches: {e}", ""

def clear_book_ui():
    """Leert die Buchdatei über die BuchRepository-Klasse."""
    try:
        buch_repository.leeren()
        yield ""
    except FileNotFoundError as e:
        logging.error(f"Fehler: Buchdatei nicht gefunden: {e}")
        yield f"Fehler: Buchdatei nicht gefunden: {e}", ""
    except IOError as e:
        logging.error(f"Fehler beim Schreiben/Lesen der Buchdatei: {e}")
        yield f"Fehler beim Schreiben/Lesen der Buchdatei: {e}", ""
    except google.api_core.exceptions as e:
        logging.error(f"Fehler: Quota für die Gemini API überschritten. Bitte später erneut versuchen. Details: {e}")
        yield f"Fehler: Quota für die Gemini API überschritten. Bitte später erneut versuchen. Details: {e}", ""
    except Exception as e:
        logging.error(f"Fehler: Unerwarteter Fehler beim Leeren des Buches: {e}")
        yield f"Fehler: Unerwarteter Fehler beim Leeren des Buches: {e}", ""

def download_book_ui():
    """Gibt den Dateipfad zum Download zurück."""
    yield buch_repository.get_datei_pfad()

# Gradio Interface
with gr.Blocks() as iface:
    prompt_input = gr.Textbox(lines=2, placeholder=DEFAULT_PROMPT, label="Prompt")
    generate_button = gr.Button("Generieren")
    clear_button = gr.Button("Buch leeren")
    book_output = gr.Textbox(lines=20, label="Buchinhalt")

    window_size_slider = gr.Slider(minimum=100, maximum=2000, value=1000, step=100, label="Sliding Window Größe")
    download_button = gr.Button("Buch herunterladen")
    tokenizer_choice = gr.Dropdown(choices=["tiktoken"], value="tiktoken", label="Tokenizer") # Dropdown für Tokenizer Auswahl
    tiktoken_model_choice = gr.Dropdown(choices=["gemini-2.0-pro-exp", "gemini-2.0-pro-exp-02-05"],value="gemini-2.0-pro-exp", label="tiktoken Modell", allow_custom_value=True)
    profile_checkbox = gr.Checkbox(label="Profilierung aktivieren") # Checkbox für Profilierung
    gewichtungsstrategie_choice = gr.Dropdown(choices=["Keine Gewichtung", "Positionsbasierte Gewichtung", "TF-IDF Gewichtung", "Kombinierte Gewichtung", "Schlüsselwort Gewichtung"], value="Kombinierte Gewichtung", label="Gewichtungsstrategie") # Dropdown für Gewichtungsstrategie
    dynamische_window_groesse_checkbox = gr.Checkbox(label="Dynamische Window-Größe aktivieren", value=True) # Checkbox für dynamische Window-Größe
    positionsbasierte_gewichtung_slider = gr.Slider(minimum=0.0, maximum=1.0, value=0.5, step=0.1, label="Gewichtung der Positionsbasierten Gewichtung (nur bei kombinierter Strategie)") # Slider für Gewichtung der positionsbasierten Gewichtung
    extra_stopwords_textbox = gr.Textbox(lines=1, placeholder="z.B. der die das", label="Zusätzliche Stopwörter (getrennt durch Leerzeichen)")

    generate_button.click(fn=generate_text_ui, inputs=[prompt_input, window_size_slider, tokenizer_choice, tiktoken_model_choice, gewichtungsstrategie_choice, dynamische_window_groesse_checkbox, positionsbasierte_gewichtung_slider, extra_stopwords_textbox, profile_checkbox],
                           outputs=[book_output, book_output], queue=True)
    clear_button.click(fn=clear_book_ui, outputs=book_output)
    download_output = gr.File(label="Download Buch")
    download_button.click(fn=download_book_ui, outputs=download_output)

    iface.load(fn=load_book_ui, outputs=[book_output, book_output])

iface.launch()