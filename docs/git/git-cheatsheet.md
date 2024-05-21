# Git Commands Cheatsheet

## GitHub Basics

```sh

git clone https://github/repo           # Clone repo from GitHub to local machine
git add . || git add fileName.txt       # Add to staging, multiple files just add a space between files
git commit -m "Fixed bug…"              # Commit changes 
git push                                # Push changes to GitHub
git pull --rebase                       # Update local with GitHub code

```

## Status

```sh

git status || git status -s             # Status
git log --oneline --all --graph         # Show linear graph of all local commits (q to exit)
git ls-files                            # Display all files being tracked in Git

```

## Reset Local

```sh
git reset -- hard                       # Reset local changes  
# Use if local repo not sync'd remote repository after rebase

```

## Staging Remove

```sh
git restore --staged file.txt || .      # Remove files from staging
git rm --cached file1.js                # Remove file from staging
git rm --cached -r logs/                # Remove folder and all contents (recursive flag)

```

## Remotes

```sh
git remote                              # List remote names
git remote -v                           # Show details of remotes
git fetch upstream                      # Get updates from source repository (default origin)
git switch master                       # Switch to master branch
git merge upstream/master               # Merge new source changes with local files
git push origin                         # Push merged changes to forked repository (GitHub)

```

## Create Git Ignore

```sh

touch .gitignore
echo JSFile1.txt > .gitignore           # Add file to .gitignore
echo JSFile2 >> .gitignore              # Append file to .gitignore
echo temp/ > .gitignore                 # Add folder to .gitignore

```

!!! tip
    - Can't create .gitignore file: Ensure file is UTF-8 encoded
    - Files not removed from untracked once added to .gitignore: Ensure correct encoding
    - Using echo in PowerShell terminal causes issue: Use Bash terminal or PowerShell cmdlet for adding content

## Rename/Move

```sh

git mv file1.js file2.txt               # Rename or move file
git docs/microsoft docs/tmp             # Rename folder

```

!!! tip
    GitHub is a case-sensitive environment.<br>

    If your local folder is named microsoft and the GitHub folder (Microsoft) doesn't match case, you need to rename it to something different and then back.<br>

    For example:<br>
    `git docs/microsoft docs/tmp`, commit and push changes<br>
    `git docs/temp docs/microsoft`, commit and push changes

## File Changes

```sh

git diff blotterLibrary\myfile.ps1        # Show changes

```

## Delete File

```sh

git rm file1.js                         # Remove file

```
