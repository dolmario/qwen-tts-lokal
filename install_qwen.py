from pathlib import Path
import argparse,hashlib,io,json,urllib.request,zipfile

def install(target):
    target=target.resolve()
    if target.exists():raise FileExistsError('Use a new target directory')
    profile=json.loads((Path(__file__).parent/'BUILD-SOURCE.json').read_text('utf-8'))
    archive=urllib.request.urlopen(profile['asset']['url'],timeout=90).read()
    digest=hashlib.sha256(archive).hexdigest()
    if digest!=profile['asset']['sha256'].removeprefix('sha256:'):raise ValueError('Official pinned release hash differs')
    members=[]
    with zipfile.ZipFile(io.BytesIO(archive)) as stream:
        if stream.testzip() is not None:raise ValueError('Release ZIP CRC failure')
        for info in stream.infolist():
            path=target/info.filename
            if not path.resolve().is_relative_to(target):raise ValueError('Release member leaves target')
            if info.is_dir():continue
            body=stream.read(info)
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(body)
            members.append({'path':info.filename,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
    if not (target/'llama-tts.exe').is_file():raise ValueError('Pinned release lacks expected TTS executable')
    (target/'INSTALLATION.json').write_text(json.dumps({'actual_download':True,'archive_sha256':digest,'release':profile['tag'],
        'source_commit':profile['commit'],'members':members,'model_started':False},indent=2)+'\n',encoding='utf-8')
    print('PINNED QWEN CPU RUNTIME INSTALLED',target,digest)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--target',type=Path,required=True)
    install(parser.parse_args().target)
