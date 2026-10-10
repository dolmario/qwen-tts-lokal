"""MOSS speech probe using the pinned model, codec and measured production settings."""
from pathlib import Path
import argparse
import importlib.metadata as metadata
import json
import hashlib
import socket
import time

MODEL = ('OpenMOSS-Team/MOSS-TTS-Local-Transformer-v1.5', 'be7766a6735b98bd793f7c79fb720b4d0f5d13b8')
CODEC = ('OpenMOSS-Team/MOSS-Audio-Tokenizer-v2', 'f6e20e543b33d2c252a7ef71bdf8aa71e5ff9169')
PATTERNS = ['*.json', '*.py', '*.txt', '*.jinja', '*.safetensors']
_ENGINE = None

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_inputs(text_file, reference, output):
    text = text_file.read_text('utf-8').strip()
    if not 1 <= len(text) <= 280:
        raise ValueError('Use one complete paragraph of 1..280 characters')
    if not reference.is_file() or reference.suffix.lower() != '.wav':
        raise ValueError('A WAV voice reference is required')
    if output.exists():
        raise FileExistsError('Choose a new output directory; no overwrite')
    return text

def packages():
    return {name: metadata.version(name) for name in
            ('torch', 'torchaudio', 'transformers', 'accelerate', 'soundfile', 'huggingface-hub', 'numpy', 'psutil')}

def snapshots(download=False):
    from huggingface_hub import snapshot_download
    return [snapshot_download(name, revision=revision, local_files_only=not download,
                              allow_patterns=PATTERNS) for name, revision in (MODEL, CODEC)]

def ready(initial=True):
    import psutil
    failures=[]
    for port in (8079, 8081, 8090, 8188, 8189, 8191):
        with socket.socket() as sock:
            sock.settimeout(.3)
            if sock.connect_ex(('127.0.0.1', port)) == 0:
                failures.append(f'Existing service on {port}; arrange free resources first')
    memory = psutil.virtual_memory()
    minimum = 12.5 if initial else 2.5
    if memory.available < minimum*2**30:
        failures.append(f'Less than {minimum} GiB free physical RAM for the current loading stage')
    if failures:
        raise RuntimeError('\n'.join(failures))
    # This check supplements the operator's actual process/queue/GPU idle check.
    # It does not detect every service and never terminates one.

