# 📱 V2rayNG Setup Guide (Android)

V2rayNG is a powerful Android client for V2Ray proxy protocols. It's lightweight, fast, and offers advanced configuration options for experienced users.

## 📥 Download & Installation

### Official Sources

1. **GitHub Releases** (Recommended)
   - Visit [V2rayNG Releases](https://github.com/2dust/v2rayNG/releases)
   - Download the latest APK file
   - Look for `v2rayNG_x.x.x_arm64-v8a.apk` for most devices

2. **Google Play Store**
   - Search for "V2rayNG"
   - Install the official app by 2dust

### Installation Steps

1. **Enable Unknown Sources**
   - Go to Settings → Security → Unknown Sources
   - Enable installation from unknown sources

2. **Install APK**
   - Open the downloaded APK file
   - Tap "Install" when prompted
   - Wait for installation to complete

## 🚀 Quick Setup

### Method 1: Subscription Import

1. **Open V2rayNG**
   - Launch the app after installation

2. **Add Subscription**
   - Tap the **"+"** button (top-right corner)
   - Select **"Import config from URL"**

3. **Enter Subscription URL**
   ```
   https://raw.githubusercontent.com/your-repo/free-proxies/main/configs/v2ray.txt
   ```
   - Paste the URL in the text field
   - Tap **"OK"**

4. **Update Subscription**
   - Pull down on the server list to refresh
   - New servers should appear automatically

5. **Connect**
   - Select a server from the list
   - Tap the **V** button at the bottom to connect
   - Grant VPN permissions when prompted

### Method 2: QR Code Import

1. **Scan QR Code**
   - Tap **"+"** → **"Scan QR code"**
   - Point camera at the QR code
   - Configuration will be imported automatically

2. **Manual QR Code**
   - If you have a config string, generate QR code online
   - Use any QR code generator with your config URL

### Method 3: Manual Configuration

1. **Add Server Manually**
   - Tap **"+"** → **"Manually input Vmess"**

2. **Enter Server Details**
   ```
   Alias: Server Name
   Address: server.example.com
   Port: 443
   User ID: your-uuid-here
   Alter ID: 0
   Security: auto
   Network: ws
   Path: /vmess
   TLS: tls
   ```

3. **Save Configuration**
   - Tap the **"✓"** button to save
   - Server will appear in the list

## ⚙️ Configuration Settings

### Basic Settings

**Connection Mode**
- **Global**: Route all traffic through proxy
- **Bypass LAN**: Direct connection for local network
- **Bypass China**: Direct connection for Chinese sites

**Route Settings**
- **Proxy**: All traffic through proxy
- **Bypass LAN and mainland**: Smart routing
- **Bypass LAN**: Only local traffic direct

### Advanced Settings

**Core Settings**
```
V2Ray Core: Latest version
Enable Mux: Yes (for better performance)
Mux Concurrency: 8
```

**DNS Settings**
```
Remote DNS: 1.1.1.1
Domestic DNS: 119.29.29.29
DNS Port: 53
```

**Network Settings**
```
Allow insecure: No
Enable sniffing: Yes
Route only: No
```

## 🔧 Protocol Configuration

### VMess Configuration

**Basic VMess**
```json
{
  "v": "2",
  "ps": "Server Name",
  "add": "server.example.com",
  "port": "443",
  "id": "uuid-here",
  "aid": "0",
  "scy": "auto",
  "net": "tcp",
  "type": "none",
  "host": "",
  "path": "",
  "tls": "tls"
}
```

**VMess over WebSocket**
```json
{
  "v": "2",
  "ps": "WS Server",
  "add": "server.example.com",
  "port": "443",
  "id": "uuid-here",
  "aid": "0",
  "scy": "auto",
  "net": "ws",
  "type": "none",
  "host": "server.example.com",
  "path": "/vmess",
  "tls": "tls"
}
```

### VLESS Configuration

**VLESS with Reality**
```
vless://uuid@server.example.com:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.microsoft.com&fp=chrome&pbk=public-key&sid=short-id&type=tcp&headerType=none#Reality-Server
```

### Shadowsocks Configuration

**SS with Plugin**
```
ss://method:password@server:port/?plugin=v2ray-plugin%3Bserver%3Btls%3Bhost%3Dserver.example.com#SS-Server
```

## 📊 Features & Tools

### Built-in Features

**Speed Test**
- Long press on any server
- Select "Test real delay"
- Results show in milliseconds

**Traffic Statistics**
- View upload/download statistics
- Monitor connection status
- Track data usage

**Log Viewer**
- Access detailed connection logs
- Debug connection issues
- Export logs for analysis

### Subscription Management

**Auto Update**
- Set automatic update intervals
- Manual refresh by pulling down
- Update all subscriptions at once

**Subscription Settings**
- Edit subscription URLs
- Enable/disable specific subscriptions
- Delete unused subscriptions

## 🛠️ Troubleshooting

### Common Issues

**❌ "Connection failed"**

**Solutions:**
1. Check server status
2. Try different servers
3. Update subscription
4. Restart the app

**❌ "No internet after connecting"**

**Solutions:**
1. Change routing mode
2. Check DNS settings
3. Try different protocols
4. Clear app data

**❌ "App crashes on startup"**

**Solutions:**
1. Update to latest version
2. Clear app cache and data
3. Reinstall the app
4. Check Android version compatibility

### Advanced Troubleshooting

**Debug Mode**
1. Go to Settings → Advanced
2. Enable "Debug mode"
3. Check logs for detailed errors

**Network Testing**
```bash
# Test server connectivity
ping server.example.com

# Check specific port
nc -zv server.example.com 443

# DNS resolution
nslookup server.example.com
```

**Configuration Validation**
1. Export configuration
2. Validate JSON format
3. Check all required fields
4. Test with V2Ray core directly

## 🔒 Security Configuration

### Recommended Security Settings

**TLS Settings**
- Always use TLS when available
- Verify server certificates
- Use SNI for domain fronting

**DNS Security**
- Use secure DNS servers
- Enable DNS over HTTPS
- Block malicious domains

**Traffic Obfuscation**
- Use WebSocket transport
- Enable path obfuscation
- Add custom headers

### Privacy Protection

**Kill Switch**
- Enable "Block connections without VPN"
- Test by disconnecting manually
- Ensure no traffic leaks

**DNS Leak Prevention**
```
Remote DNS: 1.1.1.1
Domestic DNS: 119.29.29.29
Enable DNS routing: Yes
```

**WebRTC Protection**
- Disable WebRTC in browsers
- Use WebRTC leak test tools
- Configure browser extensions

## 📱 Android-Specific Tips

### Battery Optimization

**Disable Battery Optimization**
1. Settings → Apps → V2rayNG
2. Battery → Battery Optimization
3. Select "Don't optimize"

**Background Activity**
- Allow background activity
- Enable "Start on boot"
- Keep app in recent apps

### Permissions

**Required Permissions**
- VPN service permission
- Network access
- Storage access (for configs)

**Optional Permissions**
- Camera (for QR codes)
- Location (for server selection)

### Split Tunneling

**App-based Routing**
1. Go to Settings → Route Setting
2. Enable "App proxy"
3. Select apps to proxy
4. Save settings

**Domain-based Routing**
1. Create custom routing rules
2. Add domain patterns
3. Set routing actions
4. Test configuration

## 🔄 Backup & Restore

### Export Configuration

1. **Full Backup**
   - Settings → Import/Export
   - Export all configurations
   - Save to secure location

2. **Individual Servers**
   - Long press on server
   - Select "Share config"
   - Copy or share configuration

### Import Configuration

1. **From Backup**
   - Settings → Import/Export
   - Select backup file
   - Import configurations

2. **From Clipboard**
   - Copy configuration URL
   - Open V2rayNG
   - Tap "Import from clipboard"

## 🆘 Getting Help

### Official Resources

1. **GitHub Repository**
   - [V2rayNG Issues](https://github.com/2dust/v2rayNG/issues)
   - Check existing issues first
   - Create new issue with details

2. **Documentation**
   - [V2Ray Official Docs](https://www.v2ray.com/)
   - [V2rayNG Wiki](https://github.com/2dust/v2rayNG/wiki)

### Community Support

1. **Telegram Groups**
   - Search for V2rayNG groups
   - Ask questions respectfully
   - Share solutions with others

2. **Reddit Communities**
   - r/dumbclub
   - r/VPN
   - Search for existing solutions

### Before Asking for Help

1. **Update to latest version**
2. **Check GitHub issues**
3. **Try different servers**
4. **Test basic connectivity**
5. **Gather error logs**

---

🎉 **Congratulations!** V2rayNG is now configured and ready to use. Remember to keep the app updated and test different servers for optimal performance.