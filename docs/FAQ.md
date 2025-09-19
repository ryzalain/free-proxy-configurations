# ❓ Frequently Asked Questions (FAQ)

## 🚀 Getting Started

### Q: What is this project about?
**A:** This project provides automatically updated, secure proxy configurations for various VPN and proxy protocols. It helps users maintain their internet privacy by offering free, high-quality proxy servers with easy-to-use subscription links.

### Q: Is this really free?
**A:** Yes! This project is completely free and open-source. We believe internet privacy should be accessible to everyone. However, please consider supporting the project if you find it useful.

### Q: How do I get started?
**A:** 
1. Choose a proxy client (we recommend HiddifyVPN for beginners)
2. Copy the universal subscription link from our README
3. Add it to your proxy client
4. Connect and enjoy secure browsing!

### Q: Which proxy client should I use?
**A:** 
- **Beginners**: HiddifyVPN (mobile) or Sing-box (desktop)
- **Android**: V2rayNG or HiddifyVPN
- **iOS**: HiddifyVPN or Shadowrocket
- **Windows**: V2rayN or Sing-box
- **macOS**: ClashX or Sing-box
- **Linux**: Sing-box or command-line tools

## 🔧 Technical Questions

### Q: What protocols are supported?
**A:** We support all major proxy protocols:
- **VMess** - V2Ray's native protocol
- **VLESS** - Lightweight version of VMess
- **Shadowsocks** - Simple and fast SOCKS5 proxy
- **Trojan** - TLS-based proxy protocol
- **Hysteria** - QUIC-based high-performance proxy
- **TUIC** - Modern QUIC proxy protocol
- **Reality** - Advanced TLS camouflage
- **SSH** - Secure Shell tunneling

### Q: How often are configurations updated?
**A:** Configurations are automatically updated every 6 hours. This ensures you always have access to working servers with optimal performance.

### Q: Can I use these configurations on multiple devices?
**A:** Yes! You can use the same subscription link on multiple devices. However, avoid using the same server simultaneously on many devices as it may affect performance.

### Q: Are the configurations secure?
**A:** Yes, we implement security best practices:
- Strong encryption methods (ChaCha20-Poly1305, AES-256-GCM)
- TLS 1.3 where supported
- DNS leak protection
- Secure default configurations
- Regular security audits

## 🛠️ Setup and Configuration

### Q: The subscription link isn't working. What should I do?
**A:** Try these steps:
1. Check your internet connection
2. Verify the subscription URL is correct
3. Try updating/refreshing the subscription
4. Use a different subscription format (V2ray, Shadowsocks, etc.)
5. Check our troubleshooting guide

