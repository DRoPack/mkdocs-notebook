# CMD Reference

---

## Environment Variables

```cmd
// Get all environment variables
set

// Set a variable
set Folder=MyNewFolder
mkdir %Folder%
```

---

## File and Directory Management

### Paths

```cmd
// Change path
cd Users\blotter\Downloads

// Change path (up 1 level)
cd ..
```

### Directory Operations

```cmd
// View directory contents
dir

// Make a directory
mkdir MyFolder

// Make and move to a directory
mkdir MyFolder && cd MyFolder
```

### File Operations

```cmd
// Create a file
echo "My Content" > file.txt

// Remove a file
del file.txt
```

---

## System Commands

```cmd
// Open Group Policy Editor
gpedit.msc

// Shutdown system immediately
shutdown -r -t 0

// Open File Explorer in current path
start .
```
