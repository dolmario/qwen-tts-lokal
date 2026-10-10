# From Qwen3-TTS to MOSS: Generate Your Own Local Narration

Download the current practice kit: [PRACTICE-KIT.zip](downloads/PRACTICE-KIT.zip).

Download the [practice kit](downloads/PRACTICE-KIT.zip), open [MOSS/START-EN.md](MOSS/START-EN.md), and generate a complete English paragraph. The kit includes our own synthetic female voice reference, the speech runner, pinned model and codec revisions, and two sample texts. Keep the reference and generation settings when you change the text.

The MOSS runner uses the direct GPU processor and codec construction from our local-server tutorial. It saves the WAV, input text, settings and measured durations together in a new output folder. A batch can reuse the loaded model for subsequent paragraphs. Our Windows EVO-X2 run used an existing working AMD PyTorch environment and produced 102 English paragraphs; follow the linked AMD installation guide for your GPU environment.

We chose MOSS after listening to our local examples. The earlier [Qwen CPU workflow](EN/START.md) remains available. Its pinned official Windows runtime was downloaded and extracted in an isolated installation test. Supply your own suitable reference recording for that route; a person's recording is not bundled. These are two documented setups, rather than a general model ranking.

Original projects: [MOSS-TTS](https://github.com/OpenMOSS/MOSS-TTS) and [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS).

Test hardware: [GMKtec EVO-X2 / shop](https://de.gmktec.com/?ref=DolmarioAi) · advertisement / affiliate link.

## Deutsch

Mit [der MOSS-Anleitung](MOSS/START.md) einen vollständigen Absatz lokal erzeugen. Das Paket enthält unsere eigene synthetische Frauenstimme, Beispieltexte und den Python-Starter. Für weitere Texte bleiben Referenz und Einstellungen gleich; jede Ausgabe bekommt einen neuen Ordner mit Tondatei, Text und Messprotokoll.

Unser Windows-Lauf auf dem EVO-X2 verwendete eine bereits funktionierende AMD-PyTorch-Umgebung. Die Anleitung verlinkt den passenden Installationsweg. Der frühere Qwen-CPU-Weg bleibt dokumentiert; eine private Personenaufnahme gehört nicht zum Paket.
