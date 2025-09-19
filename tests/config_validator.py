#!/usr/bin/env python3
"""
Configuration Validator
Validates proxy configurations for security and correctness
"""

import json
import yaml
import base64
import uuid
import re
import socket
import ssl
import urllib.parse
from typing import Dict, List, Any, Tuple
import jsonschema
from jsonschema import validate
import requests


class ConfigValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        
    def validate_singbox_config(self, config_path: str) -> bool:
        """Validate Sing-box configuration"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            self._validate_singbox_structure(config)
            self._validate_outbounds(config.get('outbounds', []))
            self._validate_routing(config.get('route', {}))
            self._validate_dns(config.get('dns', {}))
            
            return len(self.errors) == 0
            
        except Exception as e:
            self.errors.append(f"Failed to load configuration: {e}")
            return False
    
    def _validate_singbox_structure(self, config: Dict) -> None:
        """Validate basic Sing-box structure"""
        required_fields = ['inbounds', 'outbounds']
        
        for field in required_fields:
            if field not in config:
                self.errors.append(f"Missing required field: {field}")
        
        # Validate inbounds
        if 'inbounds' in config:
            for i, inbound in enumerate(config['inbounds']):
                if 'type' not in inbound:
                    self.errors.append(f"Inbound {i}: missing 'type' field")
                if 'listen_port' not in inbound:
                    self.errors.append(f"Inbound {i}: missing 'listen_port' field")
    
    def _validate_outbounds(self, outbounds: List[Dict]) -> None:
        """Validate outbound configurations"""
        if not outbounds:
            self.errors.append("No outbounds configured")
            return
        
        for i, outbound in enumerate(outbounds):
            self._validate_outbound(i, outbound)
    
    def _validate_outbound(self, index: int, outbound: Dict) -> None:
        """Validate individual outbound configuration"""
        if 'type' not in outbound:
            self.errors.append(f"Outbound {index}: missing 'type' field")
            return
        
        outbound_type = outbound['type']
        
        if outbound_type == 'vmess':
            self._validate_vmess(index, outbound)
        elif outbound_type == 'vless':
            self._validate_vless(index, outbound)
        elif outbound_type == 'shadowsocks':
            self._validate_shadowsocks(index, outbound)
        elif outbound_type == 'trojan':
            self._validate_trojan(index, outbound)
        elif outbound_type == 'hysteria':
            self._validate_hysteria(index, outbound)
        elif outbound_type == 'tuic':
            self._validate_tuic(index, outbound)
        elif outbound_type in ['direct', 'block', 'dns']:
            pass  # These don't need server validation
        else:
            self.warnings.append(f"Outbound {index}: unknown type '{outbound_type}'")
    
    def _validate_vmess(self, index: int, config: Dict) -> None:
        """Validate VMess configuration"""
        required_fields = ['server', 'server_port', 'uuid']
        
        for field in required_fields:
            if field not in config:
                self.errors.append(f"VMess outbound {index}: missing '{field}'")
        
        # Validate UUID format
        if 'uuid' in config:
            try:
                uuid.UUID(config['uuid'])
            except ValueError:
                self.errors.append(f"VMess outbound {index}: invalid UUID format")
        
        # Validate security method
        if 'security' in config:
            valid_methods = ['auto', 'aes-128-gcm', 'chacha20-poly1305', 'none']
            if config['security'] not in valid_methods:
                self.warnings.append(f"VMess outbound {index}: unusual security method '{config['security']}'")
        
        # Validate alter_id
        if 'alter_id' in config and config['alter_id'] != 0:
            self.warnings.append(f"VMess outbound {index}: alter_id should be 0 for security")
        
        # Validate transport
        if 'transport' in config:
            self._validate_transport(index, config['transport'])
        
        # Validate TLS
        if 'tls' in config:
            self._validate_tls(index, config['tls'])
    
    def _validate_vless(self, index: int, config: Dict) -> None:
        """Validate VLESS configuration"""
        required_fields = ['server', 'server_port', 'uuid']
        
        for field in required_fields:
            if field not in config:
                self.errors.append(f"VLESS outbound {index}: missing '{field}'")
        
        # Validate UUID
        if 'uuid' in config:
            try:
                uuid.UUID(config['uuid'])
            except ValueError:
                self.errors.append(f"VLESS outbound {index}: invalid UUID format")
        
        # Validate flow
        if 'flow' in config:
            valid_flows = ['', 'xtls-rprx-vision', 'xtls-rprx-vision-udp443']
            if config['flow'] not in valid_flows:
                self.warnings.append(f"VLESS outbound {index}: unusual flow '{config['flow']}'")
        
        # Validate Reality
        if 'tls' in config and config['tls'].get('reality', {}).get('enabled'):
            self._validate_reality(index, config['tls']['reality'])
    
    def _validate_shadowsocks(self, index: int, config: Dict) -> None:
        """Validate Shadowsocks configuration"""
        required_fields = ['server', 'server_port', 'method', 'password']
        
        for field in required_fields:
            if field not in config:
                self.errors.append(f"Shadowsocks outbound {index}: missing '{field}'")
        
        # Validate encryption method
        if 'method' in config:
            secure_methods = [
                'chacha20-ietf-poly1305',
                'aes-256-gcm',
                'aes-128-gcm',
                '2022-blake3-aes-256-gcm',
                '2022-blake3-chacha20-poly1305'
            ]
            if config['method'] not in secure_methods:
                self.warnings.append(f"Shadowsocks outbound {index}: consider using AEAD cipher")
        
        # Validate password strength
        if 'password' in config:
            password = config['password']
            if len(password) < 8:
                self.warnings.append(f"Shadowsocks outbound {index}: password too short")
    
    def _validate_trojan(self, index: int, config: Dict) -> None:
        """Validate Trojan configuration"""
        required_fields = ['server', 'server_port', 'password']
        
        for field in required_fields:
            if field not in config:
                self.errors.append(f"Trojan outbound {index}: missing '{field}'")
        
        # Validate password strength
        if 'password' in config:
            password = config['password']
            if len(password) < 16:
                self.warnings.append(f"Trojan outbound {index}: password should be at least 16 characters")
        
        # Validate TLS (required for Trojan)
        if 'tls' not in config or not config['tls'].get('enabled'):
            self.errors.append(f"Trojan outbound {index}: TLS is required")
    
    def _validate_hysteria(self, index: int, config: Dict) -> None:
        """Validate Hysteria configuration"""
        required_fields = ['server', 'server_port']
        
        for field in required_fields:
            if field not in config:
                self.errors.append(f"Hysteria outbound {index}: missing '{field}'")
        
        # Validate bandwidth settings
        if 'up_mbps' in config and config['up_mbps'] <= 0:
            self.warnings.append(f"Hysteria outbound {index}: invalid up_mbps value")
        
        if 'down_mbps' in config and config['down_mbps'] <= 0:
            self.warnings.append(f"Hysteria outbound {index}: invalid down_mbps value")
    
    def _validate_tuic(self, index: int, config: Dict) -> None:
        """Validate TUIC configuration"""
        required_fields = ['server', 'server_port', 'uuid', 'password']
        
        for field in required_fields:
            if field not in config:
                self.errors.append(f"TUIC outbound {index}: missing '{field}'")
        
        # Validate UUID
        if 'uuid' in config:
            try:
                uuid.UUID(config['uuid'])
            except ValueError:
                self.errors.append(f"TUIC outbound {index}: invalid UUID format")
        
        # Validate congestion control
        if 'congestion_control' in config:
            valid_cc = ['cubic', 'new_reno', 'bbr']
            if config['congestion_control'] not in valid_cc:
                self.warnings.append(f"TUIC outbound {index}: unusual congestion control")
    
    def _validate_transport(self, index: int, transport: Dict) -> None:
        """Validate transport configuration"""
        if 'type' not in transport:
            self.errors.append(f"Outbound {index}: transport missing 'type'")
            return
        
        transport_type = transport['type']
        
        if transport_type == 'ws':
            if 'path' not in transport:
                self.warnings.append(f"Outbound {index}: WebSocket missing path")
            
            # Check for security headers
            headers = transport.get('headers', {})
            if 'Host' not in headers:
                self.warnings.append(f"Outbound {index}: WebSocket missing Host header")
        
        elif transport_type == 'http':
            if 'host' not in transport:
                self.warnings.append(f"Outbound {index}: HTTP transport missing host")
            if 'path' not in transport:
                self.warnings.append(f"Outbound {index}: HTTP transport missing path")
    
    def _validate_tls(self, index: int, tls: Dict) -> None:
        """Validate TLS configuration"""
        if not tls.get('enabled'):
            return
        
        # Check server name
        if 'server_name' not in tls:
            self.warnings.append(f"Outbound {index}: TLS missing server_name")
        
        # Check TLS version
        if 'min_version' in tls:
            if tls['min_version'] < '1.2':
                self.warnings.append(f"Outbound {index}: TLS version too old")
        
        # Check ALPN
        if 'alpn' in tls:
            recommended_alpn = ['h2', 'http/1.1']
            if not any(proto in tls['alpn'] for proto in recommended_alpn):
                self.warnings.append(f"Outbound {index}: consider adding h2 to ALPN")
    
    def _validate_reality(self, index: int, reality: Dict) -> None:
        """Validate Reality configuration"""
        required_fields = ['public_key', 'short_id']
        
        for field in required_fields:
            if field not in reality:
                self.errors.append(f"Reality outbound {index}: missing '{field}'")
        
        # Validate public key format
        if 'public_key' in reality:
            try:
                base64.b64decode(reality['public_key'])
            except Exception:
                self.errors.append(f"Reality outbound {index}: invalid public key format")
        
        # Validate short ID format
        if 'short_id' in reality:
            if not re.match(r'^[0-9a-f]{0,16}$', reality['short_id']):
                self.errors.append(f"Reality outbound {index}: invalid short_id format")
    
    def _validate_routing(self, route: Dict) -> None:
        """Validate routing configuration"""
        if not route:
            self.warnings.append("No routing rules configured")
            return
        
        # Check for final outbound
        if 'final' not in route:
            self.warnings.append("No final outbound specified in routing")
        
        # Validate rules
        if 'rules' in route:
            for i, rule in enumerate(route['rules']):
                if 'outbound' not in rule:
                    self.errors.append(f"Routing rule {i}: missing outbound")
    
    def _validate_dns(self, dns: Dict) -> None:
        """Validate DNS configuration"""
        if not dns:
            self.warnings.append("No DNS configuration found")
            return
        
        # Check for servers
        if 'servers' not in dns:
            self.errors.append("DNS configuration missing servers")
            return
        
        # Validate DNS servers
        for i, server in enumerate(dns['servers']):
            if isinstance(server, dict):
                if 'address' not in server:
                    self.errors.append(f"DNS server {i}: missing address")
                else:
                    self._validate_dns_address(i, server['address'])
            elif isinstance(server, str):
                self._validate_dns_address(i, server)
    
    def _validate_dns_address(self, index: int, address: str) -> None:
        """Validate DNS server address"""
        if address == 'local':
            return
        
        # Check for secure DNS
        if not (address.startswith('https://') or address.startswith('tls://')):
            self.warnings.append(f"DNS server {index}: consider using secure DNS (DoH/DoT)")
        
        # Validate URL format for DoH
        if address.startswith('https://'):
            try:
                parsed = urllib.parse.urlparse(address)
                if not parsed.netloc:
                    self.errors.append(f"DNS server {index}: invalid DoH URL")
            except Exception:
                self.errors.append(f"DNS server {index}: malformed DoH URL")
    
    def validate_subscription_format(self, content: str) -> bool:
        """Validate subscription format"""
        try:
            # Try to decode base64
            decoded = base64.b64decode(content).decode('utf-8')
            
            # Split into lines and validate each
            lines = decoded.strip().split('\n')
            valid_count = 0
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if self._validate_proxy_url(line):
                    valid_count += 1
                else:
                    self.warnings.append(f"Invalid proxy URL: {line[:50]}...")
            
            if valid_count == 0:
                self.errors.append("No valid proxy URLs found in subscription")
                return False
            
            self.info.append(f"Found {valid_count} valid proxy configurations")
            return True
            
        except Exception as e:
            self.errors.append(f"Failed to decode subscription: {e}")
            return False
    
    def _validate_proxy_url(self, url: str) -> bool:
        """Validate proxy URL format"""
        # VMess
        if url.startswith('vmess://'):
            try:
                config_b64 = url[8:]
                config_json = base64.b64decode(config_b64).decode('utf-8')
                config = json.loads(config_json)
                
                required_fields = ['add', 'port', 'id']
                return all(field in config for field in required_fields)
            except:
                return False
        
        # Shadowsocks
        elif url.startswith('ss://'):
            try:
                # Parse ss://method:password@server:port#remarks
                url_part = url[5:]
                if '#' in url_part:
                    url_part = url_part.split('#')[0]
                
                if '@' in url_part:
                    auth_part, server_part = url_part.split('@', 1)
                    return ':' in server_part
                else:
                    # Base64 encoded format
                    decoded = base64.b64decode(url_part).decode('utf-8')
                    return '@' in decoded and ':' in decoded
            except:
                return False
        
        # Trojan
        elif url.startswith('trojan://'):
            try:
                # Parse trojan://password@server:port?params#remarks
                url_part = url[9:]
                if '#' in url_part:
                    url_part = url_part.split('#')[0]
                if '?' in url_part:
                    url_part = url_part.split('?')[0]
                
                return '@' in url_part and ':' in url_part.split('@')[1]
            except:
                return False
        
        # VLESS
        elif url.startswith('vless://'):
            try:
                # Parse vless://uuid@server:port?params#remarks
                url_part = url[8:]
                if '#' in url_part:
                    url_part = url_part.split('#')[0]
                if '?' in url_part:
                    url_part = url_part.split('?')[0]
                
                if '@' in url_part:
                    uuid_part, server_part = url_part.split('@', 1)
                    uuid.UUID(uuid_part)  # Validate UUID
                    return ':' in server_part
            except:
                return False
        
        return False
    
    def test_connectivity(self, config_path: str) -> bool:
        """Test proxy connectivity"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Test each outbound
            for outbound in config.get('outbounds', []):
                if outbound.get('type') in ['direct', 'block', 'dns']:
                    continue
                
                server = outbound.get('server')
                port = outbound.get('server_port')
                
                if server and port:
                    if self._test_tcp_connection(server, port):
                        self.info.append(f"✅ {server}:{port} is reachable")
                    else:
                        self.warnings.append(f"⚠️  {server}:{port} is not reachable")
            
            return True
            
        except Exception as e:
            self.errors.append(f"Connectivity test failed: {e}")
            return False
    
    def _test_tcp_connection(self, host: str, port: int, timeout: int = 5) -> bool:
        """Test TCP connection to host:port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def generate_report(self) -> str:
        """Generate validation report"""
        report = []
        
        if self.errors:
            report.append("🚫 ERRORS:")
            for error in self.errors:
                report.append(f"   • {error}")
            report.append("")
        
        if self.warnings:
            report.append("⚠️  WARNINGS:")
            for warning in self.warnings:
                report.append(f"   • {warning}")
            report.append("")
        
        if self.info:
            report.append("ℹ️  INFO:")
            for info in self.info:
                report.append(f"   • {info}")
            report.append("")
        
        # Summary
        if not self.errors and not self.warnings:
            report.append("✅ Configuration validation passed!")
        elif not self.errors:
            report.append("⚠️  Configuration has warnings but is valid")
        else:
            report.append("❌ Configuration validation failed!")
        
        return "\n".join(report)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate proxy configurations')
    parser.add_argument('config', help='Configuration file to validate')
    parser.add_argument('--type', choices=['singbox', 'subscription'], 
                       default='singbox', help='Configuration type')
    parser.add_argument('--test-connectivity', action='store_true',
                       help='Test server connectivity')
    
    args = parser.parse_args()
    
    validator = ConfigValidator()
    
    if args.type == 'singbox':
        success = validator.validate_singbox_config(args.config)
        
        if args.test_connectivity:
            validator.test_connectivity(args.config)
    
    elif args.type == 'subscription':
        with open(args.config, 'r') as f:
            content = f.read()
        success = validator.validate_subscription_format(content)
    
    print(validator.generate_report())
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())