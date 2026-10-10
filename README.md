# Qwen3-TTS: eine eigene Stimme lokal vorbereiten

Dein erster kleiner Sprachversuch: eine erlaubte Referenzaufnahme wählen, einen vollständigen Satz vorbereiten und die tatsächliche WAV-Ausgabe mit einem Hörprotokoll prüfen. Das Lernpaket beschreibt unseren dokumentierten GGUF/CPU-Weg auf Windows. Ein neuer Clean-Install- oder Qwen-Lauf wird hier nicht behauptet.

## Download / Downloads

| Sprache | Komplettes Begleitpaket | Anleitung |
|---|---|---|
| Deutsch | [QWEN-TTS-DE.zip](https://raw.githubusercontent.com/dolmario/qwen-tts-lokal/main/QWEN-TTS-DE.zip) | [DE/START.md](DE/START.md) |
| English | [QWEN-TTS-EN.zip](https://raw.githubusercontent.com/dolmario/qwen-tts-lokal/main/QWEN-TTS-EN.zip) | [EN/START.md](EN/START.md) |

Vollständig in einen neuen Ordner entpacken, dann START.md lesen. `VORBEREITEN-QWEN.ps1` schreibt nur einen Befehl für deine vorhandene EXE, Referenzaufnahme und Textdatei. Es startet nichts, erzeugt keine WAV und sendet keinHTTP. Das Skript und die erzeugten DE/EN-Befehle wurden geparst; Vorbereitung und Schutz vor Überschreiben wurden mit absichtlich nicht ausführbarer EXE und Referenz-Sentineldatei geprüft.

Der später von dir bewusst ausgeführte Befehl verwendet `-hf` und kann fehlende Modellgewichte herunterladen. Die Modell- und Referenzrechte, Ressourcenprüfung und die Entscheidung zur tatsächlichen Ausführung bleiben getrennte Schritte. Runtime, Gewichte und Referenzstimme sind nicht in diesen ZIPs enthalten.

## Was du mitnimmst

- b10621-Prerelease und vorhandene Dateiidentität prüfen: unsere ZIP und52vorhandenen Dateien wurden mit dem offiziellen SHA/Archiv verglichen.
- Qwen3-TTS und Referenzstimme unterscheiden; die Referenz ist kein separates Sprachmodell.
- Das historische CPU-Profil lesen: `-ngl0`, `--no-mmproj-offload`,4Threads, Seed42; `-n1500` begrenzt Audioframes, nicht Wörter.
- Ganze kurze Sätze vergleichen und Zahlen, Wortenden, Pausen und Übergänge tatsächlich hören.

Dieses Repository bleibt die Qwen3-TTS-Anleitung. Die Sprecherstimmen der neuen Filme (MOSS s44 und s77) sind synthetisch erzeugt, keine Aufnahmen privater Personen, und **keine Qwen-Ausgabe**; sie sind nicht Teil dieses Pakets. Andere AMD-/Mac-Neuinstallationen sind hier nicht getestet. [QUELLEN.md](QUELLEN.md) nennt die Originalquellen und den genauen Versionsstand.

## English

Prepare a short reference-based speech test with the documented Windows GGUF/CPU profile. Extract the English kit and read START.md. The preparation script writes a command only; no model is run and no audio is generated. Actual manual execution may download missing weights through `-hf`. Use a permitted reference, check current resources, then listen to your actual result and fill in the blank record. The narrator voices of the new films (MOSS s44 and s77) are synthetic, not private recordings, and not Qwen output. No model weights, runtime or reference voice is included.
