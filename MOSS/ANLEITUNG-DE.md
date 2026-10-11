# MOSS: kurze englische Sprachprobe

Der Begleitordner enthält den tatsächlich verwendeten Helfer für die synthetische EN55-Stimme. Modellgewichte und Referenzton sind nicht gebündelt. Eine eigene nutzbare WAV-Referenz als `reference.wav` bereitstellen.

Gemessene Bestandsumgebung: Python3.11, torch/torchaudio2.9.1+rocm7.2.1; übrige feste Versionen in `requirements-helper.txt`. Passenden offiziellen GPU-PyTorch-Aufbau für das eigene Gerät verwenden. Die Installation auf einer neuen Maschine ist nicht als getestet behauptet. AMD-Anleitung: https://rocm.docs.amd.com/projects/install-on-windows/en/latest/how-to/pytorch.html

```powershell
python -m pip install -r requirements-helper.txt
python moss_probe.py download
python moss_probe.py check
python moss_probe.py speak --text text-en.txt --reference reference.wav --output erste-probe --language English
```

Download lädt einmalig feste Revisionen; spätere Erzeugung nutzt den Cache. Remote-Code der festen Modellrevision vor der ersten Ausführung prüfen. Bekannte belegte Modellports werden verweigert, keine fremden Prozesse beendet. Mindestens12,5GiB physischer und14,3GiB Gerätespeicher beim Laden, nachher2,5GiB physisch sind gemessene Schutzschwellen.

Ein Absatz mit1..280Zeichen; neuer Ausgabeordner. Referenz unverändert bewahren. Temperatur1,7/top_p0,8/top_k25/Seed1234;48kHz Stereo;0,4s echte digitale Stille am Ende. Originalfloatton, PCM-Fassungen, Text und Bericht bleiben getrennt. Schwierige Zahlen/Kürzel ausschreiben. Für andere Sprecher die Referenz wechseln.

Vor Serienproduktion die gesamte erste Probe hören. Englische Vergleichsproben verwenden denselben Satz und−23LUFS. Erzeugungszeit/Tonlänge ergibt Echtzeitfaktor. ASR/Decode sind technische Hilfen, keine menschliche Hörprüfung. Modellquellen und Lizenzen stehen in README.md.
