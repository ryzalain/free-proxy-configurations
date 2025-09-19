# 🛠️ Troubleshooting Guide

This comprehensive guide helps you diagnose and fix common issues with proxy configurations.

## 🚨 Quick Fixes

### Most Common Issues

**❌ "Can't connect to proxy server"**
```bash
# Quick diagnosis
ping server.example.com
nc -zv server.example.com 443
curl -I https://server.example.com
```

**❌ "Connected but no internet"**
```bash
# Check DNS resolution
nslookup google.com
dig @1.1.1.1 google.com

# Test proxy directly
curl -x socks5://127.0.0.1:1080 https://httpbin.org/ip
```

**❌ "Slow connection speed"**
```bash
# Speed test through proxy
curl -x socks5://127.0.0.1:1080 -o /dev/null -s -w "%{speed_download}\n" https://speedtest.net/api/js/servers
```

## 🔍 Diagnostic Tools

### Network Connectivity Tests

**Basic Connectivity**
```bash
#!/bin/bash
# connectivity-test.sh

SERVER="server.example.com"
PORT="443"

echo "🔍 Testing connectivity to $SERVER:$PORT"

# Test ping
if ping -c 3 "$SERVER" > /dev/null 2>&1; then
    echo "✅ Ping successful"
else
    echo "❌ Ping failed - server unreachable or ICMP blocked"
fi

# Test TCP connection
if nc -zv "$SERVER" "$PORT" 2>/dev/null; then
    echo "✅ TCP connection successful"
else
    echo "❌ TCP connection failed - port blocked or server down"
fi

# Test TLS handshake
if openssl s_client -connect "$SERVER:$PORT" -servername "$SERVER" < /dev/null 2>/dev/null | grep -q "Verify return code: 0"; then
    echo "✅ TLS handshake successful"
else
    echo "❌ TLS handshake failed - certificate or TLS issues"
fi
```

**DNS Resolution Test**
```bash
#!/bin/bash
# dns-test.sh

DOMAIN="google.com"

echo "🔍 Testing DNS resolution for $DOMAIN"

# Test system DNS
if nslookup "$DOMAIN" > /dev/null 2>&1; then
    echo "✅ System DNS working"
else
    echo "❌ System DNS failed"
fi

# Test specific DNS servers
DNS_SERVERS=("1.1.1.1" "8.8.8.8" "9.9.9.9")

for dns in "${DNS_SERVERS[@]}"; do
    if nslookup "$DOMAIN" "$dns" > /dev/null 2>&1; then
        echo "✅ DNS $dns working"
    else
        echo "❌ DNS $dns failed"
    fi
done
```

### Proxy-Specific Tests

**SOCKS Proxy Test**
```python
#!/usr/bin/env python3
import socket
import socks

def test_socks_proxy(host='127.0.0.1', port=1080):
    try:
        # Create SOCKS socket
        sock = socks.socksocket()
        sock.set_proxy(socks.SOCKS5, host, port)
        
        # Test connection
        sock.connect(('httpbin.org', 80))
        
        # Send HTTP request
        request = b"GET /ip HTTP/1.1\r\nHost: httpbin.org\r\n\r\n"
        sock.send(request)
        
        # Receive response
        response = sock.recv(4096)
        sock.close()
        
        if b"200 OK" in response:
            print("✅ SOCKS proxy working")
            return True
        else:
            print("❌ SOCKS proxy failed")
            return False
            
    except Exception as e:
        print(f"❌ SOCKS proxy error: {e}")
        return False

if __name__ == "__main__":
    test_socks_proxy()
```

**HTTP Proxy Test**
```bash
#!/bin/bash
# http-proxy-test.sh

PROXY="127.0.0.1:1080"

echo "🔍 Testing HTTP proxy at $PROXY"

# Test HTTP proxy
if curl -x "http://$PROXY" -s -o /dev/null -w "%{http_code}" https://httpbin.org/ip | grep -q "200"; then
    echo "✅ HTTP proxy working"
else
    echo "❌ HTTP proxy failed"
fi

# Test SOCKS proxy
if curl -x "socks5://$PROXY" -s -o /dev/null -w "%{http_code}" https://httpbin.org/ip | grep -q "200"; then
    echo "✅ SOCKS proxy working"
else
    echo "❌ SOCKS proxy failed"
fi
```

## 🐛 Common Problems & Solutions

### Connection Issues

**Problem: "Connection refused"**

**Causes:**
- Proxy server is down
- Wrong server address/port
- Firewall blocking connection
- ISP blocking proxy traffic

