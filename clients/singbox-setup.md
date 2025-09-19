# 🚀 Sing-box Setup Guide

Sing-box is a modern, high-performance proxy platform that supports multiple protocols and advanced routing features. It's perfect for users who want cutting-edge technology and maximum flexibility.

## 📥 Download & Installation

### Desktop Installation

**Windows**
1. Visit [Sing-box Releases](https://github.com/SagerNet/sing-box/releases)
2. Download `sing-box-x.x.x-windows-amd64.zip`
3. Extract to `C:\Program Files\sing-box\`
4. Add to PATH environment variable

**macOS**
```bash
# Using Homebrew
brew install sing-box

# Or download binary
curl -Lo sing-box.tar.gz https://github.com/SagerNet/sing-box/releases/latest/download/sing-box-x.x.x-darwin-amd64.tar.gz
tar -xzf sing-box.tar.gz
sudo mv sing-box /usr/local/bin/
```

**Linux**
```bash
# Ubuntu/Debian
curl -fsSL https://sing-box.sagernet.org/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/sagernet.gpg
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/sagernet.gpg] https://deb.sagernet.org/ * *" | sudo tee /etc/apt/sources.list.d/sagernet.list
sudo apt update
sudo apt install sing-box

# Manual installation
wget https://github.com/SagerNet/sing-box/releases/latest/download/sing-box-x.x.x-linux-amd64.tar.gz
tar -xzf sing-box-x.x.x-linux-amd64.tar.gz
sudo mv sing-box /usr/local/bin/
```

### Mobile Apps

**Android**
- [SFA (Sing-box for Android)](https://github.com/SagerNet/sing-box-for-android/releases)
- Download and install the APK

**iOS**
- [SFI (Sing-box for iOS)](https://apps.apple.com/app/sfi/id6451272673)
- Available on the App Store

## 🚀 Quick Setup

### Method 1: Using Our Configuration

1. **Download Configuration**
   ```bash
   curl -o config.json https://raw.githubusercontent.com/your-repo/free-proxies/main/configs/singbox.json
   ```

2. **Start Sing-box**
   ```bash
   sing-box run -c config.json
   ```

3. **Configure System Proxy**
   - Set HTTP proxy to `127.0.0.1:1080`
   - Set SOCKS proxy to `127.0.0.1:1080`

### Method 2: Custom Configuration

1. **Create Configuration File**
   ```bash
   mkdir -p ~/.config/sing-box
   nano ~/.config/sing-box/config.json
   ```

2. **Basic Configuration**
   ```json
   {
     "log": {
       "level": "info",
       "timestamp": true
     },
     "inbounds": [
       {
         "type": "mixed",
         "listen": "127.0.0.1",
         "listen_port": 1080,
         "sniff": true,
         "sniff_override_destination": true
       }
     ],
     "outbounds": [
       {
         "tag": "proxy",
         "type": "vmess",
         "server": "server.example.com",
         "server_port": 443,
         "uuid": "your-uuid-here",
         "security": "auto",
         "alter_id": 0,
         "transport": {
           "type": "ws",
           "path": "/vmess",
           "headers": {
             "Host": "server.example.com"
           }
         },
         "tls": {
           "enabled": true,
           "server_name": "server.example.com"
         }
       },
       {
         "tag": "direct",
         "type": "direct"
       },
       {
         "tag": "block",
         "type": "block"
       }
     ],
     "route": {
       "final": "proxy"
     }
   }
   ```

3. **Run Sing-box**
   ```bash
   sing-box run -c ~/.config/sing-box/config.json
   ```

## ⚙️ Advanced Configuration

### Multiple Outbounds

```json
{
  "outbounds": [
    {
      "tag": "vmess-us",
      "type": "vmess",
      "server": "us.example.com",
      "server_port": 443,
      "uuid": "uuid-1",
      "transport": {
        "type": "ws",
        "path": "/vmess"
      },
      "tls": {
        "enabled": true,
        "server_name": "us.example.com"
      }
    },
    {
      "tag": "ss-uk",
      "type": "shadowsocks",
      "server": "uk.example.com",
      "server_port": 8388,
      "method": "chacha20-ietf-poly1305",
      "password": "your-password"
    },
    {
      "tag": "trojan-jp",
      "type": "trojan",
      "server": "jp.example.com",
      "server_port": 443,
      "password": "your-password",
      "tls": {
        "enabled": true,
        "server_name": "jp.example.com"
      }
    }
  ]
}
```

### Smart Routing

```json
{
  "route": {
    "geoip": {
      "download_url": "https://github.com/SagerNet/sing-geoip/releases/latest/download/geoip.db",
      "download_detour": "direct"
    },
    "geosite": {
      "download_url": "https://github.com/SagerNet/sing-geosite/releases/latest/download/geosite.db",
      "download_detour": "direct"
    },
    "rules": [
      {
        "protocol": "dns",
        "outbound": "dns-out"
      },
      {
        "geosite": "cn",
        "geoip": "cn",
        "outbound": "direct"
      },
      {
        "geosite": ["google", "youtube", "facebook"],
        "outbound": "vmess-us"
      },
      {
        "geosite": "netflix",
        "outbound": "ss-uk"
      },
      {
        "domain_suffix": [".torrent", ".p2p"],
        "outbound": "block"
      }
    ],
    "final": "vmess-us",
    "auto_detect_interface": true
  }
}
```

### DNS Configuration

```json
{
  "dns": {
    "servers": [
      {
        "tag": "cloudflare",
        "address": "https://1.1.1.1/dns-query",
        "detour": "direct"
      },
      {
        "tag": "google",
        "address": "tls://8.8.8.8",
        "detour": "proxy"
      },
      {
        "tag": "local",
        "address": "local",
        "detour": "direct"
      }
    ],
    "rules": [
      {
        "geosite": "cn",
        "server": "local"
      },
      {
        "query_type": ["A", "AAAA"],
        "server": "cloudflare"
      }
    ],
    "final": "google",
    "strategy": "prefer_ipv4",
    "disable_cache": false,
    "disable_expire": false
  }
}
```

## 🔧 Protocol-Specific Configurations

### VMess Configuration

```json
{
  "type": "vmess",
  "server": "server.example.com",
  "server_port": 443,
  "uuid": "your-uuid-here",
  "security": "auto",
  "alter_id": 0,
  "global_padding": false,
  "authenticated_length": true,
  "transport": {
    "type": "ws",
    "path": "/vmess",
    "headers": {
      "Host": "server.example.com"
    },
    "max_early_data": 2048,
    "early_data_header_name": "Sec-WebSocket-Protocol"
  },
  "tls": {
    "enabled": true,
    "server_name": "server.example.com",
    "alpn": ["h2", "http/1.1"],
    "min_version": "1.2",
    "max_version": "1.3"
  }
}
```

### VLESS with Reality

```json
{
  "type": "vless",
  "server": "server.example.com",
  "server_port": 443,
  "uuid": "your-uuid-here",
  "flow": "xtls-rprx-vision",
  "tls": {
    "enabled": true,
    "server_name": "www.microsoft.com",
    "utls": {
      "enabled": true,
      "fingerprint": "chrome"
    },
    "reality": {
      "enabled": true,
      "public_key": "your-public-key",
      "short_id": "your-short-id"
    }
  }
}
```

### Hysteria Configuration

```json
{
  "type": "hysteria",
  "server": "server.example.com",
  "server_port": 443,
  "up_mbps": 100,
  "down_mbps": 100,
  "obfs": "your-obfs-password",
  "auth_str": "your-auth-string",
  "tls": {
    "enabled": true,
    "server_name": "server.example.com",
    "alpn": ["h3"]
  }
}
```

### TUIC Configuration

```json
{
  "type": "tuic",
  "server": "server.example.com",
  "server_port": 443,
  "uuid": "your-uuid-here",
  "password": "your-password",
  "congestion_control": "bbr",
  "udp_relay_mode": "native",
  "zero_rtt_handshake": false,
  "heartbeat": "10s",
  "tls": {
    "enabled": true,
    "server_name": "server.example.com",
    "alpn": ["h3"]
  }
}
```

## 🛠️ Management & Monitoring

### Command Line Usage

**Basic Commands**
```bash
# Run with config file
sing-box run -c config.json

