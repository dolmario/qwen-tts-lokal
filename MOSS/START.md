# Einen vollständigen Absatz mit MOSS erzeugen

Für die neuen englischen Videos verwenden wir die synthetische s44-Referenz und den Aufbau aus dem Server-Tutorial 55. Jörg hat die Originalabsätze aus 55 und 65 gegengehört und 55 gewählt. Eine eigene private Personenaufnahme wird nicht mitgeliefert.

## Umgebung und Modelle

Unser vorhandener Windows-Aufbau auf dem EVO-X2 nutzt Python 3.12 und AMD-PyTorch/torchaudio `2.9.1+rocm7.2.1`. Für die passenden GPU-Pakete gilt [AMDs Windows-Anleitung](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/windows/install-pytorch.html). Mit dem Python dieser Umgebung:

```powershell
& 'C:\DEINE-UMGEBUNG\Scripts\python.exe' -m pip install -r .\MOSS\requirements-zusatz.txt
& 'C:\DEINE-UMGEBUNG\Scripts\python.exe' .\MOSS\moss_probe.py download
& 'C:\DEINE-UMGEBUNG\Scripts\python.exe' .\MOSS\moss_probe.py check
```

Die Zusatzdatei installiert kein GPU-PyTorch. Download und Check beziehen beziehungsweise prüfen die festgelegten Sprachmodell- und Codec-Versionen. `STIMME.json` beschreibt unsere Referenz.

## Englischen Absatz erzeugen

Andere Modellarbeit vorher abschließen. Der Wrapper beendet selbst keine Dienste. Er prüft bekannte Ports sowie 12,5 GiB freien Arbeitsspeicher und 14,3 GiB Gerätefreiraum vor dem Laden. Nach dem Laden und zwischen Absätzen prüft er mindestens 2,5 GiB freien Arbeitsspeicher.

```powershell
& 'C:\DEINE-UMGEBUNG\Scripts\python.exe' .\MOSS\moss_probe.py speak `
  --language English `
  --text .\MOSS\PROBE-EN.txt `
  --reference .\MOSS\stimme-s44.wav `
  --output .\MEINE-MOSS-PROBE-01
```

Ein neuer Ausgabeordner enthält die WAV, die Originalausgaben, den Text und den Bericht. Einstellungen: Seed 1234, Temperatur 1,7, top_p 0,8, top_k 25, BF16/SDPA; ursprünglicher direkter GPU-Ladeweg aus 55/65. Ausgabe: 48 kHz Stereo, anschließend 0,4 Sekunden Stille.

## Weiteren Absatz aufnehmen

Für den nächsten Absatz Text und Ausgabeordner ändern; Referenz und Einstellungen behalten. Die ganze Datei bis zum Satzende anhören. Fachwörter bei Bedarf im Eingabetext anpassen und den vollständigen Absatz erneut erzeugen.

Ein deutscher eigener Versuch verwendet `--language German` und `PROBE-DE.txt`. Die neue Videofassung hat englischen Ton, deutsche Untertitel und deutsche Studio-Texte. Die früher gehörte kurze deutsche Probe bleibt ein eigener Befund.

Unser alter [Qwen-Weg](../DE/START.md) bleibt dokumentiert. Die Auswahl von MOSS beruht auf unserem gehörten lokalen Aufbau; ein optimierter Qwen-Python-Gegenversuch mit vollständigem Referenztranskript wurde dabei nicht abgenommen. Getestet wurde auf dem EVO-X2; Einrichtung und Zeiten können anderswo abweichen.
