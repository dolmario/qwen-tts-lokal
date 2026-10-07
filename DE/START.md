# Qwen3-TTS: deine erste eigene kurze Sprachprobe

## Was du hier lernst

Eine eigene erlaubte Referenzaufnahme, ein kurzer Text und ein passender llama-tts-Build ergeben einen prüfbaren Sprachversuch. Unser neuer Erklärfilm verwendet die separat bestätigte MOSS-s44-Sprecherin. Eine Qwen-Ausgabe entsteht erst bei deinem eigenen Versuch; die Erzählstimme des Tutorials wird nicht als neu erzeugte Qwen-Probe ausgegeben.

1. ZIP vollständig in einen neuen Begleitordner entpacken. Lies BUILD-SOURCE.json und PROFILE.json. Dies ist der dokumentierte alte GGUF/CPU-Weg, kein frischer Clean-Install-Test.
2. Die Runtime stammt aus dem offiziellen b10621-Prerelease, Commit c1d0e7a004015f23bc0233470b747b596f29b264. Für diesen Windows-Archivweg ist das Vulkan-x64-Asset in BUILD-SOURCE.json genannt. Unser Sprachprofil verwendet dennoch CPU-Auslagerungseinstellungen. Ein anderes Paket ist gesondert zu prüfen.
3. Eine selbst bezogene ZIP mit Get-FileHash -Algorithm SHA256 prüfen. Erwartet2672d85bf87c8280d94dee01eb6a86280046878f70a07d786a93637fa9081163. Vollständig entpacken; EXE und Bibliotheken zusammenlassen. Unsere bereits vorhandene ZIP/52Dateien wurden damit verglichen, nichts neu heruntergeladen.
4. Im eigenen Runtime-Ordner .\llama-tts.exe --version und --help lesen. Die Optionen --tts-lang und --tts-speaker-file müssen unterstützt sein. Der Original-Python-Weg von Qwen ist eine andere Implementierung.
5. Nutze eine WAV-Referenz, deren Verwendung du erlauben darfst: eine eigene Aufnahme oder rechtmäßig nutzbare synthetische Stimme. Die alte Greta-Datei, fremde Audioaufnahmen und unsere Klonreferenz sind nicht im Paket enthalten. Die Modelllizenz ersetzt keine Rechte an fremden Stimmen.
6. Kopiere PROBE-DE.txt und ändere zunächst nur den kurzen Text. Schreibe gesprochene Zahlen verständlich aus. Lasse ganze Sätze zusammen. Behalte für einen Vergleich Referenz, Build und Einstellungen konstant.
7. Unser archiviertes Profil verwendet Qwen3-TTS-12Hz-1.7B-Base-GGUF:Q8_0, -ngl0, --no-mmproj-offload,4Threads,-n1500 und Seed42. -n begrenzt Audioframes, nicht deutsche Wörter. Ein Seed garantiert keine sauberen Wortenden.
8. Der unten vorbereitete Befehl verwendet -hf. Fehlen die benötigten Gewichte im Cache, kann seine spätere manuelle Ausführung Dateien herunterladen. Prüfe Quelle, Modellbedingungen, Speicher und Netzwerkentscheidung vorher. Die Vorbereitung selbst führt keinHTTP und keinen Download aus.
9. Beispiel im Begleitordner; alle Pfade durch deine tatsächlichen Pfade ersetzen:

```powershell
.\VORBEREITEN-QWEN.ps1 -Installation "C:\dein\llama-runtime" -Reference "C:\dein\meine-stimme.wav" -Language de -TextFile ".\PROBE-DE.txt" -OutputDirectory "C:\dein\Qwen-Probe-1"
```

10. STARTBEFEHL.txt im neuen Ausgabeordner zuerst lesen. VORBEREITUNG.json zeigt prepared_only und die Hashes deiner vorhandenen EXE/Referenz. Noch keine WAV entstanden. Das Vorbereitungswerkzeug darf nur bei einem neuen Ausgabeordner weiterlaufen.
11. Vor einem eigenen Qwen-Lauf aktuelle freie Ressourcen und fremde Aufträge prüfen. Auf unserem geteilten64GB-System nicht neben Chat-/Bild-/TTS-Inferenz starten. Keine fremden Prozesse stoppen. Für die erste Probe nur einen Job verwenden; zwei historische Sprachjobs sind keine allgemeine Empfehlung.
12. Führe erst nach deiner eigenen Prüfung den Befehl bewusst aus. Terminal offenlassen, Fehlertext und echte Dauer sichern. probe.wav ist der angegebene Ergebnisort. Bei Abbruch bleibt ein eigener Teilversuch erhalten; keine bestehende Aufnahme überschreiben.
13. Höre die ganze kurze Probe. Vergleiche den tatsächlich gesprochenen Text Wort für Wort. Prüfe Zahlen, Produktnamen, Satzenden, Pausen und abrupte Schnitte. Ein hörbar gutes Ergebnis ist mehr als ein gültiger WAV-Container. HOERPROTOKOLL.csv bleibt bis zu deiner Prüfung leer.
14. Längerer Text: ganze kleine Absätze einzeln erzeugen, identische Referenz verwenden, jeden Absatz prüfen. Keine automatischen Schnitte in Wörter und keine pauschalen Fades über Wortenden. Eine kurze vollständige Aussage kann unter2Sekunden dauern; bloße Dauer ist kein Inhaltsbeweis.
15. Für ein Video echte Audiodauer messen, daraus Bildzeiten, Kapitel und Untertitel ableiten. Automatisch angenäherte Satzzeiten sind kein wortgenauer ASR-Beleg. Technische Filmprüfung und vollständiges Endhören getrennt dokumentieren.
16. Bewahre Text, WAV, Referenzhash, Version, Parameter und ausgefülltes Hörprotokoll gemeinsam auf. Für einen anderen Rechner gelten passende Software und freie Ressourcen; andere AMD-GPUs/Mac-Neuinstallationen sind hier nicht bestätigt. Neue Filme und vollständige Endhörprüfung werden separat fertiggestellt.
