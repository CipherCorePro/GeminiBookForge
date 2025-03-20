# 📖 KI-Buchgenerator: Dein Werkzeug zum Schreiben von Büchern

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://example.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)

Willkommen beim KI-Buchgenerator! Dieses Tool nutzt die Leistungsfähigkeit von Googles Gemini-KI, um dich beim Schreiben deines eigenen Buches zu unterstützen. Egal, ob du Inspiration für den Anfang suchst oder Unterstützung beim Weiterschreiben benötigst – der KI-Buchgenerator steht dir zur Seite.

## ✨ Features

*   **🤖 Intelligente Textgenerierung:** Nutzt die fortschrittliche Gemini-KI, um kohärente und kreative Textpassagen zu generieren.
*   **🪟 Sliding Window:** Behält den Kontext deines Buches im Auge, um stilistische Konsistenz zu gewährleisten.  Die Größe des Sliding Windows ist anpassbar.
*   **⚖️ Gewichtungsstrategien:** Unterschiedliche Strategien (TF-IDF, positionsbasiert, kombiniert) zur Beeinflussung der Textgenerierung, um relevante Sätze aus dem Kontext stärker zu berücksichtigen.
*   **⚙️ Anpassbare Parameter:** Konfiguriere die Textgenerierung durch Einstellungen wie Tokenizer, Sliding-Window-Größe und zusätzliche Stoppwörter.
*   **⏩ Dynamische Window-Anpassung:** Option zur automatischen Vergrößerung des Sliding Windows bei kurzen Prompts.
*   **📝 Einfache Bedienung:** Intuitive Benutzeroberfläche mit Gradio, die es dir ermöglicht, einfach zu generieren, zu laden, zu leeren und dein Buch herunterzuladen.
*   **📚 Buchverwaltung:** Lade, speichere und leere dein Buch direkt über die Benutzeroberfläche.
*  **📊 Profilierung** Option zum einschalten der Profilerstellung.

## 🚀 Installation

1.  **Voraussetzungen:**
    *   Python 3.8 oder höher
    *   Ein Google Cloud-Konto mit aktiviertem Gemini API-Schlüssel.

2.  **Abhängigkeiten installieren:**

    ```bash
    pip install -r requirements.txt
    ```
    (Erstelle eine `requirements.txt` mit den benötigten Paketen: `gradio`, `google-generativeai`, `python-dotenv`, `nltk`, `scikit-learn`, `tiktoken`, `PyYAML`)

3.  **API-Schlüssel konfigurieren:**
    *   Erstelle eine `.env`-Datei im Hauptverzeichnis.
    *   Füge deinen Google API-Schlüssel hinzu:

        ```
        GOOGLE_API_KEY=dein_api_schlüssel
        ```
4. NLTK Resourcen herunterladen.

    ```bash
        python -m nltk.downloader punkt
        python -m nltk.downloader stopwords
    ```

## 🎬 Verwendung

1.  **Starte die Benutzeroberfläche:**

    ```bash
    python ui.py
    ```
    oder führe direkt die `main.py` aus, für eine einfache Konsolenanwendung.

2.  **Verwende die Oberfläche:**
    *   **Prompt:** Gib einen Text ein, um die Generierung fortzusetzen.
    *   **Generieren:** Klicke, um neuen Text basierend auf deinem Prompt und dem bestehenden Buchinhalt zu erzeugen.
    *   **Buchinhalt:** Zeigt den aktuellen Inhalt deines Buches an.
    *   **Buch leeren:** Löscht den gesamten Buchinhalt.
    *   **Buch herunterladen:** Speichert dein Buch als Textdatei.
    *   **Sliding Window Größe:** Passe die Größe des Kontextfensters an.
    *   **Tokenizer:** Wähle den Tokenizer aus (derzeit nur `tiktoken`).
    *   **tiktoken Modell:** Wähle das zu verwendende Modell aus.
    *   **Gewichtungsstrategie:** Bestimme, wie Sätze im Kontext gewichtet werden (Keine, Positionsbasiert, TF-IDF, Kombiniert, Schlüsselwort).
    *   **Dynamische Window-Größe:** Aktiviere/deaktiviere die automatische Anpassung der Window-Größe.
    *   **Gewichtung (positionsbasiert):** Steuere den Einfluss der positionsbasierten Gewichtung (nur bei kombinierter Strategie relevant).
    *   **Zusätzliche Stoppwörter:** Füge eigene Stoppwörter hinzu (durch Leerzeichen getrennt).

## 🛠️ Konfiguration (config.yaml)

Die `config.yaml`-Datei ermöglicht eine detaillierte Anpassung des Buchgenerators:

```yaml
api:
  key: "DEIN_API_SCHLÜSSEL"  # Ersetze dies durch deinen tatsächlichen Schlüssel
  model: "gemini-2.0-pro-exp-02-05"

text:
  window_size: 1000
  tokenizer: "tiktoken"
  buch_datei: "book.txt"
  gewichtungsstrategie: "Kombinierte"

stopwords:
  - "der"
  - "die"
  - "das"
  - "und"
```
* **`api`**:
    *   `key`: Dein Google API-Schlüssel.
    *   `model`: Das zu verwendende Gemini-Modell.
