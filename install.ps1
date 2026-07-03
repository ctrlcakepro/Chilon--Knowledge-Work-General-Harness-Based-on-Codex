param(
    [string]$TargetDir,
    [switch]$SkipAutomations
)

$ErrorActionPreference = "Stop"

function Write-Step($message) {
    Write-Host "[harness-installer] $message"
}

function Copy-WithBackup {
    param(
        [string]$SourcePath,
        [string]$DestinationPath,
        [string]$BackupRoot
    )

    if (Test-Path -LiteralPath $DestinationPath) {
        $backupPath = Join-Path $BackupRoot ([IO.Path]::GetFileName($DestinationPath))
        Write-Step "Backup existing item: $DestinationPath -> $backupPath"
        Copy-Item -LiteralPath $DestinationPath -Destination $backupPath -Recurse -Force
        Remove-Item -LiteralPath $DestinationPath -Recurse -Force
    }

    Write-Step "Install item: $DestinationPath"
    Copy-Item -LiteralPath $SourcePath -Destination $DestinationPath -Recurse -Force
}

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not $TargetDir) {
    $TargetDir = Read-Host "Enter the absolute path of the target project directory"
}

if (-not $TargetDir) {
    throw "No target directory provided. Installation cancelled."
}

$ResolvedTarget = [IO.Path]::GetFullPath($TargetDir)
if (-not (Test-Path -LiteralPath $ResolvedTarget)) {
    Write-Step "Create target directory: $ResolvedTarget"
    New-Item -ItemType Directory -Path $ResolvedTarget | Out-Null
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$BackupRoot = Join-Path $ResolvedTarget ".harness-install-backup\$timestamp"
New-Item -ItemType Directory -Path $BackupRoot -Force | Out-Null

$itemsToInstall = @(
    "AGENTS.md",
    "PROJECT-WORKFLOW.md",
    ".project-memory",
    "harness-regression",
    "tools"
)

Write-Step "Install target: $ResolvedTarget"
Write-Step "Backup root: $BackupRoot"

foreach ($item in $itemsToInstall) {
    $sourcePath = Join-Path $PackageRoot $item
    if (-not (Test-Path -LiteralPath $sourcePath)) {
        throw "Package is missing required item: $item"
    }
    $destinationPath = Join-Path $ResolvedTarget $item
    Copy-WithBackup -SourcePath $sourcePath -DestinationPath $destinationPath -BackupRoot $BackupRoot
}

if (-not $SkipAutomations) {
    $automationSource = Join-Path $PackageRoot "automations"
    if (Test-Path -LiteralPath $automationSource) {
        $codexAutomationRoot = Join-Path $env:USERPROFILE ".codex\automations"
        New-Item -ItemType Directory -Path $codexAutomationRoot -Force | Out-Null

        $automationMap = @{
            "weekly-harness-maintenance.toml" = "weekly-harness-maintenance"
            "monthly-harness-deep-audit.toml" = "monthly-harness-deep-audit"
        }

        foreach ($entry in $automationMap.GetEnumerator()) {
            $sourceFile = Join-Path $automationSource $entry.Key
            if (-not (Test-Path -LiteralPath $sourceFile)) {
                continue
            }

            $targetFolder = Join-Path $codexAutomationRoot $entry.Value
            $targetFile = Join-Path $targetFolder "automation.toml"
            New-Item -ItemType Directory -Path $targetFolder -Force | Out-Null

            if (Test-Path -LiteralPath $targetFile) {
                $automationBackupRoot = Join-Path $BackupRoot "automations\$($entry.Value)"
                New-Item -ItemType Directory -Path $automationBackupRoot -Force | Out-Null
                Copy-Item -LiteralPath $targetFile -Destination (Join-Path $automationBackupRoot "automation.toml") -Force
            }

            Write-Step "Install automation config: $targetFile"
            Copy-Item -LiteralPath $sourceFile -Destination $targetFile -Force
        }
    }
}

Write-Step "Installation complete."
Write-Step "If this is a Git project, review the diff before committing."
