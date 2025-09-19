# 📱 HiddifyVPN Setup Guide

HiddifyVPN is one of the most user-friendly proxy clients, perfect for beginners and advanced users alike. It supports all major proxy protocols and provides excellent performance.

## 📥 Download & Installation

### Android
1. **Google Play Store** (Recommended)
   - Search for "HiddifyVPN" or "Hiddify"
   - Install the official app by Hiddify Team

2. **Direct APK Download**
   - Visit [GitHub Releases](https://github.com/hiddify/hiddify-next/releases)
   - Download the latest APK file
   - Enable "Install from Unknown Sources" in Android settings
   - Install the APK

### iOS
1. **App Store**
   - Search for "Hiddify" in the App Store
   - Install the official app

2. **TestFlight** (Beta versions)
   - Join the beta program via the TestFlight link
   - Install the beta version for latest features

### Desktop (Windows/macOS/Linux)
1. Visit [GitHub Releases](https://github.com/hiddify/hiddify-next/releases)
2. Download the appropriate version for your OS
3. Install following standard procedures for your platform

## 🚀 Quick Setup

### Method 1: Subscription URL (Recommended)

1. **Open HiddifyVPN**
   - Launch the app after installation

2. **Add Profile**
   - Tap the **"+"** button (usually at the top-right)
   - Select **"Add Profile from URL"** or **"Subscription"**

3. **Enter Subscription URL**
   ```
   https://raw.githubusercontent.com/your-repo/free-proxies/main/configs/universal.txt
   ```
   - Paste the URL in the text field
   - Give it a name like "Free Proxies"
   - Tap **"Add"** or **"Save"**

4. **Update Profile**
   - The app will automatically fetch the server list
   - You should see multiple servers appear

5. **Connect**
   - Select a server from the list
   - Tap the **Connect** button
   - Grant VPN permissions when prompted

### Method 2: Manual Configuration

1. **Add Single Server**
   - Tap **"+"** → **"Add Profile Manually"**
   - Choose your protocol (VMess, Shadowsocks, etc.)

2. **Enter Server Details**
   - **Server Address**: Your server hostname/IP
   - **Port**: Server port number
   - **UUID/Password**: Authentication credentials
   - **Security**: Choose encryption method
   - **Network**: Select transport protocol

3. **Save and Connect**
   - Tap **"Save"**
   - Select the server and connect

## ⚙️ Configuration Options

### Basic Settings

**Connection Mode**
- **Global**: Route all traffic through proxy
- **Rule-based**: Use custom routing rules
- **Direct**: Bypass proxy for local traffic

**Protocol Selection**
- **Auto**: Let the app choose the best protocol
- **Manual**: Select specific protocol for each server

### Advanced Settings

**DNS Configuration**
```
Primary DNS: 1.1.1.1
Secondary DNS: 8.8.8.8
DNS over HTTPS: Enabled
```

**Routing Rules**
- **Bypass China**: Direct connection for Chinese websites
- **Block Ads**: Built-in ad blocking
- **Custom Rules**: Add your own routing rules

**Security Options**
- **Kill Switch**: Block internet if VPN disconnects
- **Auto-connect**: Connect automatically on app start
- **Start on Boot**: Launch app when device starts

## 🔧 Optimization Tips

### Speed Optimization

1. **Server Selection**
   - Use the built-in speed test feature
   - Choose servers with lowest ping
   - Try servers in nearby countries first

2. **Protocol Testing**
   - VMess: Good balance of speed and security
   - Shadowsocks: Usually fastest for streaming
   - Trojan: Most secure but may be slower

3. **Connection Settings**
   - Enable **TCP Fast Open** if available
   - Use **Mux** for multiple connections
   - Adjust **Buffer Size** for your network

### Battery Optimization

1. **Disable Battery Optimization**
   - Go to Android Settings → Apps → HiddifyVPN
   - Battery → Battery Optimization → Don't Optimize

2. **Background Activity**
   - Allow background activity for the app
   - Enable "Always-on VPN" in system VPN settings

## 📊 Features Overview

### Built-in Tools

**Speed Test**
- Test server response times
- Measure download/upload speeds
- Compare different servers

**Connection Monitor**
- Real-time traffic statistics
- Connection status indicators
- Network usage tracking

**Log Viewer**
- Debug connection issues
- Monitor proxy performance
- Export logs for troubleshooting

### Subscription Management

**Auto-update**
- Automatically refresh server lists
- Set update intervals (hourly, daily, weekly)
- Manual refresh option

**Multiple Subscriptions**
- Add multiple subscription URLs
- Organize servers by provider
- Enable/disable specific subscriptions

## 🛠️ Troubleshooting

### Common Issues

**❌ "Failed to connect"**
1. Check internet connection
2. Try a different server
3. Update subscription
4. Restart the app

**❌ "No internet after connecting"**
1. Check DNS settings
2. Try different protocol
3. Disable IPv6 if enabled
4. Clear app cache

**❌ "App keeps crashing"**
1. Update to latest version
2. Clear app data
3. Reinstall the app
4. Check device compatibility

### Advanced Troubleshooting

**Connection Logs**
1. Enable debug logging in settings
2. Reproduce the issue
3. Check logs for error messages
4. Share logs with support if needed

**Network Testing**
```bash
# Test server connectivity
ping server.example.com

# Check port accessibility
telnet server.example.com 443

# DNS resolution test
nslookup server.example.com
```

## 🔒 Security Best Practices

### Recommended Settings

**DNS Protection**
- Use secure DNS servers (1.1.1.1, 9.9.9.9)
- Enable DNS over HTTPS/TLS
- Block malicious domains

**Kill Switch**
- Always enable kill switch
- Test it by disconnecting manually
- Ensure no traffic leaks

**Auto-connect**
- Enable for untrusted networks
- Set trusted WiFi networks
- Use always-on VPN when possible

### Privacy Tips

1. **Regular Server Rotation**
   - Don't use the same server always
   - Change servers daily or weekly
   - Use different servers for different activities

2. **DNS Leak Testing**
   - Visit [dnsleaktest.com](https://dnsleaktest.com)
   - Ensure DNS queries go through proxy
   - Fix any detected leaks

3. **WebRTC Leak Prevention**
   - Disable WebRTC in browser settings
   - Use browser extensions to block WebRTC
   - Test at [browserleaks.com](https://browserleaks.com)

## 📱 Platform-Specific Tips

### Android

**Permissions**
- Grant VPN permission when prompted
- Allow background activity
- Disable battery optimization

**Split Tunneling**
- Choose which apps use the proxy
- Exclude local apps if needed
- Test app-specific routing

### iOS

**VPN Profile**
- Install VPN profile when prompted
- Trust the configuration profile
- Enable "Connect On Demand" if available

**Background Refresh**
- Enable background app refresh
- Allow cellular data usage
- Keep app in recent apps list

### Desktop

**System Proxy**
- Configure system-wide proxy settings
- Set browser proxy if needed
- Test with different applications

**Firewall Rules**
- Allow HiddifyVPN through firewall
- Configure port exceptions if needed
- Test connectivity after firewall changes

## 🆘 Getting Help

### Support Channels

1. **Official Documentation**
   - [Hiddify Wiki](https://github.com/hiddify/hiddify-config/wiki)
   - [GitHub Issues](https://github.com/hiddify/hiddify-next/issues)

2. **Community Support**
   - [Telegram Channel](https://t.me/hiddify)
   - [Discord Server](https://discord.gg/hiddify)

3. **Bug Reports**
   - Use GitHub Issues for bugs
   - Provide detailed information
   - Include logs and screenshots

### Before Asking for Help

1. **Check FAQ** in the app settings
2. **Update to latest version**
3. **Try different servers**
4. **Test with different protocols**
5. **Check network connectivity**

---

🎉 **You're all set!** HiddifyVPN is now configured and ready to protect your privacy. Remember to test your connection and adjust settings based on your needs.