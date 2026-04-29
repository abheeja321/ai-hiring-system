$python = "C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if (-not (Test-Path .venv\Scripts\python.exe)) {
    New-Item -ItemType Directory -Force .tmp | Out-Null
    $env:TEMP = (Resolve-Path .tmp).Path
    $env:TMP = (Resolve-Path .tmp).Path
    & $python -m venv .venv
}

& $python -m pip --python .\.venv\Scripts\python.exe install -r requirements.txt
& .\.venv\Scripts\python.exe manage.py migrate