def run(text_file, reference, output, language='English'):
    global _ENGINE
    text = read_inputs(text_file, reference, output)
    versions = packages()
    ready(initial=_ENGINE is None)
    model_path, codec_path = snapshots()
    import numpy as np
    import soundfile as sf
    import torch
    import torchaudio
    from transformers import AutoConfig, AutoTokenizer, AutoModel
    from transformers.dynamic_module_utils import get_class_from_dynamic_module
    import psutil

    if not torch.cuda.is_available():
        raise RuntimeError('This measured route requires GPU PyTorch; ROCm also exposes torch.cuda')
    free, total = torch.cuda.mem_get_info()
    if _ENGINE is None and free < 14.3*2**30:
        raise RuntimeError('Less than the measured 14.3 GiB device headroom')
    reference_audio, reference_rate = sf.read(reference, dtype='float32', always_2d=True)
    if len(reference_audio) == 0 or not np.isfinite(reference_audio).all():
        raise ValueError('Invalid reference audio')

    def load_audio(path, *args, **kwargs):
        audio, rate = sf.read(path, dtype='float32', always_2d=True)
        return torch.from_numpy(audio.T.copy()), rate
    torchaudio.load = load_audio
    # Original direct-GPU processor construction used for episodes 55 and 65.
    # Same pinned weights, original synthetic s44 reference and generation settings.
    if _ENGINE is None:
        config=AutoConfig.from_pretrained(model_path,trust_remote_code=True,local_files_only=True)
        tokenizer=AutoTokenizer.from_pretrained(model_path,trust_remote_code=True,local_files_only=True)
        codec=AutoModel.from_pretrained(codec_path,trust_remote_code=True,local_files_only=True,
            device_map={'':'cuda:0'},codec_weight_dtype='bf16')
        assert all(p.device.type=='cuda' for p in codec.parameters())
        assert all(p.dtype==torch.float32 for p in codec.quantizer.parameters())
        processor_class=get_class_from_dynamic_module(config.auto_map['AutoProcessor'],model_path,local_files_only=True)
        processor=processor_class(tokenizer=tokenizer,audio_tokenizer=codec,model_config=config)
        model=AutoModel.from_pretrained(model_path,trust_remote_code=True,local_files_only=True,
            attn_implementation='sdpa',torch_dtype=torch.bfloat16,device_map={'':'cuda:0'}).eval()
        codec_loading={'route':'original direct-GPU loader of episodes 55 and 65','approved_original_55_sha256':'dbfab3ccbefa25c2c4ce73adcb9319fdca83a952092fabb11ca9bf344e3a76c0','new_streaming_loader_used':False,'quantizer_dtype':'float32','encoder_decoder_dtype':'bfloat16'}
        _ENGINE=(processor,model,codec_loading)
    else:
        processor, model, codec_loading = _ENGINE
    if psutil.virtual_memory().available < 2.5*2**30:
        raise RuntimeError('Less than 2.5 GiB physical RAM after model load; stop own probe')
    torch.manual_seed(1234)
    if language not in ('English','German'):raise ValueError('Unsupported requested language')
    batch = processor([[processor.build_user_message(text=text, reference=[str(reference)], language=language)]], mode='generation')
    start=time.perf_counter()
    with torch.no_grad():
        result=model.generate(input_ids=batch['input_ids'].to('cuda'), attention_mask=batch['attention_mask'].to('cuda'),
            max_new_tokens=2048, do_sample=True, audio_temperature=1.7, audio_top_p=.8, audio_top_k=25, audio_repetition_penalty=1.)
    audio=[message for message in processor.decode(result) if message is not None][0].audio_codes_list[0].cpu().float().numpy().T
    rate=processor.model_config.sampling_rate
    peak=float(np.max(np.abs(audio)))
    if rate != 48000 or audio.ndim != 2 or audio.shape[1] != 2 or not np.isfinite(audio).all() or peak > 1.1:
        raise RuntimeError('Unexpected audio format or codec amplitude; own probe stops')
    output.mkdir(parents=True, exist_ok=False)
    sf.write(output/'probe-float-original.wav', audio, rate, subtype='FLOAT')
    gain=min(1., .98/peak) if peak else 1.
    scaled=audio*gain
    sf.write(output/'probe-roh.wav', scaled, rate, subtype='PCM_16')
    sf.write(output/'probe.wav', np.concatenate([scaled,np.zeros((19200,2),dtype=scaled.dtype)]), rate, subtype='PCM_16')
    (output/'SPRECHTEXT.txt').write_text(text+'\n', encoding='utf-8')
    report={'model': MODEL, 'codec': CODEC, 'packages': versions, 'reference_sha256': sha(reference), 'language':language,
        'sampling_rate': rate, 'channels': 2, 'audio_seconds': len(audio)/rate,
        'synthesis_seconds': time.perf_counter()-start, 'pause_seconds': .4,
        'seed': 1234, 'parameters': {'temperature': 1.7,'top_p':.8,'top_k':25,'dtype':'bf16','attention':'sdpa'},
        'original_float_peak': peak, 'pre_pcm_gain': gain, 'probe_sha256': sha(output/'probe.wav'),
        'full_human_listening': False, 'new_model_download': False, 'gpu_name': torch.cuda.get_device_name(0),
        'codec_loading':codec_loading,'own_peak_working_set_gib':psutil.Process().memory_info().peak_wset/2**30}
    (output/'BERICHT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('task',choices=('check','download','speak'))
    parser.add_argument('--text',type=Path)
    parser.add_argument('--reference',type=Path)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--language',choices=('English','German'),default='English')
    args=parser.parse_args()
    if args.task == 'check':
        print(json.dumps({'packages':packages(),'model':MODEL,'codec':CODEC,
                          'cache_paths':snapshots(),'model_loaded':False},ensure_ascii=False,indent=2))
    elif args.task == 'download':
        print(json.dumps({'cache_paths':snapshots(download=True),'model_loaded':False},ensure_ascii=False,indent=2))
    else:
        if None in (args.text,args.reference,args.output):
            parser.error('speak requires --text, --reference and --output')
        run(args.text,args.reference,args.output,args.language)

if __name__ == '__main__':
    main()
