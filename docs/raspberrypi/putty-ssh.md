# PuTTY SSH Connection Quickstart for Raspberry Pi

## Goal

Connect from Windows to your Raspberry Pi over SSH using PuTTY, then verify shell access for setup and deploy tasks.

## What You Need

- Raspberry Pi powered on and connected to LAN
- Pi LAN IP address (example: 192.168.1.50)
- SSH username (example: `root` or your DietPi user)
- Password for that SSH user
- PuTTY installed on Windows

## Connect with PuTTY

1. Open PuTTY.
2. In Host Name (or IP address), enter your Pi LAN IP.
3. Leave Port as `22` and Connection type as SSH.
4. Optional: under Saved Sessions, enter a name like `dietpi-home` and click Save.
5. Click Open.
6. Accept host key prompt on first connection.
7. Log in with username, then password.

!!! tip "PuTTY copy/paste"
    Copy from Windows normally.
    Paste into PuTTY with right-click.

## Quick Verification Commands

Run after login:

```bash
hostname
whoami
ip -4 addr show
sudo ss -tulpn | grep -E ':22|:80|:8080'
```

## If Connection Fails

- Ping the Pi IP from Windows:
  - `ping <pi-lan-ip>`
- Verify SSH service on Pi (from local console if needed):
  - `sudo systemctl status ssh`
- Reboot Pi and retry:
  - `sudo reboot`

## File Transfer Caveat (DietPi/Dropbear)

Some DietPi installs use Dropbear, which can break default Windows SCP/SFTP behavior.
Use one of these options from Windows:

- OpenSSH legacy SCP mode:
  - `scp -O "C:\path\to\file" user@pi-host:/var/www/math.home/`
- PuTTY PSCP mode:
  - `"%ProgramFiles%\PuTTY\pscp.exe" -scp "C:\path\to\file" user@pi-host:/var/www/math.home/`

## Next Steps

- Base setup guide: [rpi-web-server-setup.md](rpi-webserver-setup.md)
- Project deploy guide: [rpi-deploy-site.md](rpi-deploy-site.md)
