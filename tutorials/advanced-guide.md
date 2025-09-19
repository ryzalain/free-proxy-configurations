# 🔧 Advanced Proxy Configuration Guide

This guide covers advanced topics for experienced users who want to maximize security, performance, and customization of their proxy setups.

## 🎯 Target Audience

- Users familiar with basic proxy concepts
- System administrators and power users
- Privacy enthusiasts seeking maximum security
- Users wanting to customize configurations

## 🏗️ Advanced Configuration Concepts

### Protocol Deep Dive

#### VMess (V2Ray)
```json
{
  "protocol": "vmess",
  "settings": {
    "vnext": [{
      "address": "server.example.com",
      "port": 443,
      "users": [{
        "id": "uuid-here",
        "security": "chacha20-poly1305",
        "alterId": 0
      }]
    }]
  },
  "streamSettings": {
    "network": "ws",
    "security": "tls",
    "wsSettings": {
      "path": "/vmess",
      "headers": {
        "Host": "server.example.com"
      }
    },
    "tlsSettings": {
      "serverName": "server.example.com",
      "alpn": ["h2", "http/1.1"]
    }
  }
}
```

**Key Features:**
- Dynamic port allocation
- Built-in encryption
- Traffic obfuscation
- WebSocket transport support

#### Reality Protocol
```json
{
  "protocol": "vless",
  "settings": {
    "vnext": [{
      "address": "server.example.com",
      "port": 443,
      "users": [{
        "id": "uuid-here",
        "flow": "xtls-rprx-vision"
      }]
    }]
  },
  "streamSettings": {
    "network": "tcp",
    "security": "reality",
    "realitySettings": {
      "serverName": "www.microsoft.com",
      "fingerprint": "chrome",
      "publicKey": "public-key-here",
      "shortId": "short-id"
    }
  }
}
```

**Advantages:**
- Undetectable by DPI systems
- Perfect TLS camouflage
- No server-side TLS certificate needed
- Resistant to active probing

#### Hysteria Protocol
```yaml
server: server.example.com:443
protocol: udp
up_mbps: 100
down_mbps: 100
alpn: h3
obfs: obfuscation-password
insecure: false
sni: server.example.com
fast_open: true
lazy: false
hop_interval: 30
```

**Benefits:**
- QUIC-based for better performance
- Built-in congestion control
- Excellent for high-latency connections
- Resistant to packet loss

### Advanced Routing Rules

#### Sing-box Routing Configuration
```json
{
  "route": {
    "rules": [
      {
        "geosite": ["cn", "private"],
        "outbound": "direct"
      },
      {
        "geoip": ["cn", "private"],
        "outbound": "direct"
      },
      {
        "domain_suffix": [".cn", ".中国"],
        "outbound": "direct"
      },
      {
        "process_name": ["telegram", "discord"],
        "outbound": "proxy-fast"
      },
      {
        "port": [80, 443],
        "network": "tcp",
        "outbound": "proxy-secure"
      }
    ],
    "final": "proxy-default"
  }
}
```

#### Custom DNS Configuration
```json
{
  "dns": {
    "servers": [
      {
        "tag": "cloudflare-doh",
        "address": "https://1.1.1.1/dns-query",
        "detour": "direct"
      },
      {
        "tag": "quad9-dot",
        "address": "tls://9.9.9.9",
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
        "server": "cloudflare-doh"
      }
    ],
    "final": "quad9-dot",
    "strategy": "prefer_ipv4",
    "disable_cache": false,
    "disable_expire": false
  }
}
```

## 🔐 Security Hardening

### TLS Configuration Best Practices

#### Strong Cipher Suites
```json
{
  "tlsSettings": {
    "serverName": "server.example.com",
    "alpn": ["h2", "http/1.1"],
    "minVersion": "1.3",
    "maxVersion": "1.3",
    "cipherSuites": [
      "TLS_AES_256_GCM_SHA384",
      "TLS_CHACHA20_POLY1305_SHA256",
      "TLS_AES_128_GCM_SHA256"
    ],
    "curves": ["X25519", "P-256"],
    "fingerprint": "chrome"
  }
}
```