* **`text`**:
    *   `window_size`: Die Größe des Sliding Windows (in Token).
    *   `tokenizer`:  Der zu verwendende Tokenizer (`tiktoken`).
    *   `buch_datei`: Der Name der Datei, in der dein Buch gespeichert wird.
    *  `gewichtungsstrategie`:  Standard-Gewichtungsstrategie.
*   **`stopwords`**: Eine Liste zusätzlicher Stoppwörter.

## ❓ FAQ

*   **F: Wie funktioniert das Sliding Window?**
    **A:** Das Sliding Window behält die letzten *n* Token (festgelegt durch `window_size`) deines Buches im Auge.  Dieser Kontext wird verwendet, um sicherzustellen, dass der neu generierte Text zum bisherigen Stil und Inhalt passt.  Bei großen Textmengen werden die Sätze im Fenster nach der gewählten Gewichtungsstrategie priorisiert, um die relevantesten Teile des Textes für die Generierung zu verwenden.

*   **F: Was sind Gewichtungsstrategien?**
    **A:** Gewichtungsstrategien beeinflussen, wie der KI-Buchgenerator den vorhandenen Text berücksichtigt.
    *   **Keine Gewichtung:** Alle Sätze werden gleich behandelt.
    *   **Positionsbasiert:**  Sätze am Anfang und Ende des aktuellen Textes erhalten eine höhere Gewichtung.
    *   **TF-IDF:**  Sätze mit Wörtern, die im Verhältnis zum gesamten Text häufig, aber im aktuellen Kontext seltener vorkommen, werden höher gewichtet.
    *   **Kombiniert:** Eine Kombination aus Positionsbasiert, und TF-IDF (oder anderen Strategien – erweiterbar).
     *   **Schlüsselwort:** Sätze mit Schlüsselwörtern werden höher gewichtet.

*   **F: Kann ich die Gewichtungsstrategien anpassen?**
    **A:** Ja, du kannst eigene Gewichtungsstrategien implementieren, indem du die `plugin_weighting.py` erweiterst. Erstelle eine neue Klasse, die von `BaseWeighting` erbt, und implementiere die `calculate`-Methode.

* **F: Was ist, wenn die API-Anfragen das Limit überschreiten (Rate Limit)?**
    **A:** Die Anwendung behandelt Fehler aufgrund von Ratenbegrenzungen (Rate Limits). Du erhältst eine entsprechende Fehlermeldung. Warte eine Weile und versuche es dann erneut. Stelle sicher, dass dein Google Cloud-Konto die nötigen Kontingente hat.

*   **F: Wie kann ich eigene Stoppwörter hinzufügen?**
    **A:** Du kannst zusätzliche Stoppwörter in der `config.yaml`-Datei unter `stopwords` hinzufügen oder direkt in der Benutzeroberfläche.

*  **F: Werden meine Daten gespeichert?**
   **A:** Dein Buchinhalt wird lokal in der von dir angegebenen Textdatei (`book.txt` standardmäßig) gespeichert. Es werden keine Daten an externe Server gesendet, außer den für die Google Gemini API erforderlichen Anfragen.

## 📚 Glossar

*   **Token:** Die kleinste Einheit, mit der das Sprachmodell arbeitet (in der Regel Wörter oder Wortteile).
*   **Tokenizer:** Ein Werkzeug, das Text in Token zerlegt.
*   **Sliding Window:** Ein "Fenster", das sich über den Text bewegt und den Kontext für die Textgenerierung bereitstellt.
*   **TF-IDF:** Term Frequency-Inverse Document Frequency. Eine Metrik, die die Wichtigkeit eines Wortes in einem Dokument im Verhältnis zu einer Sammlung von Dokumenten (hier: dem gesamten Buch) misst.
*   **Stoppwörter:** Häufige Wörter (z. B. "der", "die", "das"), die oft aus Texten entfernt werden, um die Analyse zu verbessern.
*   **Prompt:** Der Eingabetext, den du dem KI-Buchgenerator gibst, um die Textgenerierung zu starten oder zu steuern.
*  **Rate Limit** Eine Begrenzung der Anzahl der API-Anfragen, die du in einem bestimmten Zeitraum senden kannst.
* **Profiling:** Profiling ist der Prozess der Analyse des Codes, um Engpässe und Ineffizienzen zu identifizieren.

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert – siehe die [LICENSE](LICENSE)-Datei für Details. (Erstelle eine LICENSE-Datei mit dem MIT-Lizenztext).

## 🤝 Mitwirken

Beiträge sind willkommen! Wenn du Fehler findest oder Verbesserungen vorschlagen möchtest, erstelle bitte ein Issue oder einen Pull Request.

## 📧 Kontakt

Bei Fragen oder Anmerkungen, wende dich bitte an support@ciphercore.de.

