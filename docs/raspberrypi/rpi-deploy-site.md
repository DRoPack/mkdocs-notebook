# Adding and Deploying a New Site Project on Raspberry Pi

## Goal

Deploy a new static web project (example: kids math facts game) to the Pi and serve it by hostname on the home network.

!!! info "Need SSH first?"
  Start with: [putty-ssh.md](putty-ssh.md)

## Naming Recommendation

- Use one hostname per project, e.g.:
  - `math.home`
  - `science.home`
  - `reading.home`

This keeps each project isolated and easy to manage.

## Deployment Workflow

- One-time prerequisite: move Pi-hole web service off port 80 (to 8080) so Nginx can bind to port 80.
- Create project folder on Pi.
- Upload project files from Windows.
- Add local DNS record in Pi-hole.
- Add Nginx site config.
- Enable site and reload Nginx.
- Validate from browser.

If Pi-hole is still on port 80, Nginx startup can fail with `bind() ... :80 failed`.

!!! warning "One-time prerequisite"
    Pi-hole must be moved off port 80 first, or Nginx will not start on port 80.

One-time prerequisite command:

```bash
sudo pihole-FTL --config webserver.port '8080o,[::]:8080o'
sudo systemctl restart pihole-FTL
```

## Create Web Root (Pi)

```bash
sudo mkdir -p /var/www/math.home
```

## Upload Files from Windows

=== "OpenSSH scp"
    Preferred if your SSH stack supports `scp`.

    Upload all files from a folder:

    ```powershell
    scp -O C:\path\to\project\* user@pi-host:/var/www/math.home/
    ```

    Upload specific files in sequence (`&&`):

    ```cmd
    scp -O "C:\path\to\project\index.html" user@pi-host:/var/www/math.home/ && scp -O "C:\path\to\project\styles.css" user@pi-host:/var/www/math.home/ && scp -O "C:\path\to\project\app.js" user@pi-host:/var/www/math.home/
    ```

    Upload an entire folder recursively:

    ```powershell
    scp -O -r C:\path\to\project\* user@pi-host:/var/www/math.home/
    ```

=== "PuTTY pscp"
    Use this path when working with PuTTY tools.

    Upload one file:

    ```cmd
    "%ProgramFiles%\PuTTY\pscp.exe" -scp "C:\path\to\project\file1" user@pi-host:/var/www/math.home/
    ```

    Upload multiple files with `&&`:

    ```cmd
    "%ProgramFiles%\PuTTY\pscp.exe" -scp "C:\path\to\project\index.html" user@pi-host:/var/www/math.home/ && "%ProgramFiles%\PuTTY\pscp.exe" -scp "C:\path\to\project\styles.css" user@pi-host:/var/www/math.home/
    ```

    Upload a whole folder recursively:

    ```cmd
    "%ProgramFiles%\PuTTY\pscp.exe" -scp -r "C:\path\to\project\*" user@pi-host:/var/www/math.home/
    ```

## Add Local DNS Record (Pi-hole UI)

- Settings > Local DNS > Local DNS Records
- Add:
  - Hostname: `math.home`
  - Address: `<pi-lan-ip>`

## Create Nginx Site

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name math.home;

    root /var/www/math.home;
    index math-facts.html;

    location / {
        try_files $uri $uri/ /math-facts.html;
    }
}
```

Save as:
`/etc/nginx/sites-available/math.home`

Use Nano to create/edit the site file, then paste the config:

```bash
sudo nano /etc/nginx/sites-available/math.home
```

In PuTTY, paste with right-click.

!!! tip "Nano quick-save"
    Save with `Ctrl+O`, press `Enter`, then exit with `Ctrl+X`.

Save and exit Nano:

- Save: `Ctrl+O`, then `Enter`
- Exit: `Ctrl+X`

## Enable and Reload

```bash
sudo ln -sf /etc/nginx/sites-available/math.home /etc/nginx/sites-enabled/math.home
sudo nginx -t
sudo systemctl reload nginx
```

## Validate

=== "From Pi"
    ```bash
    curl -I -H "Host: math.home" http://127.0.0.1
    sudo ss -tulpn | grep -E ':80|:8080'
    ```

=== "From client"
    - Open `http://math.home`

!!! success "Expected"
    Nginx on `:80`, Pi-hole FTL on `:8080`.

## Common Stumbling Blocks and Fixes

- **Site doesn’t load**
  - Check DNS record exists and points to correct LAN IP (CMD: `nslookup math.home`, `ping math.home`).
  - Flush DNS cache on client (CMD: `ipconfig /flushdns`).
  - Renew client IP/network lease if needed (CMD: `ipconfig /release` then `ipconfig /renew`).

- **NXDOMAIN from Pi-hole**
  - Re-check exact hostname spelling and IP in Local DNS (CMD: `nslookup math.home`).
  - On Windows, test with trailing dot to avoid DNS suffix/search-list interference (CMD: `nslookup math.home. <pi-lan-ip>`).
  - Avoid small IP typos (common root cause).

- **Browser timeout but server is healthy**
  - Test direct IP first to separate network vs DNS issues (browser: `http://<pi-lan-ip>`, CMD: `ping <pi-lan-ip>`, `tracert <pi-lan-ip>`).
  - Managed work laptops (enterprise policy/VPN) may return NXDOMAIN for local names even when Pi/DNS config is correct; fallback is direct IP.

!!! note "Work laptop caveat"
    Enterprise policy, VPN split DNS, or endpoint controls can override home DNS behavior.
    If hostname checks fail but Pi checks pass, use direct IP from the managed device.

- **Upload problems (`sftp-server` or `scp` errors)**
  - Use SCP legacy mode (`-O`) or PuTTY `pscp`.
  - Confirm server-side tools are installed/configured.

- **Nano paste/save confusion**
  - Paste in PuTTY with right-click.
  - Save with `Ctrl+O`, then `Enter`; exit with `Ctrl+X`.

## Quick Redeploy (Same Project)

When updating existing files:

- Upload changed files again (same destination).
- Hard-refresh browser cache (`Ctrl+F5`).
- No Nginx reload needed for static content-only edits.