### Certificate Pinning
```json
{
  "tlsSettings": {
    "serverName": "server.example.com",
    "pinnedPeerCertificateChainSha256": [
      "sha256-hash-of-certificate"
    ],
    "allowInsecure": false
  }
}
```

### Traffic Obfuscation Techniques

#### WebSocket with Custom Headers
```json
{
  "wsSettings": {
    "path": "/api/v1/ws",
    "headers": {
      "Host": "server.example.com",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
      "X-Forwarded-For": "1.1.1.1",
      "X-Real-IP": "1.1.1.1"
    }
  }
}
```

#### HTTP/2 Transport
```json
{
  "httpSettings": {
    "host": ["server.example.com"],
    "path": "/api/data",
    "method": "POST",
    "headers": {
      "Content-Type": ["application/json"],
      "Cache-Control": ["no-cache"]
    }
  }
}
```

## ⚡ Performance Optimization

### Connection Pooling
```json
{
  "mux": {
    "enabled": true,
    "concurrency": 8,
    "xudpConcurrency": 16,
    "xudpProxyUDP443": "reject"
  }
}
```

### Buffer Size Optimization
```json
{
  "sockopt": {
    "mark": 0,
    "tcpFastOpen": true,
    "tcpKeepAliveInterval": 30,
    "tcpUserTimeout": 10000,
    "tcpMaxSeg": 1440
  }
}
```

### Load Balancing Configuration
```json
{
  "balancers": [
    {
      "tag": "load-balancer",
      "selector": ["proxy-1", "proxy-2", "proxy-3"],
      "strategy": {
        "type": "leastPing"
      }
    }
  ]
}
```

## 🛡️ Advanced Security Features

### Kill Switch Implementation
```json
{
  "policy": {
    "levels": {
      "0": {
        "handshake": 4,
        "connIdle": 300,
        "uplinkOnly": 2,
        "downlinkOnly": 5,
        "bufferSize": 10240,
        "statsUserUplink": true,
        "statsUserDownlink": true
      }
    },
    "system": {
      "statsInboundUplink": true,
      "statsInboundDownlink": true,
      "statsOutboundUplink": true,
      "statsOutboundDownlink": true
    }
  }
}
```

### DNS Leak Prevention
```json
{
  "dns": {
    "servers": [
      {
        "address": "1.1.1.1",
        "domains": ["geosite:geolocation-!cn"]
      },
      {
        "address": "114.114.114.114",
        "domains": ["geosite:cn"]
      }
    ],
    "queryStrategy": "UseIPv4",
    "disableCache": false,
    "disableFallback": true
  }
}
```

### IPv6 Leak Protection
```json
{
  "routing": {
    "rules": [
      {
        "type": "field",
        "ip": ["::/0"],
        "outboundTag": "block"
      }
    ]
  }
}
```

## 🔄 Automated Configuration Management

### Configuration Validation Script
```python
#!/usr/bin/env python3
import json
import jsonschema
from jsonschema import validate

def validate_config(config_file, schema_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    with open(schema_file, 'r') as f:
        schema = json.load(f)
    
    try:
        validate(instance=config, schema=schema)
        print(f"✅ {config_file} is valid")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"❌ {config_file} validation failed: {e}")
        return False

# Usage
validate_config('config.json', 'schema.json')
```