**Solutions:**
```bash
# Check server status
curl -I https://server.example.com

# Try different ports
for port in 443 80 8080 8443; do
    nc -zv server.example.com $port
done

# Check firewall
sudo iptables -L | grep -i drop
sudo ufw status

# Try different server
# Update your subscription or try manual config
```

**Problem: "Timeout errors"**

**Causes:**
- Network congestion
- Server overload
- ISP throttling
- Wrong timeout settings

**Solutions:**
```json
{
  "timeout": {
    "connect": "10s",
    "handshake": "10s",
    "idle": "300s"
  }
}
```

### Authentication Issues

**Problem: "Authentication failed"**

**Causes:**
- Wrong credentials
- Expired subscription
- Server configuration changed
- Clock synchronization issues

**Solutions:**
```bash
# Check system time
timedatectl status

# Sync time if needed
sudo ntpdate -s time.nist.gov

# Regenerate credentials
sing-box generate uuid

# Update subscription
curl -o config.json https://your-subscription-url
```

### DNS Issues

**Problem: "DNS resolution failed"**

**Causes:**
- DNS server unreachable
- DNS poisoning/hijacking
- Wrong DNS configuration
- IPv6/IPv4 conflicts

**Solutions:**
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
        "tag": "quad9",
        "address": "tls://9.9.9.9",
        "detour": "proxy"
      }
    ],
    "final": "cloudflare",
    "strategy": "prefer_ipv4"
  }
}
```

**Problem: "DNS leaks detected"**

**Solutions:**
```bash
# Test for DNS leaks
curl -x socks5://127.0.0.1:1080 https://dnsleaktest.com/

# Fix DNS configuration
# Ensure all DNS queries go through proxy
```

### Performance Issues

**Problem: "Slow connection speed"**

**Causes:**
- Server overload
- Wrong protocol choice
- Network congestion
- Suboptimal routing

**Solutions:**
```bash
# Test different servers
for server in us1 uk1 jp1; do
    echo "Testing $server..."
    curl -x socks5://127.0.0.1:1080 -o /dev/null -s -w "Speed: %{speed_download} bytes/sec\n" https://speedtest.net/api/js/servers
done

# Try different protocols
# VMess for balance, Shadowsocks for speed, Trojan for security
```

**Problem: "High latency"**

**Solutions:**
```json
{
  "mux": {
    "enabled": true,
    "concurrency": 8
  },
  "sockopt": {
    "tcpFastOpen": true,
    "tcpKeepAliveInterval": 30
  }
}
```

### TLS/SSL Issues

**Problem: "TLS handshake failed"**

**Causes:**
- Certificate issues
- TLS version mismatch
- SNI problems
- Clock synchronization

**Solutions:**
```bash
# Check certificate
openssl s_client -connect server.example.com:443 -servername server.example.com

# Test TLS versions
for version in tls1_2 tls1_3; do
    openssl s_client -connect server.example.com:443 -$version -servername server.example.com < /dev/null
done

# Check system time
date
```

**Problem: "Certificate verification failed"**

**Solutions:**
```json
{
  "tls": {
    "enabled": true,
    "server_name": "server.example.com",
    "insecure": false,
    "alpn": ["h2", "http/1.1"]
  }
}
```

## 🔧 Platform-Specific Issues

### Windows Issues

**Problem: "VPN service won't start"**

**Solutions:**
```cmd
# Run as administrator
net start "Windows VPN Service"

# Check Windows Defender
# Add proxy client to exclusions

# Reset network stack
netsh winsock reset
netsh int ip reset
```

**Problem: "Proxy settings not applied"**

**Solutions:**
```cmd
# Check proxy settings
netsh winhttp show proxy

# Set proxy manually
netsh winhttp set proxy proxy-server="127.0.0.1:1080"

# Reset proxy settings
netsh winhttp reset proxy
```

### macOS Issues

**Problem: "Permission denied"**

**Solutions:**
```bash
# Grant VPN permissions
sudo chmod +x /path/to/proxy-client

# Add to Security & Privacy
# System Preferences → Security & Privacy → VPN

# Reset network preferences
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

### Linux Issues

**Problem: "Systemd service fails"**

**Solutions:**
```bash
# Check service status
systemctl status proxy-service

# Check logs
journalctl -u proxy-service -f

# Fix permissions
sudo chown proxy:proxy /etc/proxy/config.json
sudo chmod 600 /etc/proxy/config.json

# Restart service
sudo systemctl restart proxy-service
```

**Problem: "iptables blocking traffic"**

**Solutions:**
```bash
# Check iptables rules
sudo iptables -L -n

# Allow proxy traffic
sudo iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -p tcp --sport 443 -j ACCEPT

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
```