# Check configuration
sing-box check -c config.json

# Format configuration
sing-box format -c config.json

# Generate UUID
sing-box generate uuid

# Generate Reality keypair
sing-box generate reality-keypair
```

**Service Management**
```bash
# Install as system service (Linux)
sudo sing-box service install -c /etc/sing-box/config.json

# Start service
sudo sing-box service start

# Stop service
sudo sing-box service stop

# Uninstall service
sudo sing-box service uninstall
```

### Log Configuration

```json
{
  "log": {
    "disabled": false,
    "level": "info",
    "output": "/var/log/sing-box/sing-box.log",
    "timestamp": true
  }
}
```

### API Configuration

```json
{
  "experimental": {
    "clash_api": {
      "external_controller": "127.0.0.1:9090",
      "external_ui": "ui",
      "secret": "your-secret-key",
      "default_mode": "rule"
    }
  }
}
```

## 📊 Performance Optimization

### Connection Optimization

```json
{
  "outbounds": [
    {
      "type": "vmess",
      "server": "server.example.com",
      "server_port": 443,
      "uuid": "your-uuid-here",
      "multiplex": {
        "enabled": true,
        "protocol": "smux",
        "max_connections": 4,
        "min_streams": 4,
        "max_streams": 0
      }
    }
  ]
}
```

### System Optimization

**Linux Kernel Parameters**
```bash
# /etc/sysctl.conf
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 134217728
net.ipv4.tcp_wmem = 4096 65536 134217728
net.ipv4.tcp_congestion_control = bbr
```

**File Descriptor Limits**
```bash
# /etc/security/limits.conf
* soft nofile 65536
* hard nofile 65536
```

## 🔒 Security Configuration

### TLS Security

```json
{
  "tls": {
    "enabled": true,
    "server_name": "server.example.com",
    "alpn": ["h2", "http/1.1"],
    "min_version": "1.3",
    "max_version": "1.3",
    "cipher_suites": [
      "TLS_AES_256_GCM_SHA384",
      "TLS_CHACHA20_POLY1305_SHA256"
    ],
    "certificate_path": "/path/to/cert.pem",
    "key_path": "/path/to/key.pem"
  }
}
```

### Traffic Obfuscation

```json
{
  "transport": {
    "type": "http",
    "host": ["server.example.com"],
    "path": "/api/v1/data",
    "method": "POST",
    "headers": {
      "Content-Type": ["application/json"],
      "User-Agent": ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"]
    }
  }
}
```

## 🛠️ Troubleshooting

### Common Issues

**❌ "Configuration validation failed"**
```bash
# Check configuration syntax
sing-box check -c config.json

