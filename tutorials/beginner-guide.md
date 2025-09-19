# 🚀 Beginner's Guide to Free Proxy Configurations

Welcome! This guide will help you set up secure proxy connections to protect your internet privacy, even if you're completely new to proxies and VPNs.

## 📚 What You'll Learn

- What proxies are and why they're important
- How to choose the right proxy client
- Step-by-step setup instructions
- Basic troubleshooting

## 🤔 What is a Proxy?

A proxy is like a middleman between your device and the internet. Instead of connecting directly to websites, your traffic goes through the proxy server first. This helps:

- **Protect your privacy** - Websites can't see your real IP address
- **Bypass restrictions** - Access blocked content in your region
- **Secure your connection** - Encrypt your internet traffic

## 🎯 Choosing Your Client App

Different apps work better on different devices. Here are our top recommendations:

### 📱 For Mobile (Android/iOS)

**🥇 HiddifyVPN** (Recommended for beginners)
- ✅ Easy to use interface
- ✅ Supports all proxy types
- ✅ Built-in speed testing
- ✅ Free and open source

**🥈 V2rayNG** (Android only)
- ✅ Lightweight and fast
- ✅ Advanced features available
- ✅ Regular updates

### 💻 For Desktop (Windows/Mac/Linux)

**🥇 Sing-box** (Recommended)
- ✅ Cross-platform support
- ✅ Modern and efficient
- ✅ Excellent performance

**🥈 V2rayN** (Windows)
- ✅ User-friendly interface
- ✅ Comprehensive features

## 📲 Quick Setup Guide

### Method 1: HiddifyVPN (Easiest)

1. **Download the app**
   - Android: [Google Play Store](https://play.google.com/store/apps/details?id=app.hiddify.com)
   - iOS: [App Store](https://apps.apple.com/app/hiddify/id1596777532)

2. **Add proxy configuration**
   - Open HiddifyVPN
   - Tap the **"+"** button
   - Select **"Add Profile from URL"**
   - Paste this link:
     ```
     https://raw.githubusercontent.com/your-repo/free-proxies/main/configs/universal.txt
     ```
   - Tap **"Add"**

3. **Connect**
   - Select a server from the list
   - Tap the **Connect** button
   - Allow VPN permissions when prompted

4. **Test your connection**
   - Visit [whatismyipaddress.com](https://whatismyipaddress.com)
   - Your IP should be different from your real one

### Method 2: V2rayNG (Android)

1. **Download V2rayNG**
   - Get it from [GitHub Releases](https://github.com/2dust/v2rayNG/releases)
   - Install the APK file

2. **Import configuration**
   - Open V2rayNG
   - Tap **"+"** → **"Import config from URL"**
   - Paste:
     ```
     https://raw.githubusercontent.com/your-repo/free-proxies/main/configs/v2ray.txt
     ```
   - Tap **"OK"**

3. **Update and connect**
   - Pull down to refresh the server list
   - Select a server
   - Tap the **V** button to connect

## 🔧 Basic Settings

### Recommended Settings for Beginners

**Connection Mode**: Auto-select or Global
**DNS Settings**: Use proxy DNS (usually default)
**Kill Switch**: Enable if available
**Auto-connect**: Enable for convenience

### Speed Optimization

1. **Test server speeds**
   - Most apps have built-in speed testing
   - Choose servers with lowest ping

2. **Try different protocols**
   - VMess: Good balance of speed and security
   - Shadowsocks: Fastest, good for streaming
   - Trojan: Most secure, slightly slower

3. **Change servers if slow**
   - Different servers have different speeds
   - Try servers in nearby countries first

## 🛠️ Troubleshooting Common Issues

### ❌ "Can't connect to server"

**Solutions:**
1. Try a different server from the list
2. Check your internet connection
3. Update the subscription (pull to refresh)
4. Restart the app

### ❌ "Internet not working after connecting"

**Solutions:**
1. Check if the proxy is actually connected
2. Try changing DNS settings to 1.1.1.1 or 8.8.8.8
3. Disable and re-enable the connection
4. Try a different server

### ❌ "App keeps disconnecting"

**Solutions:**
1. Disable battery optimization for the app
2. Enable "Always-on VPN" in system settings
3. Try a more stable protocol (Trojan or VMess)
4. Check if your network blocks VPN traffic

### ❌ "Slow internet speed"

**Solutions:**
1. Test different servers - some are faster than others
2. Try different protocols (Shadowsocks is usually fastest)
3. Connect to servers closer to your location
4. Check if your ISP is throttling VPN traffic

## 🔒 Staying Safe

### ✅ Do's

- **Always use HTTPS websites** when possible
- **Keep your proxy app updated** for security patches
- **Use different servers regularly** to avoid detection
- **Test for DNS leaks** at [dnsleaktest.com](https://dnsleaktest.com)

### ❌ Don'ts

- **Don't use for illegal activities** - respect local laws
- **Don't trust free proxies with sensitive data** - use for general browsing only
- **Don't keep logs** - clear browser history regularly
- **Don't use the same server for everything** - rotate servers

## 📊 Understanding Server Information

When you see server lists, here's what the information means:

- **Country/City**: Physical location of the server
- **Ping**: Response time (lower is better, under 100ms is good)
- **Protocol**: Type of proxy (VMess, Shadowsocks, etc.)
- **Load**: How busy the server is (lower is better)

## 🆘 Getting Help

If you're still having trouble:

1. **Check our FAQ** in the docs folder
2. **Read the troubleshooting guide** for advanced solutions
3. **Join our community** on Telegram for real-time help
4. **Report issues** on GitHub if you find bugs

## 🎓 Next Steps

Once you're comfortable with the basics:

1. **Read the Advanced Guide** to learn about custom configurations
2. **Explore different protocols** to find what works best for you
3. **Learn about security features** like kill switches and DNS protection
4. **Consider setting up your own proxy server** for maximum privacy

## 📝 Quick Reference

### Essential Links
- Universal subscription: `https://raw.githubusercontent.com/your-repo/free-proxies/main/configs/universal.txt`
- V2ray subscription: `https://raw.githubusercontent.com/your-repo/free-proxies/main/configs/v2ray.txt`
- Shadowsocks subscription: `https://raw.githubusercontent.com/your-repo/free-proxies/main/configs/shadowsocks.txt`

### Best Apps for Beginners
- **Mobile**: HiddifyVPN
- **Desktop**: Sing-box or V2rayN

### Quick Test Sites
- IP check: [whatismyipaddress.com](https://whatismyipaddress.com)
- DNS leak test: [dnsleaktest.com](https://dnsleaktest.com)
- Speed test: [speedtest.net](https://speedtest.net)

---

🎉 **Congratulations!** You now know how to set up and use proxy configurations safely. Remember to always respect local laws and use these tools responsibly for protecting your privacy online.