### Q: How do I know if my proxy is working?
**A:** 
1. Visit [whatismyipaddress.com](https://whatismyipaddress.com) - your IP should be different
2. Check for DNS leaks at [dnsleaktest.com](https://dnsleaktest.com)
3. Run our security test script: `python tests/security_test.py`

### Q: Can I add my own servers?
**A:** Yes! You can:
1. Fork the repository
2. Modify the server list in `scripts/proxy_generator.py`
3. Run the generator to create new configurations
4. Submit a pull request to share with others

### Q: How do I set up automatic updates?
**A:** 
- **Linux/macOS**: Run `python scripts/setup.py` to set up cron jobs
- **Windows**: Use Task Scheduler to run the updater script
- **Manual**: Run `python scripts/auto_updater.py --once` periodically

## 🔒 Security and Privacy

### Q: Can these proxies see my traffic?
**A:** Proxy servers can potentially see your traffic, which is why we:
- Use only encrypted protocols
- Recommend HTTPS websites
- Provide security testing tools
- Regularly rotate servers
- Don't log any user activity ourselves

### Q: Are these proxies safe for banking/sensitive activities?
**A:** While our configurations use strong encryption, we recommend:
- Using your regular connection for banking
- Only using proxies for general browsing
- Never entering sensitive information on HTTP sites
- Using additional security measures like 2FA

### Q: How do I test for security leaks?
**A:** Use our built-in security tester:
```bash
python tests/security_test.py
```
Or manually check:
- IP leak: [ipleak.net](https://ipleak.net)
- DNS leak: [dnsleaktest.com](https://dnsleaktest.com)
- WebRTC leak: [browserleaks.com](https://browserleaks.com)

### Q: What should I do if I detect a leak?
**A:** 
1. Disconnect the proxy immediately
2. Check your client configuration
3. Try a different server/protocol
4. Ensure kill switch is enabled
5. Report the issue on our GitHub

## 🌍 Performance and Reliability

### Q: Why is my connection slow?
**A:** Several factors can affect speed:
- **Server load**: Try different servers
- **Distance**: Choose servers closer to your location
- **Protocol**: Shadowsocks is usually fastest
- **ISP throttling**: Try different ports/protocols
- **Network congestion**: Test at different times

### Q: Which protocol is fastest?
**A:** Generally:
1. **Shadowsocks** - Fastest, good for streaming
2. **VMess** - Good balance of speed and security
3. **Hysteria** - Excellent for high-latency connections
4. **Trojan** - Secure but may be slower
5. **Reality** - Most secure but potentially slower

### Q: Some servers don't work. Is this normal?
**A:** Yes, this is normal for free proxy services:
- Servers may go offline
- Some ISPs block certain IPs
- Geographic restrictions may apply
- Try different servers from the list
- Update your subscription regularly

### Q: Can I use these for streaming?
**A:** You can try, but:
- Performance varies by server and location
- Some streaming services actively block proxies
- Use servers in the same region as the content
- Shadowsocks protocol often works best for streaming

## 📱 Platform-Specific Questions

### Q: Why won't the VPN connect on my iPhone?
**A:** Common iOS issues:
1. Trust the configuration profile in Settings
2. Enable "Connect On Demand" if available
3. Restart the device
4. Check for iOS updates
5. Try a different server

### Q: Android app keeps disconnecting. How to fix?
**A:** 
1. Disable battery optimization for the proxy app
2. Enable "Always-on VPN" in system settings
3. Add app to auto-start list
4. Check for conflicting VPN apps
5. Try different servers

### Q: How do I set up on Linux command line?
**A:** 
1. Install Sing-box: `curl -fsSL https://sing-box.sagernet.org/install.sh | bash`
2. Download config: `curl -o config.json [subscription-url]`
3. Run: `sing-box run -c config.json`
4. Set system proxy to `127.0.0.1:1080`

## 🤝 Contributing and Support

### Q: How can I contribute to this project?
**A:** Many ways to help:
- **Report bugs** and issues
- **Test configurations** on different platforms
- **Improve documentation** and tutorials
- **Add new protocols** or features
- **Translate** documentation to other languages
- **Share** the project with others

### Q: I found a bug. How do I report it?
**A:** 
1. Check existing issues on GitHub first
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Your system information
   - Configuration details (remove sensitive data)
   - Error logs if available

### Q: Can I request new features?
**A:** Absolutely! Create a feature request on GitHub with:
- Clear description of the feature
- Use case and benefits
- Any relevant technical details
- Examples from other projects if applicable

### Q: How do I get help with setup?
**A:** 
1. **Read the documentation** - most questions are answered there
2. **Check the troubleshooting guide** for common issues
3. **Search GitHub issues** for similar problems
4. **Join our community** on Telegram/Discord
5. **Create an issue** if you can't find a solution

## 🔄 Updates and Maintenance

### Q: How do I update my configurations?
**A:** 
- **Automatic**: Most clients update subscriptions automatically
- **Manual**: Pull down to refresh in your proxy app
- **Command line**: Re-run the generator script

### Q: What happens if the project stops being maintained?
**A:** 
- All code is open-source, so anyone can fork and continue
- Configurations will continue working until servers go offline
- You can run your own instance using our code
- We'll provide advance notice if we plan to discontinue

### Q: Can I run my own instance of this system?
**A:** Yes! The entire system is open-source:
1. Fork the repository
2. Modify server sources and configurations
3. Set up your own update schedule
4. Deploy to your own infrastructure

## 📊 Statistics and Monitoring

### Q: How many servers are available?
**A:** The number varies as we continuously update our server list. Check the status file in the configs directory for current statistics.

### Q: How can I monitor server status?
**A:** 
- Check `configs/status.json` for update information
- Use our validation script: `python tests/config_validator.py`
- Monitor GitHub Actions for update status
- Join our community channels for announcements

### Q: Are there usage statistics available?
**A:** We don't collect user statistics for privacy reasons. However, we do track:
- Server availability and performance
- Configuration update success rates
- GitHub repository statistics

## ⚖️ Legal and Compliance

### Q: Is using these proxies legal?
**A:** Proxy usage legality varies by jurisdiction:
- Generally legal in most countries for privacy
- May be restricted in some regions
- Always comply with local laws and regulations
- Use responsibly and ethically

### Q: What's your privacy policy?
**A:** 
- We don't collect or store user data
- No logging of user activities
- Open-source code for transparency
- Configurations are publicly available
- We recommend reading server providers' policies

### Q: Can I use this for commercial purposes?
**A:** The code is MIT licensed, so yes, but:
- Respect the license terms
- Consider the server providers' terms of service
- Don't abuse the free servers
- Consider contributing back to the project

---

❓ **Still have questions?** 

- 📖 Check our [documentation](../docs/)
- 🐛 [Report issues](https://github.com/your-repo/free-proxies/issues) on GitHub
- 💬 Join our [community discussions](https://github.com/your-repo/free-proxies/discussions)
- 📧 Contact us through GitHub

We're here to help make internet privacy accessible to everyone! 🔒