### Health Check Script
```bash
#!/bin/bash

CONFIG_FILE="config.json"
TEST_URL="https://httpbin.org/ip"
TIMEOUT=10

# Test proxy connectivity
test_proxy() {
    local proxy_url=$1
    local response=$(curl -s --max-time $TIMEOUT --proxy "$proxy_url" "$TEST_URL")
    
    if [[ $? -eq 0 ]] && [[ -n "$response" ]]; then
        echo "✅ Proxy $proxy_url is working"
        return 0
    else
        echo "❌ Proxy $proxy_url failed"
        return 1
    fi
}

# Extract proxies from config and test
jq -r '.outbounds[] | select(.protocol != "direct" and .protocol != "block") | "\(.protocol)://\(.settings.vnext[0].address):\(.settings.vnext[0].port)"' "$CONFIG_FILE" | while read proxy; do
    test_proxy "$proxy"
done
```

## 📊 Monitoring and Analytics

### Traffic Analysis
```json
{
  "stats": {},
  "api": {
    "tag": "api",
    "services": ["StatsService"]
  },
  "policy": {
    "levels": {
      "0": {
        "statsUserUplink": true,
        "statsUserDownlink": true
      }
    }
  }
}
```

### Log Configuration
```json
{
  "log": {
    "access": "/var/log/proxy/access.log",
    "error": "/var/log/proxy/error.log",
    "loglevel": "info",
    "dnsLog": true
  }
}
```

## 🌐 Multi-Platform Deployment

### Docker Configuration
```dockerfile
FROM alpine:latest

RUN apk add --no-cache ca-certificates tzdata
RUN adduser -D -s /bin/sh proxy

COPY config.json /etc/proxy/
COPY proxy-binary /usr/bin/proxy

USER proxy
EXPOSE 1080 1081

CMD ["/usr/bin/proxy", "-config", "/etc/proxy/config.json"]
```

### Systemd Service
```ini
[Unit]
Description=Proxy Service
After=network.target

[Service]
Type=simple
User=proxy
Group=proxy
ExecStart=/usr/bin/proxy -config /etc/proxy/config.json
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## 🔧 Custom Protocol Development

### Plugin Architecture
```go
package main

import (
    "context"
    "net"
)

type ProxyPlugin interface {
    Name() string
    Dial(ctx context.Context, dest net.Destination) (net.Conn, error)
    Listen(ctx context.Context, addr net.Address) (net.Listener, error)
}

type CustomProtocol struct {
    config *Config
}

func (p *CustomProtocol) Name() string {
    return "custom-protocol"
}

func (p *CustomProtocol) Dial(ctx context.Context, dest net.Destination) (net.Conn, error) {
    // Custom dialing logic
    return nil, nil
}
```

## 🚀 Performance Tuning

### Kernel Parameters
```bash
# /etc/sysctl.conf
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 134217728
net.ipv4.tcp_wmem = 4096 65536 134217728
net.ipv4.tcp_congestion_control = bbr
net.core.default_qdisc = fq
```

### Application-Level Tuning
```json
{
  "transport": {
    "tcpSettings": {
      "header": {
        "type": "none"
      },
      "acceptProxyProtocol": false
    },
    "kcpSettings": {
      "mtu": 1350,
      "tti": 20,
      "uplinkCapacity": 100,
      "downlinkCapacity": 100,
      "congestion": true,
      "readBufferSize": 2,
      "writeBufferSize": 2
    }
  }
}
```

## 🔍 Troubleshooting Advanced Issues

### Debug Mode Configuration
```json
{
  "log": {
    "loglevel": "debug",
    "access": "stdout:",
    "error": "stdout:"
  }
}
```

### Network Diagnostics
```bash
# Test connectivity
nc -zv server.example.com 443

# Check TLS handshake
openssl s_client -connect server.example.com:443 -servername server.example.com

# Trace route
traceroute server.example.com

# DNS resolution
dig @1.1.1.1 server.example.com
```

## 📚 Additional Resources

- [Protocol Specifications](../docs/protocols.md)
- [Security Best Practices](../docs/security.md)
- [Performance Benchmarks](../docs/benchmarks.md)
- [API Documentation](../docs/api.md)

---

This advanced guide provides the foundation for building robust, secure, and high-performance proxy configurations. Always test thoroughly in a safe environment before deploying to production.