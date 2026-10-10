# Generate your own English narration with MOSS

Use our synthetic s44 reference and the settings selected for our local-server tutorial. Jörg compared the original English excerpts from videos 55 and 65 and selected 55. Keep that reference for subsequent paragraphs.

## Prepare the Python environment

Our working machine is an EVO-X2 with Strix Halo, Windows and Python 3.12. It uses AMD PyTorch and torchaudio `2.9.1+rocm7.2.1`. Follow [AMD’s Windows installation guide](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/windows/install-pytorch.html) for the matching GPU wheels. The Linux ROCm index is a separate installation route.

Install the additional packages with that environment’s Python:

```powershell
& 'C:\YOUR-ENV\Scripts\python.exe' -m pip install -r .\MOSS\requirements-zusatz.txt
```

The additional requirements do not install GPU PyTorch. Our execution used an existing working AMD environment; another computer’s installation can differ.

## Download and inspect the files

```powershell
& 'C:\YOUR-ENV\Scripts\python.exe' .\MOSS\moss_probe.py download
& 'C:\YOUR-ENV\Scripts\python.exe' .\MOSS\moss_probe.py check
```

These commands retrieve the pinned speech-model and codec revisions, then display packages and cache paths. Open `PROBE-EN.txt` and `STIMME.json`. The reference is our own synthetic output; it contains no private person’s recording.

## Generate a paragraph

Finish competing model work first. The wrapper checks known service ports and never stops services itself. It requires 12.5 GiB available physical RAM and 14.3 GiB device headroom at startup, retaining at least 2.5 GiB RAM after loading and between paragraphs.

```powershell
& 'C:\YOUR-ENV\Scripts\python.exe' .\MOSS\moss_probe.py speak `
  --language English `
  --text .\MOSS\PROBE-EN.txt `
  --reference .\MOSS\stimme-s44.wav `
  --output .\MY-MOSS-SAMPLE-01
```

Choose a new output folder. The runner uses the direct GPU processor/codec construction from videos 55/65, BF16/SDPA for the speech model, seed 1234, temperature 1.7, top_p 0.8 and top_k 25. It keeps the codec’s original precision policy.

## Open, listen and repeat

Open `probe.wav`: 48 kHz stereo with 0.4 seconds of silence after the complete paragraph. `SPRECHTEXT.txt`, the original float/PCM audio and `BERICHT.json` retain the text, reference hash, parameters and measured durations.

For another paragraph, use `ABSATZ-02-EN.txt`, the same reference and a new output folder. Write numbers as you want them spoken. If a term needs correction, regenerate its complete paragraph and listen through its ending. A batch in one Python process can reuse the loaded model.

The original short English excerpt was heard and chosen. Complete new films have a separate listening state.

## Why we changed from Qwen

Our earlier Qwen setup used llama-tts, Q8_0 weights, four CPU threads and a short voice reference without its transcript. We selected the MOSS narration after listening to our local examples. [The earlier Qwen workflow](../EN/START.md) remains available. `install_qwen.py` installs its pinned Windows runtime into a new folder; that download/extraction was tested. An optimized Qwen Python run with a reference transcript was not our historical comparison.

Original implementations: [MOSS-TTS](https://github.com/OpenMOSS/MOSS-TTS) and [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS).
