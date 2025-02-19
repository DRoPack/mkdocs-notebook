# Git Commands Cheatsheet

## GitHub Basics

```sh
git init                                # Initialize git to local project

git clone https://github/repo           # Clone repo from GitHub to local machine
git add . || git add fileName.txt       # Add to staging, multiple files just add a space between files
git commit -m "Fixed bug…"              # Commit changes
git commit --amend                      # Amend commit message prior to push
git push                                # Push changes to GitHub
git pull --rebase                       # Update local with GitHub code

```

## Status

```sh

git status || git status -s             # Status
git log --oneline --all --graph         # Show linear graph of all local commits (q to exit)
git ls-files                            # Display all files being tracked in Git

```

## Stash

```sh

git stash push -m "Work in progress"   # Save uncommitted changes and add a message
git stash list                         # List all stashed changes
git stash apply stash@{2}              # Apply specific stash to the working directory (does not remove it)
git stash drop stash@{1}               # Delete a specific stash
git stash pop stash@{2}                # Apply specific stash and remove it from the stash list

git stash show stash@{1}               # Show a summary of changes in a specific stash
git stash show -p stash@{2}            # Show a detailed diff of changes in a specific stash

```

## Branching

```sh

git branch                              # List all branches in the repository
git branch <branch-name>                # Create a new branch

git switch <branch-name>                # Switch to an existing branch
git switch -c <branch-name>             # Create a new branch and switch to it

git branch -d <branch-name>             # Delete a branch (if it's fully merged)
git branch -D <branch-name>             # Force delete a branch (even if it's not merged)

git merge <branch-name>                 # Merge a branch into the current branch
git rebase <branch-name>                # Rebase the current branch onto another branch

git pull origin <branch-name>           # Pull changes from a specific branch on the remote
git push origin <branch-name>           # Push the branch to the remote repository
git push origin --delete <branch-name>  # Delete a branch from the remote repository

```

## Reset Local

```sh

git reset --hard                       # Discard all local changes (unstaged and staged)  
# Use if the local repo is out of sync with the remote after a rebase  

git reset --hard HEAD~1                # Undo the last commit and reset to the previous state  
git push origin --force                # Force push to remove the last commit from the remote  

git reflog                             # Show history of HEAD movements (useful for recovery)  
git reset --hard <commit-hash>         # Restore to a previous commit found in reflog  
```

## Staging Exclude Folder/File

```sh

git add . ":!docs/markdown/mkdocs-material.md"  # Excludes folder/file from from staging

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

# Initialize New Repository and Push to Github
1. Create a new repository on GitHub (without initializing it with README, .gitignore, etc..)
2. Run the following commands in your local project folder:
    git init                                # Initialize Git in local project
    git remote add origin <repository-url>  # Add remote repository url
    git add .                               # Add all files to staging
    git commit -m "Initial commit"          # Commit staged files
    git branch -M main                      # Rename the current branch to 'main' (force rename if necessary)
    git push -u origin main                 # Push the branch and commits to the remote repository
    git remote -v                           # Verify the remote connection

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
