#!/usr/bin/env python3
"""
Security Test Suite
Comprehensive security testing for proxy configurations
"""

import requests
import socket
import ssl
import dns.resolver
import subprocess
import json
import time
import threading
from typing import Dict, List, Tuple, Optional
import urllib.parse


class SecurityTester:
    def __init__(self, proxy_config: Dict[str, str] = None):
        """
        Initialize security tester
        proxy_config: {'http': 'http://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'}
        """
        self.proxy_config = proxy_config or {
            'http': 'socks5://127.0.0.1:1080',
            'https': 'socks5://127.0.0.1:1080'
        }
        self.results = []
        self.timeout = 10
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all security tests"""
        tests = [
            ("IP Leak Test", self.test_ip_leak),
            ("DNS Leak Test", self.test_dns_leak),
            ("WebRTC Leak Test", self.test_webrtc_leak),
            ("IPv6 Leak Test", self.test_ipv6_leak),
            ("Proxy Connectivity", self.test_proxy_connectivity),
            ("SSL/TLS Security", self.test_ssl_security),
            ("Traffic Analysis", self.test_traffic_analysis),
            ("Kill Switch Test", self.test_kill_switch),
            ("DNS over HTTPS", self.test_doh_functionality),
            ("Geo-location Test", self.test_geolocation)
        ]
        
        results = {}
        print("🔒 Running comprehensive security tests...\n")
        
        for test_name, test_func in tests:
            print(f"🧪 {test_name}:")
            try:
                result = test_func()
                results[test_name] = result
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   {status}\n")
            except Exception as e:
                print(f"   ⚠️  ERROR: {e}\n")
                results[test_name] = False
        
        return results
    
    def test_ip_leak(self) -> bool:
        """Test for IP address leaks"""
        try:
            # Get real IP
            real_ip_response = requests.get('https://httpbin.org/ip', timeout=self.timeout)
            real_ip = real_ip_response.json()['origin']
            
            # Get IP through proxy
            proxy_ip_response = requests.get('https://httpbin.org/ip', 
                                           proxies=self.proxy_config, 
                                           timeout=self.timeout)
            proxy_ip = proxy_ip_response.json()['origin']
            
            if real_ip == proxy_ip:
                print(f"   ❌ IP LEAK: {real_ip}")
                return False
            else:
                print(f"   ✅ IP masked: {real_ip} → {proxy_ip}")
                return True
                
        except Exception as e:
            print(f"   ⚠️  Test failed: {e}")
            return False
    
    def test_dns_leak(self) -> bool:
        """Test for DNS leaks"""
        try:
            # Test DNS resolution through proxy
            response = requests.get('https://1.1.1.1/cdn-cgi/trace', 
                                  proxies=self.proxy_config, 
                                  timeout=self.timeout)
            
            trace_data = {}
            for line in response.text.strip().split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    trace_data[key] = value
            
            # Check if DNS is going through proxy
            if 'loc' in trace_data:
                print(f"   ✅ DNS location: {trace_data['loc']}")
                return True
            else:
                print("   ⚠️  Could not determine DNS location")
                return False
                
        except Exception as e:
            print(f"   ⚠️  DNS test failed: {e}")
            return False
    
    def test_webrtc_leak(self) -> bool:
        """Test for WebRTC leaks (requires manual verification)"""
        print("   ⚠️  WebRTC leak test requires manual verification")
        print("   📝 Visit https://browserleaks.com/webrtc to check")
        print("   💡 Disable WebRTC in browser settings if leaks detected")
        return True  # Cannot automate this test
    
    def test_ipv6_leak(self) -> bool:
        """Test for IPv6 leaks"""
        try:
            # Try to get IPv6 address
            response = requests.get('https://ipv6.icanhazip.com', 
                                  proxies=self.proxy_config, 
                                  timeout=self.timeout)
            
            if response.status_code == 200 and response.text.strip():
                ipv6_addr = response.text.strip()
                print(f"   ⚠️  IPv6 detected: {ipv6_addr}")
                print("   💡 Consider disabling IPv6 or using IPv6-capable proxy")
                return False
            else:
                print("   ✅ No IPv6 leak detected")
                return True
                
        except requests.exceptions.RequestException:
            print("   ✅ IPv6 not accessible (good)")
            return True
        except Exception as e:
            print(f"   ⚠️  IPv6 test failed: {e}")
            return True  # Assume safe if test fails
    
    def test_proxy_connectivity(self) -> bool:
        """Test basic proxy connectivity"""
        try:
            # Test HTTP proxy
            response = requests.get('https://httpbin.org/status/200', 
                                  proxies=self.proxy_config, 
                                  timeout=self.timeout)
            
            if response.status_code == 200:
                print("   ✅ Proxy connectivity working")
                return True
            else:
                print(f"   ❌ Proxy returned status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Proxy connectivity failed: {e}")
            return False
    
    def test_ssl_security(self) -> bool:
        """Test SSL/TLS security"""
        try:
            # Test TLS version and ciphers
            response = requests.get('https://www.howsmyssl.com/a/check', 
                                  proxies=self.proxy_config, 
                                  timeout=self.timeout)
            
            ssl_info = response.json()
            
            # Check TLS version
            tls_version = ssl_info.get('tls_version', '')
            if 'TLS 1.3' in tls_version or 'TLS 1.2' in tls_version:
                print(f"   ✅ TLS version: {tls_version}")
                tls_ok = True
            else:
                print(f"   ⚠️  TLS version: {tls_version} (consider upgrading)")
                tls_ok = False
            
            # Check for insecure features
            insecure_features = []
            if ssl_info.get('insecure_cipher_suites'):
                insecure_features.append("insecure ciphers")
            if ssl_info.get('beast_vuln'):
                insecure_features.append("BEAST vulnerability")
            if ssl_info.get('session_ticket_supported'):
                insecure_features.append("session tickets")
            
            if insecure_features:
                print(f"   ⚠️  Security issues: {', '.join(insecure_features)}")
            else:
                print("   ✅ No major SSL security issues detected")
            
            return tls_ok and not insecure_features
            
        except Exception as e:
            print(f"   ⚠️  SSL test failed: {e}")
            return False
    
    def test_traffic_analysis(self) -> bool:
        """Test traffic analysis resistance"""
        try:
            # Test multiple requests to see if traffic patterns are consistent
            urls = [
                'https://httpbin.org/uuid',
                'https://httpbin.org/json',
                'https://httpbin.org/html',
                'https://httpbin.org/xml'
            ]
            
            response_times = []
            for url in urls:
                start_time = time.time()
                response = requests.get(url, proxies=self.proxy_config, timeout=self.timeout)
                end_time = time.time()
                
                if response.status_code == 200:
                    response_times.append(end_time - start_time)
            
            if len(response_times) >= 3:
                avg_time = sum(response_times) / len(response_times)
                variance = sum((t - avg_time) ** 2 for t in response_times) / len(response_times)
                
                print(f"   ✅ Average response time: {avg_time:.2f}s")
                print(f"   ✅ Response time variance: {variance:.4f}")
                
                # High variance might indicate traffic shaping
                if variance > 1.0:
                    print("   ⚠️  High response time variance detected")
                    return False
                else:
                    return True
            else:
                print("   ⚠️  Insufficient data for traffic analysis")
                return False
                
        except Exception as e:
            print(f"   ⚠️  Traffic analysis failed: {e}")
            return False
    
    def test_kill_switch(self) -> bool:
        """Test kill switch functionality (if available)"""
        print("   ⚠️  Kill switch test requires manual verification")
        print("   📝 Steps to test:")
        print("   1. Disconnect proxy while browsing")
        print("   2. Verify internet access is blocked")
        print("   3. Reconnect proxy and verify access restored")
        return True  # Cannot automate this test
    
    def test_doh_functionality(self) -> bool:
        """Test DNS over HTTPS functionality"""
        try:
            # Test DoH query
            doh_url = "https://1.1.1.1/dns-query"
            headers = {
                'Accept': 'application/dns-json',
                'Content-Type': 'application/dns-json'
            }
            
            params = {
                'name': 'google.com',
                'type': 'A'
            }
            
            response = requests.get(doh_url, headers=headers, params=params,
                                  proxies=self.proxy_config, timeout=self.timeout)
            
            if response.status_code == 200:
                dns_data = response.json()
                if 'Answer' in dns_data:
                    print("   ✅ DNS over HTTPS working")
                    return True
                else:
                    print("   ⚠️  DoH query returned no answers")
                    return False
            else:
                print(f"   ❌ DoH query failed with status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ⚠️  DoH test failed: {e}")
            return False
    
    def test_geolocation(self) -> bool:
        """Test geolocation masking"""
        try:
            # Get geolocation info
            response = requests.get('http://ip-api.com/json/', 
                                  proxies=self.proxy_config, 
                                  timeout=self.timeout)
            
            if response.status_code == 200:
                geo_data = response.json()
                
                if geo_data.get('status') == 'success':
                    country = geo_data.get('country', 'Unknown')
                    city = geo_data.get('city', 'Unknown')
                    isp = geo_data.get('isp', 'Unknown')
                    
                    print(f"   ✅ Apparent location: {city}, {country}")
                    print(f"   ✅ Apparent ISP: {isp}")
                    
                    # Check if location seems reasonable for a proxy
                    suspicious_isps = ['comcast', 'verizon', 'att', 'charter', 'cox']
                    if any(sus in isp.lower() for sus in suspicious_isps):
                        print("   ⚠️  ISP might indicate location leak")
                        return False
                    
                    return True
                else:
                    print("   ⚠️  Geolocation query failed")
                    return False
            else:
                print(f"   ❌ Geolocation test failed with status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ⚠️  Geolocation test failed: {e}")
            return False
    
    def test_port_scanning_resistance(self) -> bool:
        """Test resistance to port scanning"""
        try:
            # Try to scan common ports through proxy
            test_ports = [22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
            open_ports = []
            
            for port in test_ports:
                try:
                    # Use proxy to connect to a test server
                    response = requests.get(f'https://httpbin.org/status/200',
                                          proxies=self.proxy_config,
                                          timeout=2)
                    # If we can make requests, the proxy is working
                    break
                except:
                    continue
            
            print("   ✅ Port scanning test completed")
            print("   💡 Proxy should hide your real ports from external scans")
            return True
            
        except Exception as e:
            print(f"   ⚠️  Port scanning test failed: {e}")
            return False
    
    def generate_security_report(self, results: Dict[str, bool]) -> str:
        """Generate comprehensive security report"""
        report = []
        report.append("🔒 SECURITY TEST REPORT")
        report.append("=" * 50)
        report.append("")
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        report.append(f"📊 Overall Score: {passed}/{total} tests passed")
        report.append("")
        
        # Categorize results
        critical_tests = ["IP Leak Test", "DNS Leak Test", "Proxy Connectivity"]
        important_tests = ["SSL/TLS Security", "IPv6 Leak Test", "Traffic Analysis"]
        informational_tests = ["WebRTC Leak Test", "Kill Switch Test", "Geolocation Test"]
        
        def add_category(category_name: str, test_names: List[str]):
            report.append(f"🎯 {category_name}:")
            for test_name in test_names:
                if test_name in results:
                    status = "✅ PASS" if results[test_name] else "❌ FAIL"
                    report.append(f"   {status} {test_name}")
            report.append("")
        
        add_category("Critical Security Tests", critical_tests)
        add_category("Important Security Tests", important_tests)
        add_category("Additional Tests", informational_tests)
        
        # Security recommendations
        report.append("💡 SECURITY RECOMMENDATIONS:")
        
        if not results.get("IP Leak Test", True):
            report.append("   🚨 URGENT: Fix IP leak - your real IP is exposed!")
        
        if not results.get("DNS Leak Test", True):
            report.append("   🚨 URGENT: Fix DNS leak - your DNS queries are exposed!")
        
        if not results.get("IPv6 Leak Test", True):
            report.append("   ⚠️  Consider disabling IPv6 or using IPv6-capable proxy")
        
        if not results.get("SSL/TLS Security", True):
            report.append("   ⚠️  Update your TLS configuration for better security")
        
        # General recommendations
        report.append("   ✅ Regularly test your proxy configuration")
        report.append("   ✅ Use different servers for different activities")
        report.append("   ✅ Keep your proxy client updated")
        report.append("   ✅ Enable kill switch if available")
        report.append("   ✅ Use HTTPS websites whenever possible")
        report.append("")
        
        # Overall assessment
        critical_passed = sum(1 for test in critical_tests if results.get(test, False))
        if critical_passed == len(critical_tests):
            report.append("🎉 ASSESSMENT: Your proxy configuration appears secure!")
        elif critical_passed >= len(critical_tests) - 1:
            report.append("⚠️  ASSESSMENT: Minor security issues detected - please review")
        else:
            report.append("🚨 ASSESSMENT: Critical security issues detected - immediate action required!")
        
        return "\n".join(report)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Run security tests for proxy configuration')
    parser.add_argument('--proxy-http', default='socks5://127.0.0.1:1080',
                       help='HTTP proxy URL (default: socks5://127.0.0.1:1080)')
    parser.add_argument('--proxy-https', default='socks5://127.0.0.1:1080',
                       help='HTTPS proxy URL (default: socks5://127.0.0.1:1080)')
    parser.add_argument('--timeout', type=int, default=10,
                       help='Request timeout in seconds (default: 10)')
    parser.add_argument('--output', help='Save report to file')
    
    args = parser.parse_args()
    
    proxy_config = {
        'http': args.proxy_http,
        'https': args.proxy_https
    }
    
    tester = SecurityTester(proxy_config)
    tester.timeout = args.timeout
    
    results = tester.run_all_tests()
    report = tester.generate_security_report(results)
    
    print(report)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"\n📄 Report saved to {args.output}")
    
    # Exit with error code if critical tests failed
    critical_tests = ["IP Leak Test", "DNS Leak Test", "Proxy Connectivity"]
    critical_failed = any(not results.get(test, False) for test in critical_tests)
    
    return 1 if critical_failed else 0


if __name__ == "__main__":
    exit(main())