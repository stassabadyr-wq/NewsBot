Set-Location $PSScriptRoot
New-Item -ItemType Directory -Force logs | Out-Null
$env:PYTHONUTF8 = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] запуск" | Add-Content logs\newsbot.log -Encoding utf8
& .\.venv\Scripts\python.exe -m src.main 2>&1 | Add-Content logs\newsbot.log -Encoding utf8
