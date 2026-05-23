<#
Usage (PowerShell):
  .\install_uv_and_tool_windows.ps1 -Tool forge
If you need to run as admin, start PowerShell as Administrator.
#>

param(
  [string]$Tool = "forge"
)

Write-Host "==> Prüfe, ob 'uv' installiert ist..."
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  Write-Host "'uv' nicht gefunden — versuche Installation via PowerShell-Installer..."
  try {
    iex (irm 'https://astral.sh/uv/install.ps1')
  } catch {
    Write-Error "Fehler beim Ausführen des Installers. Stelle sicher, dass PowerShell Remote-Skripte erlaubt sind und du online bist."
    exit 1
  }
} else {
  Write-Host "'uv' ist bereits installiert."
}

Write-Host "==> Installiere Tool: $Tool"
uv tool install $Tool

Write-Host "Fertig. Überprüfe mit: uv tool list"
