# PnP SharePoint template with logging

Template base used for SharePoint scripts using PnP PowerShell. Template includes PnP connect and disconnect functions, as well as log to log file, Seq, and console logging.  

```pnp title="SharePoint Template with Logging"

<##############################################
Author:       
Date:         
Description:  PnP SharePoint Template with Logging 
Location:      
##############################################>

param (  
    # Debug, Error, Fatal, Information, Verbose, Warning
    [string] $MinLogLevel = "Information",
    [switch] $seqLogging, # Writes to Seq
    [switch] $debug, # Writes to network log file
    [switch] $consoleLog, # Outputs to console, debug must be enabled
    [string] $guid = [System.Guid]::NewGuid(), # Create unique GUID
    [string] $logFileName = 'RenameFile-Log'
)

# Test Data
$web = @{url = 'https://blotter.sharepoint.com' }
#$list = 'SharePointListName' #@{Title = "SharePointListName" }
#$itemid = 1

# Imports/ Modules
$scriptDirInfo = New-Object System.IO.DirectoryInfo($PSScriptRoot)
$scriptParentDir = $scriptDirInfo.Parent.FullName
. \\**UPDATE--ServerPath**\PowerShell\CommonLib.ps1 # Load the common library, Required for MSGraph token


$shared = [System.IO.Path]::Combine($scriptParentDir, "Shared", "Logging.ps1")
. $shared
Initialize-Logging -MinLogLevel $MinLogLevel -CorrelationId $guid | Out-Null

# Push logging comment to SeqLogging and WriteLog
function log
{
    param(
        [Parameter(Mandatory = $false)]
        [switch] $includeSeq,

        [Parameter(Mandatory = $false)]
        [string] $logType,

        [Parameter(Mandatory = $true)]
        [string] $comment
    )

    # Send to logging functions
    if ($includeSeq)
    {
        if ($logType) { SeqLogging -comment $comment -logType $logType } else { SeqLogging -comment $comment }
    }
    writeLog -comment $comment
}

# Seq Logging
function seqLogging
{
    Param(
        [string] $comment = 'n/a',
        [string] $logType = 'Write-InfoLog'
    )

    if ($seqLogging)
    {
        & $logType "{list} | Comment: {Comment} " -PropertyValues $list, $comment
    }
}

# Debug Logging
function writeLog
{
    Param(
        [string] $comment
    )

    #debug file location
    $logFile = Join-Path $PSScriptRoot "$logFileName.log"

    $maxLogSize = 1MB
    if ((Test-Path $logFile) -AND (Get-Item $logFile).Length -gt $maxLogSize)
    {
        Clear-Content $logFile
        writeLog -comment ("Log file cleared due to {0}MB size limit" -f ($maxLogSize / 1MB))
    }

    if ($debug)
    {
        $timeStamp = Get-Date -Format "MM/dd/yyyy HH:mm:ss"
        $logMessage = "$timeStamp -- $comment"
        Add-Content $logFile -value $logMessage
    }

    if ($consoleLog)
    {
        Write-Host -f Cyan $comment
    }
}

# PnP Connect
function connect()
{
    writeLog -comment $("-" * 50)
    try
    {
        $connect = Connect-PnPOnline $web.Url -CurrentCredentials -ReturnConnection
        log -comment ("Connect-PnPOnline connection success. {0}" -f $web.Url)
        return $connect
    }
    catch
    {
        log -logType 'Write-ErrorLog' -includeSeq -comment 'Connect-PnPOnline connection failed'
    }
}

# PnP Disconnect
function disconnect($connect)
{
    try
    {
        # PnP Disconnect 
        Disconnect-PnPOnline -Connection $connect
        log -comment 'Connect-PnPOnline connection closed'
    }
    catch
    {
        log -logType 'Write-ErrorLog' -includeSeq -comment 'Connect-PnPOnline disconnect failed'
    }
}

function MainScript()
{
    try
    {
        # Connect to PnP
        $connect = connect

        log -comment "Logging function is working..."


        # Disconnect PnP
        disconnect $connect
    }
    catch
    {
        # Add to log
        log -logType 'Write-ErrorLog' -includeSeq -comment ("MainScript: {0} on line {1}" -f $_.Exception.message, ($_.InvocationInfo.ScriptLineNumber))
    }
}

# Run Script
MainScript
Close-Logger
```
