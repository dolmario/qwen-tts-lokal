# Qwen3-TTS: your first short reference-based speech test

This is the Qwen3-TTS guide of this repository. The narrator voices of the new films (MOSS s44 and s77) are synthetic voices, not recordings of private persons; they are not part of this package and not Qwen output.

1. Extract the complete ZIP into a new companion folder. Read BUILD-SOURCE.json and PROFILE.json. This is the documented historical GGUF/CPU path, not a freshly verified clean install.
2. The official prerelease is b10621, commit c1d0e7a004015f23bc0233470b747b596f29b264. BUILD-SOURCE.json identifies the Windows Vulkan archive. The documented speech profile still uses CPU settings. Assess any other package separately.
3. Check a downloaded archive with Get-FileHash -Algorithm SHA256. Expected2672d85bf87c8280d94dee01eb6a86280046878f70a07d786a93637fa9081163. Extract everything; keep executable and libraries together. Our existing archive and52files were compared, without a new download.
4. Read .\llama-tts.exe --version and --help in your own runtime directory. Verify --tts-lang and --tts-speaker-file support. The upstream Qwen Python implementation is a separate approach.
5. Use a reference WAV that you may legitimately use: your own recording or a permitted synthetic voice. Neither third-party recordings nor our own reference files are included. A model licence does not confer rights to somebody else's voice.
6. Copy PROBE-EN.txt and first change only the short text. Spell spoken numbers naturally. Keep complete sentences together and retain reference/build/settings for comparison.
7. The archived profile uses Qwen3-TTS-12Hz-1.7B-Base-GGUF:Q8_0,-ngl0,--no-mmproj-offload,4threads,-n1500 and seed42. -n limits audio frames, not words. A fixed seed cannot guarantee complete word endings.
8. The prepared command uses -hf. Its later manual execution may download missing cached model files. Review the source, terms, memory and network decision first. Preparation itself performs noHTTP or download.
9. From the companion directory, replace all paths with your own:

```powershell
.\VORBEREITEN-QWEN.ps1 -Installation "C:\your\llama-runtime" -Reference "C:\your\my-voice.wav" -Language en -TextFile ".\PROBE-EN.txt" -OutputDirectory "C:\your\Qwen-Test-1"
```

10. Read STARTBEFEHL.txt in the new output folder. It contains one line of this pattern (with your paths and text):

```powershell
& 'C:\your\llama-runtime\llama-tts.exe' '-hf' 'ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF:Q8_0' '--tts-lang' 'en' '--tts-speaker-file' 'C:\your\my-voice.wav' '-p' '<text from PROBE-EN.txt>' '-ngl' '0' '--no-mmproj-offload' '-t' '4' '-n' '1500' '--seed' '42' '-o' 'C:\your\Qwen-Test-1\probe.wav'
```

The folder also holds `SPRECHTEXT.txt`, and VORBEREITUNG.json records prepared_only and your executable/reference hashes. No WAV has yet been generated. Existing output folders are rejected.
11. Before a Qwen attempt, check current resources and competing jobs. Do not add it to other chat/image/TTS inference on our shared64GB system. Never stop another person's process. Use one job for the first test; two historical jobs are not a general recommendation.
12. Only after your own review, deliberately run the command. Keep the terminal open and preserve errors/actual elapsed time. probe.wav is the planned output. Preserve interrupted attempts and never overwrite existing recordings.
13. Listen to the complete short recording. Compare the spoken words with the text. Check numbers, technical names, endings, pauses and abrupt cuts. A valid WAV container is not proof of good speech. Fill in HOERPROTOKOLL.csv only from actual observations.
14. For longer text, generate small complete paragraphs with the same reference and review each one. Do not cut within words or blindly fade endings. A complete short statement can last under two seconds; duration alone cannot establish content correctness.
15. For video, measure actual audio duration before image timings, chapters and subtitles. Approximated sentence timings are not word-level ASR alignment. Document technical verification and complete listening separately.
16. Keep text,WAV,reference hash,version,settings and your completed listening record together. Other machines require matching software and free resources. Other AMD/Mac clean installations are unverified here.
