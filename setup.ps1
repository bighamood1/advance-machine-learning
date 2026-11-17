$ErrorActionPreference = 'Stop'
$pythonExe = 'py'
$pythonPrefix = @('-3.11')
& $pythonExe @pythonPrefix -c 'import sys; assert sys.version_info[:2] == (3, 11)' 2>$null
if ($LASTEXITCODE -ne 0) {
    $candidates = @()
    if ($env:LOCALAPPDATA) {
        $candidates += Join-Path $env:LOCALAPPDATA 'Programs\Python\Python311\python.exe'
    }
    if ($env:USERPROFILE) {
        $candidates += Join-Path $env:USERPROFILE 'AppData\Local\Programs\Python\Python311\python.exe'
    }
    $candidate = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if (-not $candidate) { throw 'Python 3.11 was not found. Install Python 3.11, then rerun setup.ps1.' }
    $pythonExe = $candidate
    $pythonPrefix = @()
}
& $pythonExe @pythonPrefix -m venv .venv
if (-not (Test-Path .venv\Scripts\python.exe)) { throw 'Python 3.11 was not found. Install Python 3.11 or use the interpreter-specific commands in README.md.' }
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Write-Host 'Setup complete. Activate with .\.venv\Scripts\Activate.ps1'
