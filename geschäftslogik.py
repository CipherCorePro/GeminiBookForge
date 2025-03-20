import google.generativeai as genai
import tiktoken
from functools import lru_cache
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging
import yaml
import importlib
import time
import asyncio
from google.api_core.exceptions import InvalidArgument, PermissionDenied, ResourceExhausted
from plugin_weighting import BaseWeighting

# Logging-Konfiguration
logging.basicConfig(filename='buchgenerator.log', level=logging.INFO)

# Konfiguration laden
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
    extra_stopwords = config.get("stopwords", [])

nltk.download('stopwords')
stopwords_de = set(stopwords.words('german')) | set(extra_stopwords)

class BuchGenerator:
    def __init__(self, modell: genai.GenerativeModel, buch_repository: 'BuchRepository', window_size: int = config["text"]["window_size"], tokenizer_name: str = config["text"]["tokenizer"]):
        self.modell = modell  # ✅ Das Modell wird direkt gespeichert, ohne erneut GenerativeModel zu erstellen!
        self.buch_repository = buch_repository
        self.window_size = window_size
        self.tokenizer = self.create_tokenizer(tokenizer_name)
        self.tfidf_vectorizer = TfidfVectorizer()  # Initialisiere TfidfVectorizer
        self.tfidf_matrix = None  # TF-IDF Matrix für den bestehenden Text

    def create_tokenizer(self, tokenizer_name: str) -> tiktoken.Encoding:
        """Erstellt den Tokenizer basierend auf dem Namen."""
        if tokenizer_name == "tiktoken":
            try:
                return tiktoken.encoding_for_model("gpt-3.5-turbo")  # Oder ein anderes passendes Modell
            except Exception as e:
                logging.error(f"Fehler beim Initialisieren von tiktoken: {e}")
                raise
        else:
            logging.error(f"Ungültiger Tokenizer-Name: {tokenizer_name}")
            raise ValueError(f"Ungültiger Tokenizer-Name: {tokenizer_name}")

    def gewichtung_basierend_auf_position(self, satz_index: int, anzahl_saetze: int) -> float:
        """Weist einem Satz basierend auf seiner Position eine Gewichtung zu."""
        if satz_index < anzahl_saetze * 0.2:  # Die ersten 20% der Sätze
            return 0.8  # Hohe Gewichtung
        elif satz_index > anzahl_saetze * 0.8:  # Die letzten 20% der Sätze
            return 0.8  # Hohe Gewichtung
        else:
            return 0.4  # Niedrige Gewichtung

    def extrahiere_schluesselwoerter(self, text: str) -> list[str]:
        """Extrahiert die wichtigsten Schlüsselwörter aus dem Text."""
        tfidf_vectorizer = TfidfVectorizer(stop_words=stopwords_de)
        tfidf_matrix = tfidf_vectorizer.fit_transform([text])

        feature_names = tfidf_vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]

        # Wähle die 10 wichtigsten Schlüsselwörter
        return [feature_names[i] for i in tfidf_scores.argsort()[-10:][::-1]]

    def generieren(self, prompt: str, gewichtungsstrategie: BaseWeighting, positionsbasierte_gewichtung_faktor: float) -> str:
        """Generiert Text basierend auf dem Prompt und dem bestehenden Buchinhalt (Sliding Window)."""
        try:
            existing_text = ""  # Initialisiere existing_text als leeren String
            # Bestehenden Text laden, wenn die Datei existiert und nicht leer ist
            if self.buch_repository.existiert():
                try:
                    existing_text = self.buch_repository.laden()
                except FileNotFoundError as e:
                    logging.error(f"Fehler beim Laden der Buchdatei: {e}")
                    raise
                except IOError as e:
                    logging.error(f"Fehler beim Lesen der Buchdatei: {e}")
                    raise

            # Sliding Window anwenden (tokenbasiert)
            anzahl_tokens = self.token_zaehlen(existing_text)
            if anzahl_tokens > self.window_size:
                # Text in Sätze aufteilen
                saetze = nltk.sent_tokenize(existing_text)  # Nutze nltk für Satzsegmentierung

                # Schlüsselwörter extrahieren
                schluesselwoerter = self.extrahiere_schluesselwoerter(existing_text)

                # Gewichtungen berechnen (basierend auf der ausgewählten Strategie)
                gewichtete_saetze = []
                for i, satz in enumerate(saetze):
                    gewichtung = gewichtungsstrategie.calculate(satz, existing_text)
                    gewichtete_saetze.append((satz, gewichtung))

                # Gewichtete Sätze sortieren (absteigend)
                gewichtete_saetze.sort(key=lambda x: x[1], reverse=True)

                # Text zusammenstellen, bis die maximale Window-Größe erreicht ist
                kontext = ""
                kontext_token_anzahl = 0
                for satz, gewichtung in gewichtete_saetze:
                    satz_token_anzahl = self.token_zaehlen(satz)
                    if kontext_token_anzahl + satz_token_anzahl <= self.window_size:
                        kontext += satz + " "  # Satz zum Kontext hinzufügen (Leerzeichen als Trennzeichen)
                        kontext_token_anzahl += satz_token_anzahl
                    else:
                        break  # Window-Größe erreicht

            else:
                kontext = existing_text

            # Text generieren
            response = self.modell.generate_content(kontext + prompt)
            generated_text = response.text

            # Text speichern
            self.buch_repository.speichern(generated_text)

            return generated_text

        except Exception as e:
            logging.error(f"Fehler bei der Textgenerierung: {e}")
            raise

    @lru_cache(maxsize=128)
    def token_zaehlen(self, text: str) -> int:
        """Zählt die Token im Text mit tiktoken und nutzt Caching für Effizienz."""
        try:
            return len(self.tokenizer.encode(text))
        except Exception as e:
            logging.error(f"Fehler beim Zählen der Token mit tiktoken: {e}")
            raise RuntimeError(f"Fehler beim Zählen der Token mit tiktoken: {e}")

    @lru_cache(maxsize=128)  # Begrenze die Cache-Größe auf 128 Einträge
    def encode_cached(self, text: str) -> list[int]:
        """Tokenisiert den Text und verwendet einen Cache."""
        return self.tokenizer.encode(text)

    @lru_cache(maxsize=128)  # Begrenze die Cache-Größe auf 128 Einträge
    def decode_cached(self, token_ids: tuple[int, ...]) -> str:
        """Decodiert die Token-IDs und verwendet einen Cache."""
        return self.tokenizer.decode(token_ids)  # Token-IDs müssen hashable sein (tuple)

async def generate_text_ui(prompt: str, window_size: int, tokenizer_name: str, tiktoken_model: str, gewichtungsstrategie: BaseWeighting, dynamische_window_groesse: bool, positionsbasierte_gewichtung_faktor: float, extra_stopwords: str, profile: bool = False):
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
        yield generated_text, generated_text
        # Gib generierten Text und gesamten Buchinhalt zurück

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