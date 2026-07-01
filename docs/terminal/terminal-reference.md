# Terminal Reference

---

## Navigation

| Action | CMD | PowerShell | Git Bash |
|----------|----------|----------|----------|
| Current Directory | `cd` | `Get-Location` or `pwd` | `pwd` |
| Change Directory | `cd Folder` | `cd Folder` | `cd Folder` |
| Up One Level | `cd ..` | `cd ..` | `cd ..` |
| List Contents | `dir` | `Get-ChildItem` or `ls` | `ls` |

---

## Directory Operations

| Action | CMD | PowerShell | Git Bash |
|----------|----------|----------|----------|
| Create Directory | `mkdir MyFolder` | `mkdir MyFolder` | `mkdir MyFolder` |
| Remove Empty Directory | `rmdir MyFolder` | `Remove-Item MyFolder` | `rmdir MyFolder` |
| Remove Directory and Contents | `rmdir /s /q MyFolder` | `Remove-Item MyFolder -Recurse -Force` | `rm -rf MyFolder` |

---

## File Operations

| Action | CMD | PowerShell | Git Bash |
|----------|----------|----------|----------|
| Create File | `echo Text > file.txt` | `Set-Content file.txt "Text"` | `echo "Text" > file.txt` |
| Display File | `type file.txt` | `Get-Content file.txt` | `cat file.txt` |
| Delete File | `del file.txt` | `Remove-Item file.txt` | `rm file.txt` |
| Copy File | `copy a.txt b.txt` | `Copy-Item a.txt b.txt` | `cp a.txt b.txt` |
| Move/Rename File | `move a.txt b.txt` | `Move-Item a.txt b.txt` | `mv a.txt b.txt` |

---

## Environment Variables

| Action | CMD | PowerShell | Git Bash |
|----------|----------|----------|----------|
| View Variables | `set` | `Get-ChildItem Env:` | `env` |
| Create Variable | `set FolderName=Value` | `$FolderName = "Value"` | `FolderName="Value"` |
| Use Variable | `%FolderName%` | `$FolderName` | `$FolderName` |

---

---

## Common Translation Examples

| Tutorial Says | PowerShell Equivalent |
|----------|----------|
| `rm file.txt` | `Remove-Item file.txt` |
| `rm -rf node_modules` | `Remove-Item node_modules -Recurse -Force` |
| `cat package.json` | `Get-Content package.json` |
| `cp source.txt backup.txt` | `Copy-Item source.txt backup.txt` |
| `mv old.txt new.txt` | `Move-Item old.txt new.txt` |
| `pwd` | `Get-Location` |
| `ls -la` | `Get-ChildItem -Force` |

---

## System Commands

| Action | CMD | PowerShell | Git Bash |
|----------|----------|----------|----------|
| Open Group Policy Editor | `gpedit.msc` | `gpedit.msc` | `gpedit.msc` |
| Restart Immediately | `shutdown -r -t 0` | `shutdown -r -t 0` | `shutdown -r -t 0` |
| Open Explorer in Current Path | `start .` | `start .` | `explorer .` |
| Open Current Folder | `start .` | `ii .` | `explorer .` |
| Clear Screen | `cls` | `cls` | `clear` |
| Show Current User | `whoami` | `whoami` | `whoami` |
| Show Hostname | `hostname` | `hostname` | `hostname` |
| Show IP Configuration | `ipconfig` | `ipconfig` | `ipconfig` |
| Open Current Directory in Explorer | `start .` | `explorer .` | `explorer .` |
