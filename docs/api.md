# 🔌 API Documentation

This document describes the APIs and interfaces available in the Free Proxy Configurations project.

## 📋 Table of Contents

- [Configuration Generator API](#configuration-generator-api)
- [Validator API](#validator-api)
- [Auto-Updater API](#auto-updater-api)
- [Security Tester API](#security-tester-api)
- [REST API Endpoints](#rest-api-endpoints)

## 🔧 Configuration Generator API

### ProxyGenerator Class

The main class for generating proxy configurations.

```python
from scripts.proxy_generator import ProxyGenerator

generator = ProxyGenerator()
```

#### Methods

**`generate_shadowsocks_config(server: Dict) -> Dict`**
```python
server = {
    "host": "server.example.com",
    "country": "US",
    "city": "New York",
    "ports": {"shadowsocks": 8388}
}
config = generator.generate_shadowsocks_config(server)
```

**`generate_vmess_config(server: Dict) -> Dict`**
```python
config = generator.generate_vmess_config(server)
```

**`generate_trojan_config(server: Dict) -> Dict`**
```python
config = generator.generate_trojan_config(server)
```

**`generate_hysteria_config(server: Dict) -> Dict`**
```python
config = generator.generate_hysteria_config(server)
```

**`generate_tuic_config(server: Dict) -> Dict`**
```python
config = generator.generate_tuic_config(server)
```

**`generate_reality_config(server: Dict) -> Dict`**
```python
config = generator.generate_reality_config(server)
```

**`generate_ssh_config(server: Dict) -> Dict`**
```python
config = generator.generate_ssh_config(server)
```

**`generate_singbox_config() -> Dict`**
```python
config = generator.generate_singbox_config()
```

**`export_shadowsocks_subscription() -> str`**
```python
subscription = generator.export_shadowsocks_subscription()
```

**`export_vmess_subscription() -> str`**
```python
subscription = generator.export_vmess_subscription()
```

**`export_universal_subscription() -> str`**
```python
subscription = generator.export_universal_subscription()
```

### Server Data Format

```python
server = {
    "host": "server.example.com",      # Server hostname or IP
    "country": "US",                   # Country code
    "city": "New York",                # City name
    "ports": {                         # Port mappings
        "shadowsocks": 8388,
        "trojan": 443,
        "vmess": 10086,
        "hysteria": 443,
        "tuic": 443
    }
}
```

## ✅ Validator API

### ConfigValidator Class

```python
from tests.config_validator import ConfigValidator

validator = ConfigValidator()
```

#### Methods

**`validate_singbox_config(config_path: str) -> bool`**
```python
is_valid = validator.validate_singbox_config("config.json")
```

**`validate_subscription_format(content: str) -> bool`**
```python
with open("subscription.txt", "r") as f:
    content = f.read()
is_valid = validator.validate_subscription_format(content)
```

**`test_connectivity(config_path: str) -> bool`**
```python
is_reachable = validator.test_connectivity("config.json")
```

**`generate_report() -> str`**
```python
report = validator.generate_report()
print(report)
```

### Validation Results

```python
# Access validation results
errors = validator.errors        # List of error messages
warnings = validator.warnings    # List of warning messages
info = validator.info            # List of info messages
```

## 🔄 Auto-Updater API

### ProxyUpdater Class

```python
from scripts.auto_updater import ProxyUpdater

updater = ProxyUpdater()
```

#### Methods

**`fetch_proxy_servers() -> List[Dict]`**
```python
servers = updater.fetch_proxy_servers()
```

**`validate_servers(servers: List[Dict]) -> List[Dict]`**
```python
valid_servers = updater.validate_servers(servers)
```

**`generate_configurations(servers: List[Dict]) -> None`**
```python
updater.generate_configurations(valid_servers)
```

**`run_update_cycle() -> None`**
```python
updater.run_update_cycle()
```

**`start_scheduler() -> None`**
```python
updater.start_scheduler()  # Runs continuously
```

### Server Data Format

```python
server = {
    "host": "1.2.3.4",
    "port": 8080,
    "country": "US",
    "city": "New York",
    "source": "API Source Name"
}
```

## 🔒 Security Tester API

### SecurityTester Class

```python
from tests.security_test import SecurityTester

proxy_config = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}
tester = SecurityTester(proxy_config)
```

#### Methods

**`run_all_tests() -> Dict[str, bool]`**
```python
results = tester.run_all_tests()
```

**`test_ip_leak() -> bool`**
```python
no_leak = tester.test_ip_leak()
```

**`test_dns_leak() -> bool`**
```python
no_leak = tester.test_dns_leak()
```

**`test_proxy_connectivity() -> bool`**
```python
is_working = tester.test_proxy_connectivity()
```

**`generate_security_report(results: Dict[str, bool]) -> str`**
```python
report = tester.generate_security_report(results)
```

## 🌐 REST API Endpoints

### Configuration Endpoints

**GET `/api/v1/configs/singbox`**
```http
GET /api/v1/configs/singbox
Content-Type: application/json

Response:
{
  "log": {...},
  "inbounds": [...],
  "outbounds": [...],
  "route": {...}
}
```

**GET `/api/v1/configs/subscription/{type}`**
```http
GET /api/v1/configs/subscription/universal
Content-Type: text/plain

Response: Base64 encoded subscription content
```

**GET `/api/v1/configs/subscription/{type}/raw`**
```http
GET /api/v1/configs/subscription/universal/raw
Content-Type: text/plain

Response: Raw subscription URLs (one per line)
```

### Server Information Endpoints

**GET `/api/v1/servers`**
```http
GET /api/v1/servers
Content-Type: application/json

Response:
{
  "servers": [
    {
      "host": "server1.example.com",
      "country": "US",
      "city": "New York",
      "protocols": ["vmess", "shadowsocks", "trojan"],
      "status": "online",
      "ping": 45
    }
  ],
  "total": 10,
  "online": 8
}
```

**GET `/api/v1/servers/{country}`**
```http
GET /api/v1/servers/US
Content-Type: application/json

Response: Servers filtered by country
```

### Status Endpoints

**GET `/api/v1/status`**
```http
GET /api/v1/status
Content-Type: application/json

Response:
{
  "last_updated": "2024-01-01T12:00:00Z",
  "server_count": 25,
  "status": "active",
  "next_update": 1704110400,
  "version": "1.0.0"
}
```

**GET `/api/v1/health`**
```http
GET /api/v1/health
Content-Type: application/json

Response:
{
  "status": "healthy",
  "checks": {
    "database": "ok",
    "external_apis": "ok",
    "disk_space": "ok"
  }
}
```

### Validation Endpoints

**POST `/api/v1/validate/config`**
```http
POST /api/v1/validate/config
Content-Type: application/json

Request:
{
  "type": "singbox",
  "config": {...}
}

Response:
{
  "valid": true,
  "errors": [],
  "warnings": ["Minor warning message"],
  "info": ["Configuration looks good"]
}
```

**POST `/api/v1/validate/subscription`**
```http
POST /api/v1/validate/subscription
Content-Type: text/plain

Request: Base64 encoded subscription content

Response:
{
  "valid": true,
  "proxy_count": 15,
  "protocols": ["vmess", "shadowsocks", "trojan"],
  "errors": [],
  "warnings": []
}
```

## 🔧 Command Line Interface

### Configuration Generation

```bash
# Generate all configurations
python scripts/proxy_generator.py

# Generate specific protocol
python scripts/proxy_generator.py --protocol vmess

# Output to specific directory
python scripts/proxy_generator.py --output /path/to/configs
```

### Configuration Validation

```bash
# Validate Sing-box config
python tests/config_validator.py config.json --type singbox

# Validate subscription
python tests/config_validator.py subscription.txt --type subscription

# Test connectivity
python tests/config_validator.py config.json --test-connectivity
```

### Security Testing

```bash
# Run all security tests
python tests/security_test.py

# Use custom proxy
python tests/security_test.py --proxy-http socks5://127.0.0.1:1080

# Save report to file
python tests/security_test.py --output security-report.txt
```

### Auto-Updater

```bash
# Run single update
python scripts/auto_updater.py --once

# Start continuous updates
python scripts/auto_updater.py

# Custom update interval
python scripts/auto_updater.py --interval 3600  # 1 hour
```

## 📊 Data Formats

### Configuration Schema

**Sing-box Configuration**
```json
{
  "log": {
    "level": "info",
    "timestamp": true
  },
  "dns": {
    "servers": [...],
    "rules": [...],
    "final": "cloudflare"
  },
  "inbounds": [
    {
      "type": "mixed",
      "listen": "127.0.0.1",
      "listen_port": 1080
    }
  ],
  "outbounds": [...],
  "route": {
    "rules": [...],
    "final": "proxy"
  }
}
```

**Subscription Format**
```
vmess://base64-encoded-config
ss://base64-encoded-config
trojan://password@server:port?params#remarks
vless://uuid@server:port?params#remarks
```

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Configuration validation failed",
    "details": [
      {
        "field": "outbounds[0].server",
        "message": "Server address is required"
      }
    ]
  }
}
```

## 🔐 Authentication

### API Key Authentication

```http
Authorization: Bearer your-api-key-here
```

### Rate Limiting

- **Configuration endpoints**: 100 requests per hour
- **Validation endpoints**: 1000 requests per hour
- **Status endpoints**: 10000 requests per hour

## 📚 SDK Examples

### Python SDK

```python
import requests

class ProxyConfigAPI:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.headers = {}
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def get_singbox_config(self):
        response = requests.get(
            f'{self.base_url}/api/v1/configs/singbox',
            headers=self.headers
        )
        return response.json()
    
    def get_subscription(self, sub_type='universal'):
        response = requests.get(
            f'{self.base_url}/api/v1/configs/subscription/{sub_type}',
            headers=self.headers
        )
        return response.text
    
    def validate_config(self, config, config_type='singbox'):
        response = requests.post(
            f'{self.base_url}/api/v1/validate/config',
            json={'type': config_type, 'config': config},
            headers=self.headers
        )
        return response.json()

# Usage
api = ProxyConfigAPI('https://api.example.com')
config = api.get_singbox_config()
subscription = api.get_subscription('universal')
```

### JavaScript SDK

```javascript
class ProxyConfigAPI {
    constructor(baseUrl, apiKey = null) {
        this.baseUrl = baseUrl;
        this.headers = {};
        if (apiKey) {
            this.headers['Authorization'] = `Bearer ${apiKey}`;
        }
    }
    
    async getSingboxConfig() {
        const response = await fetch(`${this.baseUrl}/api/v1/configs/singbox`, {
            headers: this.headers
        });
        return response.json();
    }
    
    async getSubscription(type = 'universal') {
        const response = await fetch(`${this.baseUrl}/api/v1/configs/subscription/${type}`, {
            headers: this.headers
        });
        return response.text();
    }
    
    async validateConfig(config, type = 'singbox') {
        const response = await fetch(`${this.baseUrl}/api/v1/validate/config`, {
            method: 'POST',
            headers: {
                ...this.headers,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ type, config })
        });
        return response.json();
    }
}

// Usage
const api = new ProxyConfigAPI('https://api.example.com');
const config = await api.getSingboxConfig();
const subscription = await api.getSubscription('universal');
```

---

📚 This API documentation provides comprehensive information for integrating with the Free Proxy Configurations system. For more examples and detailed usage, check the source code and test files.