# Excel for Finance - full setup check
#
# Run it from the project folder in a NEW terminal window:
#
#     .\check_setup.ps1
#
# If Windows says "running scripts is disabled on this system", run this once
# and then try again:
#
#     Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
#
# The script only READS your setup. It changes nothing except installing the
# project's Python libraries (uv sync) and writing two report files.

$ErrorActionPreference = 'Continue'
$results = New-Object System.Collections.Generic.List[string]
$script:fails = 0
$script:warns = 0

function Add-Result([string]$status, [string]$label, [string]$detail) {
    $line = "[$status] $label"
    if ($detail) { $line = "$line - $detail" }
    $results.Add($line)
    $colour = 'Green'
    if ($status -eq 'FAIL') { $colour = 'Red'; $script:fails++ }
    if ($status -eq 'WARN') { $colour = 'Yellow'; $script:warns++ }
    Write-Host $line -ForegroundColor $colour
}

function Test-Tool([string]$name, [string]$label, [bool]$required, [string]$fix) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if (-not $cmd) {
        $status = 'WARN'
        if ($required) { $status = 'FAIL' }
        Add-Result $status $label "not found. $fix"
        return
    }
    $version = ''
    try { $version = (& $name --version 2>$null | Select-Object -First 1) } catch { $version = '' }
    if (-not $version) { $version = 'installed' }
    Add-Result 'PASS' $label ([string]$version).Trim()
}

Write-Host ''
Write-Host 'Excel for Finance - setup check' -ForegroundColor Cyan
Write-Host '================================' -ForegroundColor Cyan

# 1. PowerShell itself
$policy = Get-ExecutionPolicy -Scope CurrentUser
if ($policy -eq 'RemoteSigned' -or $policy -eq 'Unrestricted' -or $policy -eq 'Bypass') {
    Add-Result 'PASS' 'PowerShell script policy' "$policy"
} else {
    Add-Result 'WARN' 'PowerShell script policy' "CurrentUser is '$policy'. Run: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned"
}

# 2. Programs
Test-Tool 'git'      'Git'                  $true  'Install Git for Windows (guide step 3), then open a NEW terminal.'
Test-Tool 'code'     'VS Code (code command)' $true 'Install VS Code (guide step 3), then open a NEW terminal.'
Test-Tool 'node'     'Node.js'              $true  'Install Node.js LTS (guide step 3), then open a NEW terminal.'
Test-Tool 'npm'      'npm (comes with Node)' $true 'Reinstall Node.js LTS.'
Test-Tool 'uv'       'uv (Python manager)'  $true  'Install uv (guide step 3), then open a NEW terminal.'
Test-Tool 'opencode' 'OpenCode agent'       $true  'Run: npm install -g opencode-ai'
Test-Tool 'agy'      'Antigravity CLI agent' $false 'Optional second agent - see guide step 6.'

# 3. Git identity
$gitName = ''
$gitEmail = ''
if (Get-Command git -ErrorAction SilentlyContinue) {
    $gitName = (git config --global user.name) 2>$null
    $gitEmail = (git config --global user.email) 2>$null
}
if ($gitName -and $gitEmail) {
    Add-Result 'PASS' 'Git identity' "$gitName <$gitEmail>"
} else {
    Add-Result 'FAIL' 'Git identity' 'Run: git config --global user.name "Your Name"  and  git config --global user.email "you@example.com"'
}

# 4. VS Code extensions
if (Get-Command code -ErrorAction SilentlyContinue) {
    $extensions = (code --list-extensions 2>$null) | ForEach-Object { $_.ToLower() }
    $wanted = @(
        @('ms-python.python', $true),
        @('ms-toolsai.jupyter', $true),
        @('ms-toolsai.datawrangler', $true),
        @('grapecity.gc-excelviewer', $false),
        @('sst-dev.opencode', $false)
    )
    foreach ($item in $wanted) {
        $id = $item[0]
        if ($extensions -contains $id) {
            Add-Result 'PASS' "VS Code extension $id" ''
        } else {
            $status = 'WARN'
            if ($item[1]) { $status = 'FAIL' }
            Add-Result $status "VS Code extension $id" "Run: code --install-extension $id"
        }
    }
}

