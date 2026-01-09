# Local SMTP demo PowerShell helper
# Usage: .venv\Scripts\Activate.ps1 ; .\backend\scripts\local_smtp_demo.ps1 -To you@example.com -Port 2505
param(
    [Parameter(Mandatory=$true)]
    [string] $To,
    [int] $Port = 2505
)

Write-Host "Starting local SMTP demo (port $Port)"
$python = Join-Path $PSScriptRoot '..\.venv\Scripts\python'
$cmd = "$python backend/scripts/local_smtp_demo.py --to $To --port $Port"
Write-Host "Running: $cmd"
& $python backend/scripts/local_smtp_demo.py --to $To --port $Port
if ($LASTEXITCODE -eq 0) {
    Write-Host "Demo succeeded"
} elseif ($LASTEXITCODE -eq 2) {
    Write-Warning "Partial success: app reported success but server saw no message"
} else {
    Write-Error "Demo failed (exit code $LASTEXITCODE)"
}
