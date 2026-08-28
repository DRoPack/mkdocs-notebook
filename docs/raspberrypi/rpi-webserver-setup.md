# Raspberry Pi + Pi-hole + Nginx (LAN Web Server) Setup

## Goal

Set up an IIS-like web hosting flow on a Raspberry Pi already running Pi-hole, using Nginx for serving local sites on a home network.

!!! info "Need SSH first?"
  Start with: [putty-ssh.md](putty-ssh.md)

!!! tip "Scope"
    This guide assumes LAN-only access and no public internet exposure.

## Environment (Sanitized)

- Raspberry Pi with DietPi
- Pi-hole already installed and active
- SSH access from Windows via PuTTY
- Home/LAN-only access (no public exposure required)

## What We Implemented

- Updated DietPi and rebooted.
- Installed Nginx.
- Resolved port conflict by moving Pi-hole web service off port 80 to port 8080.
- Started and enabled Nginx on port 80.
- Confirmed final state:
  - Nginx listening on `:80`
  - Pi-hole FTL listening on `:8080`
- Configured name-based virtual hosts (`web.home`, later `math.home`).

## Core Commands (Genericized)

!!! warning "Port 80 conflict prerequisite"
    Pi-hole must be moved off port 80 before Nginx can bind to `:80`.
    If not, Nginx can fail with `bind() to :80 failed`.

```bash
sudo dietpi-update
sudo apt update && sudo apt upgrade -y
sudo apt install -y nginx

# Move Pi-hole web server off :80
sudo pihole-FTL --config webserver.port '8080o,[::]:8080o'
sudo systemctl restart pihole-FTL

# Start nginx
sudo systemctl enable --now nginx
sudo systemctl status nginx --no-pager -l

# Check listeners
sudo ss -tulpn | grep -E ':80|:8080'
```

## Nginx Site Pattern Used

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name web.home;

    location / {
        root /var/www/web.home;
        index index.html;
    }

    location /admin/ {
        proxy_pass http://127.0.0.1:8080/admin/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

!!! note "Pi-hole admin URL after port change"
  After moving Pi-hole off port 80, direct Pi-hole admin is typically:
  `http://<pi-lan-ip>:8080/admin/`
  If using the Nginx proxy path, access it as:
  `http://web.home/admin/`

## Stumbling Blocks and Fixes

- **SSH timeout after update/reboot**
  - Cause: device IP/availability changed after reboot.
  - Fix: rediscover active LAN address and reconnect.

- **Nginx failed to start (`bind() to :80 failed`)**
  - Cause: Pi-hole still owned port 80.
  - Fix: move Pi-hole web port to 8080, restart Pi-hole FTL, then restart Nginx.

- **Service name typos (`ngix`/`system`)**
  - Cause: command typo.
  - Fix: use `systemctl` and `nginx` exactly.

- **Pi-hole CLI command mismatch**
  - Cause: version differences; older `pihole restartdns` style command unavailable.
  - Fix: restart `pihole-FTL` with `systemctl`.

- **Local DNS mistakes caused NXDOMAIN/timeouts**
  - Cause: incorrect A record IPs.
  - Fix: correct Local DNS entries and flush client DNS cache.
  - Windows CMD checks: `nslookup web.home`, `nslookup web.home. <pi-lan-ip>`, `ipconfig /flushdns`.

- **Work laptop DNS behavior differed**
  - Cause: enterprise endpoint/VPN policy effects.
  - Fix: managed devices can return NXDOMAIN for local names even when Pi/DNS is correct; validate from personal device and use direct IP from restricted endpoint when needed.

- **File transfer from Windows intermittently failed**
  - Cause: some DietPi installs use Dropbear, which can affect default SFTP/SCP behavior from Windows clients.
  - Fix: use `scp -O` (legacy mode) or PuTTY `pscp -scp`.

## Verification Checks

=== "Pi (SSH)"
    ```bash
    sudo nginx -t
    sudo systemctl status nginx --no-pager -l
    sudo ss -tulpn | grep -E ':80|:8080'
    curl -I -H "Host: web.home" http://127.0.0.1
    ```

=== "Windows (CMD)"
    ```cmd
    nslookup web.home
    nslookup web.home. <pi-lan-ip>
    ping web.home
    ipconfig /flushdns
    ```

!!! success "Expected listener state"
    Nginx on `:80`, Pi-hole FTL on `:8080`.

Post-reboot persistence check:

```bash
systemctl is-enabled nginx pihole-FTL
ss -tulpn | grep -E ':80|:8080'
```

## Windows Client Quick Checks

Run in Command Prompt (`cmd`) when local hostname access fails:

```cmd
nslookup web.home
nslookup web.home. <pi-lan-ip>
ping web.home
ipconfig /flushdns
```

Notes:

- `web.home.` (with trailing dot) bypasses DNS suffix/search-list interference.
- If corporate policy/VPN affects local DNS, test `http://<pi-lan-ip>` directly.

!!! note "Managed device caveat"
    Work-managed devices can return NXDOMAIN for local names even when Pi-hole and Nginx are configured correctly.
    If that happens, validate from a personal device and use direct IP as a fallback.

## Result

Local hosting is active with Nginx fronting custom sites on `:80`, while Pi-hole admin remains reachable behind Nginx via proxy path.
