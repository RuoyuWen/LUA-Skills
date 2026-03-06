param(
    [switch]$Run
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Write-Step([string]$msg) {
    Write-Host "[DEPLOY] $msg" -ForegroundColor Cyan
}

function Fail([string]$msg) {
    Write-Host "[ERROR] $msg" -ForegroundColor Red
    exit 1
}

function Parse-PythonVersion([string]$versionText) {
    if ($versionText -match "Python (\d+)\.(\d+)\.(\d+)") {
        return @{
            Major = [int]$Matches[1]
            Minor = [int]$Matches[2]
            Patch = [int]$Matches[3]
            Raw = $Matches[0]
        }
    }
    return $null
}

function Is-Python310Plus($versionInfo) {
    if (-not $versionInfo) { return $false }
    return ($versionInfo.Major -gt 3) -or ($versionInfo.Major -eq 3 -and $versionInfo.Minor -ge 10)
}

function Test-PythonCommand([string]$cmdText) {
    try {
        $versionOutput = & cmd /c "$cmdText --version" 2>&1
        if ($LASTEXITCODE -ne 0) { return $null }
        $parsed = Parse-PythonVersion (($versionOutput | Out-String).Trim())
        if (-not $parsed) { return $null }
        return @{
            Mode = "cmd"
            Command = $cmdText
            Version = $parsed
        }
    } catch {
        return $null
    }
}

function Test-PythonExe([string]$exePath) {
    if (-not (Test-Path $exePath)) { return $null }
    try {
        $versionOutput = & $exePath --version 2>&1
        if ($LASTEXITCODE -ne 0) { return $null }
        $parsed = Parse-PythonVersion (($versionOutput | Out-String).Trim())
        if (-not $parsed) { return $null }
        return @{
            Mode = "exe"
            Command = $exePath
            Version = $parsed
        }
    } catch {
        return $null
    }
}

function Get-PythonRuntime {
    $cmdCandidates = @(
        "py -3.12",
        "py -3.11",
        "py -3.10",
        "python"
    )
    foreach ($cmdText in $cmdCandidates) {
        $r = Test-PythonCommand $cmdText
        if ($r -and (Is-Python310Plus $r.Version)) { return $r }
    }

    $exeCandidates = @(
        "$env:LocalAppData\Programs\Python\Python312\python.exe",
        "$env:LocalAppData\Programs\Python\Python311\python.exe",
        "$env:LocalAppData\Programs\Python\Python310\python.exe",
        "$env:ProgramFiles\Python312\python.exe",
        "$env:ProgramFiles\Python311\python.exe",
        "$env:ProgramFiles\Python310\python.exe"
    )
    foreach ($exePath in $exeCandidates) {
        $r = Test-PythonExe $exePath
        if ($r -and (Is-Python310Plus $r.Version)) { return $r }
    }

    return $null
}

function Install-PythonIfNeeded {
    $runtime = Get-PythonRuntime
    if ($runtime) { return $runtime }

    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) {
        Fail "Python 3.10+ not found and winget is unavailable."
    }

    Write-Step "Python 3.10+ not found. Installing via winget..."
    $targets = @(
        @{ Id = "Python.Python.3.12"; Default = "3.12" },
        @{ Id = "Python.Python.3.11"; Default = "3.11" },
        @{ Id = "Python.Python.3.10"; Default = "3.10" }
    )

    $installed = $false
    $defaultVersion = ""
    foreach ($t in $targets) {
        Write-Step "Trying install $($t.Id)..."
        & winget install --id $t.Id --exact --scope user --silent --accept-source-agreements --accept-package-agreements
        if ($LASTEXITCODE -eq 0) {
            $installed = $true
            $defaultVersion = $t.Default
            break
        }
    }

    if (-not $installed) {
        Fail "Auto install Python failed. Please install Python 3.10+ manually."
    }

    Write-Step "Setting py default version to $defaultVersion"
    $env:PY_PYTHON = $defaultVersion
    & setx PY_PYTHON $defaultVersion > $null

    Start-Sleep -Seconds 2
    $runtime = Get-PythonRuntime
    if (-not $runtime) {
        Fail "Python installed but still not detected in current shell. Open a new terminal and run deploy.bat again."
    }
    return $runtime
}

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Join-Path $root "LUA-Skills\lua_story_generator"
$venvDir = Join-Path $projectDir "venv"
$requirements = Join-Path $projectDir "requirements.txt"

Write-Step "Root: $root"

if (-not (Test-Path $projectDir)) {
    Fail "Project directory not found: $projectDir"
}

if (-not (Test-Path $requirements)) {
    Fail "requirements.txt not found: $requirements"
}

$runtime = Install-PythonIfNeeded
if (-not $runtime) {
    Fail "Python runtime unavailable."
}

Write-Step "Using Python: $($runtime.Version.Raw)"
Write-Step "Runtime command: $($runtime.Command)"
Set-Location $projectDir

if (-not (Test-Path $venvDir)) {
    Write-Step "Creating virtual environment..."
    if ($runtime.Mode -eq "cmd") {
        & cmd /c "$($runtime.Command) -m venv venv"
    } else {
        & $runtime.Command -m venv venv
    }
    if ($LASTEXITCODE -ne 0) { Fail "Failed to create virtual environment." }
} else {
    Write-Step "Virtual environment exists, skip create."
}

$venvPython = Join-Path $venvDir "Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Fail "Virtual environment python not found: $venvPython"
}

Write-Step "Upgrading pip..."
& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { Fail "Failed to upgrade pip." }

Write-Step "Installing dependencies..."
& $venvPython -m pip install -r $requirements
if ($LASTEXITCODE -ne 0) { Fail "Failed to install dependencies." }

Write-Step "Deployment finished."
Write-Host "Run command: `"$venvPython`" main.py" -ForegroundColor Green
Write-Host "URL: http://localhost:9000" -ForegroundColor Green

if ($Run) {
    $startupBat = Join-Path $projectDir "startup.bat"
    if (Test-Path $startupBat) {
        Write-Step "Starting service via startup.bat..."
        & cmd /c "`"$startupBat`""
    } else {
        Write-Step "startup.bat not found, fallback to python main.py"
        & $venvPython main.py
    }
}
