[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][string]$Installation,
 [Parameter(Mandatory=$true)][string]$Reference,
 [ValidateSet('de','en')][string]$Language='de',
 [Parameter(Mandatory=$true)][string]$TextFile,
 [Parameter(Mandatory=$true)][string]$OutputDirectory
)
$ErrorActionPreference='Stop'
$installPath=(Resolve-Path -LiteralPath $Installation).Path
$exe=Join-Path $installPath 'llama-tts.exe'
if(-not(Test-Path -LiteralPath $exe -PathType Leaf)){throw 'llama-tts.exe missing'}
$ref=(Resolve-Path -LiteralPath $Reference).Path
$textPath=(Resolve-Path -LiteralPath $TextFile).Path
$speech=[IO.File]::ReadAllText($textPath,[Text.Encoding]::UTF8).Trim()
if($speech.Length -lt 1 -or $speech.Length -gt 1000){throw 'Use one short complete sentence/paragraph,1..1000 characters'}
if(Test-Path -LiteralPath $OutputDirectory){throw 'Choose a NEW output directory; no overwrite'}
$profile=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'PROFILE.json') -Raw | ConvertFrom-Json
$target=[IO.Path]::GetFullPath((Join-Path $OutputDirectory 'probe.wav'))
$arguments=@('-hf',$profile.model_hf,'--tts-lang',$Language,'--tts-speaker-file',$ref,'-p',$speech)+@($profile.arguments)+@('-o',$target)
$quoted=@($exe)+$arguments | ForEach-Object {"'"+$_.Replace("'","''")+"'"}
$command='& '+($quoted -join ' ')
New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
$encoding=[Text.UTF8Encoding]::new($false)
[IO.File]::WriteAllText((Join-Path $OutputDirectory 'STARTBEFEHL.txt'),$command+"`n",$encoding)
[IO.File]::WriteAllText((Join-Path $OutputDirectory 'SPRECHTEXT.txt'),$speech+"`n",$encoding)
[IO.File]::WriteAllText((Join-Path $OutputDirectory 'VORBEREITUNG.json'),(@{prepared_only=$true;executable_sha256=(Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash.ToLower();reference_sha256=(Get-FileHash -LiteralPath $ref -Algorithm SHA256).Hash.ToLower();language=$Language;http_requests=0;model_started=$false;audio_generated=$false;execution_may_download_model=$true;output_audio=$target} | ConvertTo-Json -Depth 8)+"`n",$encoding)
Write-Output 'Prepared only; no execution or HTTP. Read START.md before manually running this command. The -hf option can download weights when the model is absent. Your reference rights, resources and full listening must be checked separately.'
