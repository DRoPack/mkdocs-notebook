<!-- markdownlint-disable MD046 -->

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

## Squash (WIP)

!!! tip "Why use WIP commits?"

    WIP commits let you safely checkpoint unfinished work.
    You can clean them up later using interactive rebase.

!!! warning

    Only rewrite local commits. If already pushed, git push --force is required.

```sh title="Combine Adjacent Commits"
git rebase -i HEAD~2               # Rewrite last 2 commits

pick a1a1a1 WIP: updating file1
squash b2b2b2 WIP: updating file2  # Squash second commit into first
```

```sh title="Combine Non-Adjacent Commits"
# Reorder commits - must be in sequential order
git rebase -i HEAD~3               # Reorder and rewrite 2 commits

pick a1a1a1 WIP: updating file1    # Commit 1
squash c3c3c3 WIP: updating file3  # Commit 3
pick b2b2b2                        # Commit 2
```

Verify clean history:

```sh
git log --oneline
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

!!! tip "Most Common Workflow"
    Create feature branch → commit changes → push feature branch → switch to main/master → pull latest → merge feature branch → push main/master → delete branch.

```sh title="Inspect Branches"
git branch                           # List local branches
git branch -a                        # List local and remote branches

git status                           # Show current branch and working tree status
```
```sh title="Create and Switch Branches"
git switch -c feature/my-change      # Create and switch to a new branch

git switch <branch-name>             # Switch to an existing branch
```
```sh title="Commit Changes on Feature Branch"
git status                           # Verify changed files

git add .                            # Stage all changes
git commit -m "Chore: Description"   # Commit using preferred prefix style
```
```sh title="Push Feature Branch"
git push -u origin feature/my-change # First push; creates upstream tracking

git push                             # Push future commits to the same branch
```
```sh title="Merge Feature Branch into Main or Master"
# IMPORTANT:
# You merge INTO the branch you are currently on.
# Switch to main/master first, then merge the feature branch.

git switch main                      # Or use: git switch master
git pull                             # Get latest changes from remote

git merge feature/my-change          # Merge feature branch into current branch

git push                             # Push updated main/master to remote
```

??? success "Merge Message - Fast-Forward"

    If Git displays:

    ```text
    Fast-forward
    ```

    this is normal.

    It means no new commits were made on `main` since the feature branch was created, so Git simply moved the `main` pointer forward to the latest commit.

    No merge conflict occurred and no merge commit was required.

??? failure "Merge Message - Conflicts"
    
    If Git cannot automatically merge changes, you'll see a message similar to:

    ```text
    CONFLICT (content): Merge conflict in filename
    Automatic merge failed; fix conflicts and then commit the result.
    ```

    You are still on the branch where the merge was initiated
    (typically `main`).

    Steps:

    1. Open the conflicted file.
    2. Locate the conflict markers:

        ```text
        <<<<<<< HEAD
        Current branch content
        =======
        Incoming branch content
        >>>>>>> feature/my-branch
        ```

    3. Keep the desired code.
    4. Remove the conflict markers.
    5. Save the file.
    6. Stage the resolved file:

        ```bash
        git add filename
        ```

    7. Complete the merge:

        ```bash
        git commit
        ```
    No additional `git merge` command is required.


```sh title="Verify Merge"
git status                           # Confirm branch is up to date and clean

git log --oneline                    # Confirm recent commits are present
```

```sh title="Delete Branches After Merge"
git branch -d feature/my-change      # Delete local branch if Git confirms it is merged

git branch -D feature/my-change      # Force delete local branch after verifying merge

git push origin --delete feature/my-change  # Delete remote branch from GitHub
```

??? warning "When git branch -d refuses to delete"
    Sometimes Git refuses to delete a local branch even after it was merged into main/master.
    This can happen when Git is comparing the local branch to the remote feature branch instead of main/master.

    If all of the following are true:

    1. The feature branch was merged into main/master.
    2. main/master was pushed to GitHub.
    3. GitHub shows the expected commits.
    4. git status shows a clean working tree.

```sh title="Troubleshooting"
git diff                             # View unstaged changes

git diff -- <file-path>              # View changes for a specific file

git restore <file>                   # Discard local changes to a file

git log --oneline --graph --all      # Visualize branch history
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

## Create Git Ignore

```sh

touch .gitignore
echo JSFile1.txt > .gitignore           # Add file to .gitignore
echo JSFile2 >> .gitignore              # Append file to .gitignore
echo temp/ > .gitignore                 # Add folder to .gitignore

```

!!! tip

    Can't create .gitignore file: Ensure file is UTF-8 encoded - Files not removed from untracked once added to .gitignore: Ensure correct encoding - Using echo in PowerShell terminal causes issue: Use Bash terminal or PowerShell cmdlet for adding content

## Rename/Move

```sh

git mv file1.js file2.txt               # Rename or move file
git docs/microsoft docs/tmp             # Rename folder

```

<!-- prettier-ignore-start -->
!!! tip
    GitHub is a case-sensitive environment.<br>

    If your local folder is named microsoft and the GitHub folder (Microsoft) doesn't match case, you need to rename it to something different and then back.<br>

    For example:<br>
    `git docs/microsoft docs/tmp`, commit and push changes<br>
    `git docs/temp docs/microsoft`, commit and push changes
<!-- prettier-ignore-end -->

## File Changes

```sh

git diff blotterLibrary\myfile.ps1        # Show changes

```

## Delete File

```sh

git rm file1.js                         # Remove file

```