# 5. This project folder: cloned from GitHub, first commit pushed
$insideRepo = $false
if (Get-Command git -ErrorAction SilentlyContinue) {
    $insideRepo = ((git rev-parse --is-inside-work-tree 2>$null) -eq 'true')
}
if (-not $insideRepo) {
    Add-Result 'FAIL' 'Project folder is a Git repository' 'Run this script inside the folder you cloned from GitHub (guide step 5).'
} else {
    $remote = (git remote get-url origin 2>$null)
    if ($remote -match 'github\.com') {
        Add-Result 'PASS' 'Connected to GitHub' $remote
    } else {
        Add-Result 'FAIL' 'Connected to GitHub' 'No GitHub "origin" remote. Clone your own copy of the template (guide step 5).'
    }
    git fetch --quiet origin 2>$null
    $branch = (git rev-parse --abbrev-ref HEAD 2>$null)
    $ahead = (git rev-list --count "origin/$branch..HEAD" 2>$null)
    $mine = ''
    if ($gitEmail) { $mine = (git log --author="$gitEmail" --oneline -1 2>$null) }
    if (-not $mine) {
        Add-Result 'FAIL' 'Your first commit' 'No commit with your e-mail yet. Do the "hello" commit (guide step 5).'
    } elseif ($ahead -and [int]$ahead -gt 0) {
        Add-Result 'FAIL' 'Your first commit is on GitHub' "$ahead commit(s) not pushed yet. Run: git push"
    } else {
        Add-Result 'PASS' 'Your first commit is on GitHub' $mine
    }
}

if (Test-Path (Join-Path $PSScriptRoot 'AGENTS.md')) {
    Add-Result 'PASS' 'Agent instructions file' 'AGENTS.md found'
} else {
    Add-Result 'FAIL' 'Agent instructions file' 'AGENTS.md is missing - re-clone the template.'
}

# 6. Python, libraries and Excel round trip (delegated to the Python check)
if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host ''
    Write-Host 'Installing the project libraries (uv sync) - the first run can take a minute...' -ForegroundColor Cyan
    Push-Location $PSScriptRoot
    uv sync --quiet
    $syncCode = $LASTEXITCODE
    if ($syncCode -ne 0) {
        Add-Result 'FAIL' 'Install Python libraries (uv sync)' "exit code $syncCode - check your internet connection and run: uv sync"
    } else {
        Add-Result 'PASS' 'Install Python libraries (uv sync)' ''
        Write-Host ''
        uv run python scripts/check_setup.py
        if ($LASTEXITCODE -eq 0) {
            Add-Result 'PASS' 'Python + Excel check' 'output\setup_check.xlsx written'
        } else {
            Add-Result 'FAIL' 'Python + Excel check' 'see the lines above'
        }
    }
    Pop-Location
}

# 7. Summary and report file
Write-Host ''
$os = [System.Environment]::OSVersion.VersionString
$summary = "SUMMARY: $($script:fails) failed, $($script:warns) warnings"
if ($script:fails -eq 0) {
    $summary = "READY FOR THE MODULE ($($script:warns) optional warnings)"
    Write-Host $summary -ForegroundColor Green
} else {
    Write-Host $summary -ForegroundColor Red
    Write-Host 'Fix the FAIL lines (each one says how), open a NEW terminal and run .\check_setup.ps1 again.' -ForegroundColor Red
}

$header = @(
    'Excel for Finance - setup report',
    ('Date: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm')),
    ('PowerShell: ' + $PSVersionTable.PSVersion.ToString()),
    ('Windows: ' + $os),
    ''
)
$reportPath = Join-Path $PSScriptRoot 'setup_report.txt'
($header + $results + @('', $summary)) | Set-Content -Path $reportPath -Encoding UTF8
Write-Host "Report saved to $reportPath - post a screenshot of the summary in the course Teams channel."
