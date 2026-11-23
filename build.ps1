<#
.Synopsis
Activates the project virtual environment, sets PYTHONPATH so the custom_fences
module resolves, and builds the Zensical site.
#>
$root = $PSScriptRoot
& "$root\venv\Scripts\Activate.ps1"
$env:PYTHONPATH = "$root\docs\assets\python"
zensical build --clean
