## 🤖 KI-Buchgenerator: Eine Schritt-für-Schritt-Anleitung

Diese Anleitung führt Sie durch die Verwendung der interaktiven Gradio-Weboberfläche, um mit Hilfe von Künstlicher Intelligenz (KI) Ihr eigenes Buch zu erstellen.

---

### 🚀 **1. Loslegen**

1.  **Voraussetzungen:**
    *   Stellen Sie sicher, dass Ihr Google API-Schlüssel korrekt in der `config.yaml`-Datei hinterlegt ist.
    *   Starten Sie die Anwendung, indem Sie `ui.py` ausführen.
2.  **Initialisierung:**
    *   Beim Start wird der Inhalt der Datei `book.txt` (falls vorhanden) automatisch in die Weboberfläche geladen.

---

### 📝 **2. Die Benutzeroberfläche im Detail**

| Symbol | Element                       | Beschreibung                                                                                                                                                                                                                                                                                          |
| :----: | :---------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ✍️      | **Prompt (Eingabe)**         | Hier geben Sie Ihre Anweisungen an die KI ein. Das kann ein Satz, eine Frage, eine Beschreibung oder ein beliebiger Text sein, der die Richtung vorgibt.                                                                                                                                              |
| ⚡      | **Generieren**                | Klicken Sie auf diese Schaltfläche, um die KI mit der Texterstellung zu beauftragen.  Ein Fortschrittsbalken (⏳) zeigt den ungefähren Fortschritt an. Der generierte Text wird dem "Buchinhalt" hinzugefügt.                                                                                      |
| 🗑️      | **Buch leeren**              | Löscht den gesamten bisherigen Buchinhalt. **Achtung:** Diese Aktion kann nicht rückgängig gemacht werden.                                                                                                                                                                                         |
| 📖      | **Buchinhalt (Ausgabe)**     | Zeigt den gesamten Text Ihres Buches an. Sie können den Text lesen, aber *nicht* direkt bearbeiten. Änderungen erfolgen über neue Prompts.                                                                                                                                                           |
| ⬇️      | **Buch herunterladen**          | Speichert das gesamte Buch als `book.txt` Datei                                                                                                                                                    |
| ↔️      | **Sliding Window Größe**     | (Schieberegler) Legt fest, wie viele *vorherige* Text-Token die KI berücksichtigt. Größeres Fenster = mehr Kontext, aber auch mehr Wiederholungen. Beginnen Sie mit dem Standardwert (1000) und experimentieren Sie.                                                                          |
| ⚙️      | **Tokenizer**                 | (Auswahlfeld) Bestimmt, wie Text in Token umgewandelt wird. "tiktoken" ist die Standardoption.                                                                                                                                                                                                   |
| 🧠      | **tiktoken Modell**            | (Auswahlfeld) Wählen Sie ein spezifisches `tiktoken`-Modell.  `gemini-2.0-pro-exp` ist voreingestellt. Fortgeschrittene Benutzer können eigene Werte eingeben.                                                                                                                                       |
| ✅      | **Profilierung aktivieren**   | (Kontrollkästchen) *Nur für Entwickler.* Aktiviert detaillierte Protokolle zur Leistungsanalyse.                                                                                                                                                                                                  |
| ⚖️      | **Gewichtungsstrategie**     | (Auswahlfeld) Beeinflusst, wie die KI die Wichtigkeit von Textteilen im "Sliding Window" bewertet.  Optionen: Keine, Positionsbasiert, TF-IDF, Kombiniert (Standard), Schlüsselwort (experimentell).                                                                                                |
| 📏      | **Dyn. Window-Größe**        | (Kontrollkästchen) Passt die Fenstergröße automatisch an die Promptlänge an. Kurzer Prompt = größeres Fenster (mehr Kontext). Empfehlung: Aktiviert lassen.                                                                                                                                        |
| ⬆️      | **Pos.-basierte Gewichtung** | (Schieberegler) *Nur bei "Kombinierter Gewichtung".* Steuert, wie stark die Position (Anfang/Ende) des Textes gewichtet wird.                                                                                                                                                                       |
| 🔠      | **Zusätzl. Stopwörter**     | (Textfeld) Wörter, die die KI bei der TF-IDF-Gewichtung ignorieren soll (zusätzlich zu den Standard-Stopwörtern). Trennen Sie Wörter durch Leerzeichen.                                                                                                                                          |

---

### 📚 **3. Ihr Buch schreiben: Der Prozess**

1.  **Prompt eingeben:** Schreiben Sie Ihre Anweisung in das Feld "Prompt". Seien Sie präzise und kreativ!
2.  **Einstellungen anpassen:**
    *   **Sliding Window:** Beeinflusst den Kontext.
    *   **Gewichtung:** Experimentieren Sie mit verschiedenen Strategien.
3.  **Text generieren:** Klicken Sie auf "Generieren".
4.  **Wiederholen:**  Fügen Sie weitere Prompts hinzu und passen Sie die Einstellungen an, um Ihr Buch Kapitel für Kapitel (oder Satz für Satz) zu formen.
5. **Buch herunterladen:** Klicken Sie auf "Buch herunterladen", um die txt-Datei zu speichern

---

### ✨ **4. Tipps & Tricks**

*   **Experimentieren:** Der Schlüssel zum Erfolg! Probieren Sie verschiedene Prompts und Einstellungen aus.
*   **Kontext:** Die KI "erinnert" sich nur an den Text im "Sliding Window". Erwähnen Sie wichtige Dinge im Prompt, wenn sie weiter zurückliegen.
*   **Unerwartetes?** Die KI ist nicht perfekt. Ändern Sie den Prompt oder die Einstellungen, wenn das Ergebnis nicht passt.
*   **Kreativität:** Nutzen Sie die KI als Ideengeber und erweitern Sie Ihre eigenen Vorstellungen.
*   **Speichern nicht vergessen:** Der Text wird automatisch in der `book.txt`-Datei gespeichert.

---

### 🚨 **5. Fehlerbehebung**

| Fehlermeldung          | Ursache                                                                                             | Lösung                                                                                                                                        |
| :--------------------- | :--------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| Quota überschritten     | Nutzungslimit der Google Gemini API erreicht.                                                        | Warten Sie eine Weile und versuchen Sie es später erneut.                                                                                    |
| Fehlende Berechtigung | API-Schlüssel ungültig oder fehlt.                                                                     | Überprüfen Sie die `config.yaml`-Datei.                                                                                                       |
| Ungültige Eingabe      | Prompt zu lang oder enthält ungültige Zeichen.                                                       | Kürzen Sie den Prompt oder entfernen Sie Sonderzeichen.                                                                                      |
| Sonstige Fehler        | Es kann weitere Fehlermeldungen geben, die spezifisch für die Google Gemini- oder tiktoken-Bibliothek sind. | Lesen sie aufmerksam die Fehlermeldung und passen die Einstellungen an. |

---

### 🏁 **6. Neustart**

*   Um ein *völlig neues* Buch zu beginnen, klicken Sie auf "Buch leeren".
