import os
import logging

class BuchRepository:
    def __init__(self, datei_pfad: str):
        self.datei_pfad = datei_pfad

    def laden(self) -> str:
        """Liest den Inhalt der Buchdatei."""
        try:
            if os.path.exists(self.datei_pfad):
                with open(self.datei_pfad, "r", encoding="utf-8") as f:
                    return f.read()
            else:
                return ""
        except FileNotFoundError:
            logging.error("Fehler: Buchdatei nicht gefunden.")
            raise
        except IOError as e:
            logging.error(f"Fehler beim Lesen der Buchdatei: {e}")
            raise

    def speichern(self, text: str) -> None:
        """Schreibt Text in die Buchdatei."""
        try:
            with open(self.datei_pfad, "a", encoding="utf-8") as f:
                f.write(text)
        except IOError as e:
            logging.error(f"Fehler beim Schreiben in die Buchdatei: {e}")
            raise

    def leeren(self) -> None:
        """Leert die Buchdatei."""
        try:
            with open(self.datei_pfad, "w", encoding="utf-8") as f:
                f.write("")  # ✅ Datei wirklich leeren
        except IOError as e:
            logging.error(f"Fehler beim Leeren der Buchdatei: {e}")
            raise

    def existiert(self) -> bool:
        """Prüft, ob die Buchdatei existiert."""
        return os.path.exists(self.datei_pfad)

    def get_datei_pfad(self) -> str:
        """Gibt den Dateipfad zurück."""
        return self.datei_pfad