# Format configuration
sing-box format -c config.json -w
```

**❌ "Connection timeout"**
```bash
# Test server connectivity
ping server.example.com
nc -zv server.example.com 443

# Check DNS resolution
dig server.example.com
```

**❌ "TLS handshake failed"**
```bash
# Test TLS connection
openssl s_client -connect server.example.com:443 -servername server.example.com

# Check certificate
openssl s_client -connect server.example.com:443 -showcerts
```

### Debug Mode

```json
{
  "log": {
    "level": "debug",
    "timestamp": true
  }
}
```

### Network Testing

```bash
# Test proxy connectivity
curl -x socks5://127.0.0.1:1080 https://httpbin.org/ip

# Test HTTP proxy
curl -x http://127.0.0.1:1080 https://httpbin.org/ip

# Speed test
curl -x socks5://127.0.0.1:1080 -o /dev/null -s -w "%{speed_download}\n" https://speedtest.net/api/js/servers?engine=js
```

## 🔄 Automation & Scripts

### Auto-start Script (Linux)

```bash
#!/bin/bash
# /etc/systemd/system/sing-box.service

[Unit]
Description=sing-box service
Documentation=https://sing-box.sagernet.org
After=network.target nss-lookup.target

[Service]
User=sing-box
Group=sing-box
Type=simple
ExecStart=/usr/local/bin/sing-box run -c /etc/sing-box/config.json
ExecReload=/bin/kill -HUP $MAINPID
LimitNOFILE=infinity
LimitNPROC=infinity
LimitMEMLOCK=infinity
LimitCORE=infinity
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

### Configuration Update Script

```bash
#!/bin/bash
# update-config.sh

CONFIG_URL="https://raw.githubusercontent.com/your-repo/free-proxies/main/configs/singbox.json"
CONFIG_FILE="/etc/sing-box/config.json"
BACKUP_FILE="/etc/sing-box/config.json.backup"

# Backup current config
cp "$CONFIG_FILE" "$BACKUP_FILE"

# Download new config
curl -o "$CONFIG_FILE.new" "$CONFIG_URL"

# Validate new config
if sing-box check -c "$CONFIG_FILE.new"; then
    mv "$CONFIG_FILE.new" "$CONFIG_FILE"
    systemctl reload sing-box
    echo "Configuration updated successfully"
else
    rm "$CONFIG_FILE.new"
    echo "New configuration is invalid, keeping current config"
fi
```

## 🆘 Getting Help

### Official Resources

1. **Documentation**
   - [Sing-box Wiki](https://sing-box.sagernet.org/)
   - [Configuration Examples](https://github.com/SagerNet/sing-box/tree/main/docs/configuration)

2. **Community**
   - [GitHub Discussions](https://github.com/SagerNet/sing-box/discussions)
   - [Telegram Group](https://t.me/SagerNet)

### Before Asking for Help

1. **Check configuration syntax**
2. **Test with minimal config**
3. **Check server connectivity**
4. **Review debug logs**
5. **Search existing issues**

---

🎉 **Excellent!** Sing-box is now configured with advanced features. This modern proxy platform will provide you with excellent performance and security for all your privacy needs.