### Android Issues

**Problem: "VPN won't connect"**

**Solutions:**
```
1. Check VPN permissions in Settings
2. Disable battery optimization for proxy app
3. Clear app cache and data
4. Restart device
5. Try different server/protocol
```

**Problem: "App keeps disconnecting"**

**Solutions:**
```
1. Enable "Always-on VPN" in system settings
2. Disable "Block connections without VPN"
3. Add app to battery optimization whitelist
4. Check for conflicting VPN apps
```

### iOS Issues

**Problem: "Profile installation failed"**

**Solutions:**
```
1. Go to Settings → General → VPN & Device Management
2. Trust the configuration profile
3. Enable "Connect On Demand" if available
4. Restart device if needed
```

## 🔍 Advanced Debugging

### Log Analysis

**Enable Debug Logging**
```json
{
  "log": {
    "level": "debug",
    "timestamp": true,
    "output": "/var/log/proxy/debug.log"
  }
}
```

**Log Analysis Script**
```bash
#!/bin/bash
# analyze-logs.sh

LOG_FILE="/var/log/proxy/debug.log"

echo "🔍 Analyzing proxy logs..."

# Count error types
echo "📊 Error Summary:"
grep -i error "$LOG_FILE" | cut -d' ' -f4- | sort | uniq -c | sort -nr

# Find connection failures
echo "📊 Connection Failures:"
grep -i "failed\|timeout\|refused" "$LOG_FILE" | tail -10

# Check TLS issues
echo "📊 TLS Issues:"
grep -i "tls\|ssl\|certificate" "$LOG_FILE" | tail -5

# Monitor recent activity
echo "📊 Recent Activity:"
tail -20 "$LOG_FILE"
```

### Network Packet Analysis

**Capture Proxy Traffic**
```bash
# Capture traffic on proxy port
sudo tcpdump -i any -w proxy-traffic.pcap port 1080

# Analyze with Wireshark
wireshark proxy-traffic.pcap

# Command-line analysis
tcpdump -r proxy-traffic.pcap -A | grep -i "host:"
```

### Performance Profiling

**Connection Speed Test**
```python
#!/usr/bin/env python3
import time
import requests

def speed_test(proxy_url, test_url="https://httpbin.org/bytes/1048576"):
    proxies = {'http': proxy_url, 'https': proxy_url}
    
    start_time = time.time()
    response = requests.get(test_url, proxies=proxies, timeout=30)
    end_time = time.time()
    
    if response.status_code == 200:
        duration = end_time - start_time
        size_mb = len(response.content) / (1024 * 1024)
        speed_mbps = (size_mb * 8) / duration
        
        print(f"✅ Speed: {speed_mbps:.2f} Mbps")
        print(f"📊 Duration: {duration:.2f} seconds")
        print(f"📊 Size: {size_mb:.2f} MB")
    else:
        print(f"❌ Speed test failed: {response.status_code}")

if __name__ == "__main__":
    speed_test("socks5://127.0.0.1:1080")
```

## 🆘 Getting Help

### Before Asking for Help

**Gather Information**
```bash
#!/bin/bash
# gather-debug-info.sh

echo "🔍 Gathering debug information..."

echo "System Information:"
uname -a
cat /etc/os-release

echo "Network Configuration:"
ip addr show
ip route show

echo "DNS Configuration:"
cat /etc/resolv.conf

echo "Proxy Process:"
ps aux | grep -i proxy

echo "Network Connections:"
netstat -tulpn | grep :1080

echo "Recent Logs:"
tail -50 /var/log/proxy/*.log
```

### Support Channels

1. **GitHub Issues**
   - Search existing issues first
   - Provide debug information
   - Include configuration (remove sensitive data)

2. **Community Forums**
   - Reddit: r/VPN, r/privacy
   - Telegram groups
   - Discord servers

3. **Documentation**
   - Check official documentation
   - Read FAQ sections
   - Review troubleshooting guides

### Creating Bug Reports

**Template:**
```markdown
## Bug Report

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Proxy Client: [e.g., Sing-box 1.5.0]
- Protocol: [e.g., VMess over WebSocket]

**Problem Description:**
[Clear description of the issue]

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. [Third step]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Configuration:**
```json
[Your configuration with sensitive data removed]
```

**Logs:**
```
[Relevant log entries]
```

**Additional Context:**
[Any other relevant information]
```

---

🛠️ **Remember**: Most issues can be resolved by checking the basics first - network connectivity, correct configuration, and up-to-date software. When in doubt, try a different server or protocol!