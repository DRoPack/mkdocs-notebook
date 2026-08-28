# VS Code Remote SSH to Raspberry Pi

## Goal

Connect from Windows VS Code directly to your Raspberry Pi and edit files like local files.

## Prerequisites

- Raspberry Pi reachable on LAN
- OpenSSH running on the Pi
- Working SSH login in PuTTY or terminal
- VS Code desktop (not web)

## 1) Install the VS Code Extension

Install **Remote - SSH** (Microsoft).

Quick install from terminal:

```powershell
code --install-extension ms-vscode-remote.remote-ssh
```

If command palette options are missing, check the extension is installed and enabled, then reload VS Code.

## 2) Add SSH Host

In VS Code:

1. Press `Ctrl+Shift+P`
2. Run `Remote-SSH: Add New SSH Host...`
3. Enter:

```bash
ssh root@<pi-lan-ip>
```

4. Save to your SSH config (typically `C:\Users\<you>\.ssh\config`)

## 3) Connect to the Pi

1. Press `Ctrl+Shift+P`
2. Run `Remote-SSH: Connect to Host...`
3. Select your Pi host
4. When prompted for platform, choose **Linux**

## 4) Fix Host Key Changed Error (After SSH Server Switch)

If you switched from Dropbear to OpenSSH, the host key changes and VS Code may fail with `Host key verification failed`.

Run on Windows PowerShell:

```powershell
ssh-keygen -R <pi-lan-ip>
```

Reconnect and accept the new fingerprint.

Expected fingerprint from your migration example:
`SHA256:LjmTwuc+2XgjKswhENoJqhv/9aisDtuo8YJ3XFXSyi4`

## 5) Open the Web Root Folder

Use **File > Open Folder...** and open:

- `/var/www`
- or a specific site folder like `/var/www/web.home`

Common typo to avoid: use `/var/www` (three `w`), not `/var/wwww`.

## 6) If Login Fails with Access Denied

OpenSSH can block root/password login by default. If needed:

```bash
sudo tee /etc/ssh/sshd_config.d/99-local-login.conf > /dev/null <<'EOF'
PermitRootLogin yes
PasswordAuthentication yes
KbdInteractiveAuthentication no
EOF

sudo systemctl restart ssh
sudo systemctl status ssh --no-pager -l
```

!!! warning "Security note"
    Root password login is convenient but less secure.
    Prefer a normal user plus SSH keys for long-term use.

## 7) Quick Verification Commands

Run on the Pi:

```bash
systemctl status ssh --no-pager
ss -tulpn | grep ':22'
```

Run on Windows:

```powershell
ssh root@<pi-lan-ip>
```

If these succeed, VS Code Remote SSH should connect cleanly.
