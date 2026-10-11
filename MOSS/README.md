# MOSS local English voice companion

Actual helper used for the Dolmario EN55 synthetic narrator, fixed model and tokenizer revisions, and the fresh English comparison with Qwen3-TTS. Audio references and model weights are not bundled: supply your own reference you can use. The sample texts are English.

## Environment

The measured existing Windows/AMD route uses Python3.11, GPU PyTorch/torchaudio2.9.1+rocm7.2.1, transformers5.0.0, accelerate1.15.0, soundfile0.14.0, huggingface-hub1.32.0, numpy2.1.0, psutil7.2.2. ROCm exposes the `torch.cuda` interface. Use the appropriate official GPU build for your hardware and operating system; a generic CPU torch installation does not satisfy this measured route. [AMD PyTorch installation](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/how-to/pytorch.html) and [PyTorch](https://pytorch.org/get-started/locally/).

In a dedicated compatible environment, install the helper dependencies with `python -m pip install -r requirements-helper.txt`. Do not replace a working GPU stack blindly. The existing production environment was exercised; a fresh machine installation is not claimed as tested.

## Download once, then check

```powershell
python moss_probe.py download
python moss_probe.py check
```

`download` explicitly fetches the pinned model/code files. Review the pinned remote model code before running it: the implementation uses `trust_remote_code=True`. `check` reports versions/cache without loading the model. Revisions: MOSS-TTS-Local-Transformer-v1.5 `be7766a6735b98bd793f7c79fb720b4d0f5d13b8`; MOSS-Audio-Tokenizer-v2 `f6e20e543b33d2c252a7ef71bdf8aa71e5ff9169`. Later speech runs use cached files only.

## First local English paragraph

Save your reference as `reference.wav`, free resources after other work has finished, and run:

```powershell
python moss_probe.py speak --text text-en.txt --reference reference.wav --output first-take --language English
```

One complete paragraph1..280characters; choose a new output folder. The helper refuses occupied known model ports and insufficient physical/device memory, and never stops another process. Loading requires at least12.5GiB physical and14.3GiB device headroom; after loading it checks2.5GiB physical. These are measured safeguards, not universal capacity guarantees.

The production parameters are audio_temperature1.7/top_p0.8/top_k25, seed1234, SDPA/bfloat16,48kHz stereo. Codec quantizer remains float32. Output includes original float WAV, PCM WAV, a take with0.4s digital silence appended, text, and a generation report with hashes/versions/timing.

## Stable voice and listening

Keep the exact reference. A male/female instruction does not reliably replace the reference's voice; choose another usable reference instead. Earlier temperature1.0 produced an overlong take in this setup;1.7 is the measured production choice. Write difficult acronyms/numbers phonetically in spoken text and preserve canonical product spelling in visible text.

Listen to one entire paragraph before a batch. For comparisons, use the same English sentence and matched loudness (`ffmpeg -i in.wav -af loudnorm=I=-23:TP=-2:LRA=9 -ar 48000 out.wav`; a second measured pass is preferable). Synthesis seconds/audio seconds gives real-time factor. Decode/transcripts do not replace listening.

The fresh Qwen comparison uses [llama.cpp TTS](https://github.com/ggml-org/llama.cpp/tree/master/tools/tts), Qwen3-TTS12Hz1.7BBaseQ8_0 on CPU, and the same own synthetic female reference. The MOSS male example changes only the reference. No German hearing sample or unverifiable old voice clone is republished.

Official model sources: [MOSS model](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Local-Transformer-v1.5), [audio tokenizer](https://huggingface.co/OpenMOSS-Team/MOSS-Audio-Tokenizer-v2), [OpenMOSS code](https://github.com/OpenMOSS/MOSS-TTS). Consult each license; no weights are distributed here.
