#!/usr/bin/env python3
"""
pyhttpx-pro - A Python HTTP probing tool inspired by httpx and httprobe

Features:
- Fast HTTP/HTTPS probing
- Multiple probes (status, title, content-length, etc.)
- Concurrency support
- Custom ports and protocols
- Output in various formats
- Matchers and filters
"""

import argparse
import concurrent.futures
import csv
import json
import re
import sys
import time
import socket
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
import mmh3
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)


def print_banner():
    """Print the colorful banner"""
    try:
        banner = f"""
{Fore.CYAN}{'='*60}
{Style.BRIGHT}{Fore.MAGENTA}        _____ _   _ _____ _____ _   _ _____ _____
{Style.BRIGHT}{Fore.MAGENTA}       |  _  | | | |_   _|  _  | | | |_   _|  _  |
{Style.BRIGHT}{Fore.MAGENTA}       | | | | |_| | | | | | | | | | | | | | | | |
{Style.BRIGHT}{Fore.MAGENTA}       | | | |  _  | | | | | | | | | | | | | | | |
{Style.BRIGHT}{Fore.MAGENTA}       | |_| | | | |_| |_| |_| |_| |_| |_| |_| |
{Style.BRIGHT}{Fore.MAGENTA}       |_____| |_| |_____|_____| |_| |_____|_____|
{Fore.CYAN}{'='*60}
{Style.BRIGHT}{Fore.YELLOW}                    HTTP Probing Tool v6.0.0
{Style.BRIGHT}{Fore.GREEN}                Author: ArkhAngelLifeJiggy
{Style.BRIGHT}{Fore.BLUE}        Inspired by httpx & httprobe | Fast & Reliable
{Fore.CYAN}{'='*60}
{Style.BRIGHT}{Fore.WHITE}Features:
{Style.BRIGHT}{Fore.GREEN}• {Fore.WHITE}Fast HTTP/HTTPS probing with concurrency
{Style.BRIGHT}{Fore.GREEN}• {Fore.WHITE}Multiple probes (status, title, content-length, etc.)
{Style.BRIGHT}{Fore.GREEN}• {Fore.WHITE}Custom ports, headers, and user agents
{Style.BRIGHT}{Fore.GREEN}• {Fore.WHITE}JSON, CSV, and colored text output
{Style.BRIGHT}{Fore.GREEN}• {Fore.WHITE}Proxy support and SSL verification control
{Style.BRIGHT}{Fore.GREEN}• {Fore.WHITE}Rate limiting and timeout configuration
{Fore.CYAN}{'='*60}
"""
        print(banner)
    except UnicodeEncodeError:
        # Fallback for systems that don't support Unicode
        simple_banner = """
============================================================
        _____ _   _ _____ _____ _   _ _____ _____
       |  _  | | | |_   _|  _  | | | |_   _|  _  |
       | | | | |_| | | | | | | | | | | | | | | | |
       | | | |  _  | | | | | | | | | | | | | | | |
       | |_| | | | |_| |_| |_| |_| |_| |_| |_| |
       |_____| |_| |_____|_____| |_| |_____|_____|
============================================================
                    HTTP Probing Tool v6.0.0
                Author: ArkhAngelLifeJiggy
        Inspired by httpx & httprobe | Fast & Reliable
============================================================
Features:
• Fast HTTP/HTTPS probing with concurrency
• Multiple probes (status, title, content-length, etc.)
• Custom ports, headers, and user agents
• JSON, CSV, and colored text output
• Proxy support and SSL verification control
• Rate limiting and timeout configuration
============================================================
"""
        print(simple_banner)


class ProbeResult:
    """Represents the result of probing a URL"""

    def __init__(self, url: str):
        self.url = url
        self.status_code: Optional[int] = None
        self.title: Optional[str] = None
        self.content_length: Optional[int] = None
        self.content_type: Optional[str] = None
        self.server: Optional[str] = None
        self.response_time: Optional[float] = None
        self.ip: Optional[str] = None
        self.cname: Optional[str] = None
        self.webserver: Optional[str] = None
        self.websocket: bool = False
        self.http2: bool = False
        self.tls: bool = False
        self.body_hash: Optional[str] = None
        self.header_hash: Optional[str] = None
        self.favicon_hash: Optional[int] = None
        self.line_count: Optional[int] = None
        self.word_count: Optional[int] = None
        self.location: Optional[str] = None
        self.asn: Optional[str] = None
        self.cdn: Optional[str] = None
        self.probe_status: bool = False
        self.error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'url': self.url,
            'status_code': self.status_code,
            'title': self.title,
            'content_length': self.content_length,
            'content_type': self.content_type,
            'server': self.server,
            'response_time': self.response_time,
            'ip': self.ip,
            'cname': self.cname,
            'webserver': self.webserver,
            'websocket': self.websocket,
            'http2': self.http2,
            'tls': self.tls,
            'body_hash': self.body_hash,
            'header_hash': self.header_hash,
            'favicon_hash': self.favicon_hash,
            'line_count': self.line_count,
            'word_count': self.word_count,
            'location': self.location,
            'asn': self.asn,
            'cdn': self.cdn,
            'probe_status': self.probe_status,
            'error': self.error
        }


class HTTPProber:
    """Main HTTP probing class"""

    def __init__(self, args: argparse.Namespace):
        try:
            self.args = args
            # Optimize session configuration for performance
            self.session = requests.Session()

            # Connection pooling for better performance
            adapter = requests.adapters.HTTPAdapter(
                pool_connections=args.threads,
                pool_maxsize=args.threads * 2,
                max_retries=0,  # We handle retries ourselves
                pool_block=False
            )
            self.session.mount('http://', adapter)
            self.session.mount('https://', adapter)

            self.session.timeout = args.timeout
            # Allow at least 1 redirect for HTTPS fallback, but respect user setting
            min_redirects = 1 if not args.follow_redirects else args.max_redirects
            self.session.max_redirects = min_redirects

            # Configure headers
            headers = {
                'User-Agent': args.user_agent or 'pyhttpx/5.0.0',
                'Connection': 'keep-alive',  # Changed to keep-alive for connection reuse
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            if args.header:
                for header in args.header:
                    try:
                        key, value = header.split(':', 1)
                        headers[key.strip()] = value.strip()
                    except ValueError:
                        print(f"{Fore.YELLOW}[!] Warning: Invalid header format '{header}', skipping{Style.RESET_ALL}")
            self.session.headers.update(headers)

            # Configure proxies
            if args.proxy:
                self.session.proxies = {'http': args.proxy, 'https': args.proxy}

            # Disable SSL verification if requested
            if args.insecure:
                self.session.verify = False
                # Suppress SSL warnings
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        except Exception as e:
            raise RuntimeError(f"Failed to initialize HTTP prober: {str(e)}")

    def probe_url(self, url: str) -> ProbeResult:
        """Probe a single URL and return results"""
        result = ProbeResult(url)
        start_time = time.time()

        try:
            response = self.session.get(url, allow_redirects=self.args.follow_redirects)
            result.response_time = time.time() - start_time
            result.status_code = response.status_code
            result.content_length = len(response.content)
            result.content_type = response.headers.get('Content-Type', '')
            result.server = response.headers.get('Server', '')
            result.location = response.headers.get('Location', '')
            result.probe_status = True

            # Parse title with error handling
            if 'text/html' in result.content_type.lower():
                try:
                    text = response.content.decode(response.encoding or 'utf-8', errors='ignore')
                    soup = BeautifulSoup(text, 'html.parser')
                    title_tag = soup.find('title')
                    if title_tag:
                        result.title = title_tag.get_text().strip()
                except Exception as e:
                    # Silently handle title parsing errors
                    pass

            # Calculate hashes with error handling
            if self.args.hash:
                try:
                    import hashlib
                    if 'md5' in self.args.hash:
                        result.body_hash = hashlib.md5(response.content).hexdigest()
                    if 'sha256' in self.args.hash:
                        result.body_hash = hashlib.sha256(response.content).hexdigest()
                except Exception as e:
                    # Silently handle hash calculation errors
                    pass

            # Favicon hash with comprehensive error handling
            if self.args.favicon:
                try:
                    favicon_url = urljoin(url, '/favicon.ico')
                    favicon_response = self.session.get(favicon_url, timeout=5)
                    if favicon_response.status_code == 200 and favicon_response.content:
                        result.favicon_hash = mmh3.hash(favicon_response.content)
                except Exception as e:
                    # Silently handle favicon errors
                    pass

            # Get IP address with error handling
            if self.args.ip:
                try:
                    parsed_url = urlparse(url)
                    hostname = parsed_url.hostname
                    if hostname:
                        result.ip = socket.gethostbyname(hostname)
                except Exception as e:
                    # Silently handle DNS resolution errors
                    pass

            # Line and word count with error handling
            if self.args.line_count or self.args.word_count:
                try:
                    text = response.text
                    result.line_count = len(text.splitlines())
                    result.word_count = len(text.split())
                except Exception as e:
                    # Silently handle text processing errors
                    pass

        except requests.exceptions.Timeout:
            result.error = "Request timeout"
            result.response_time = time.time() - start_time
        except requests.exceptions.ConnectionError:
            result.error = "Connection failed"
            result.response_time = time.time() - start_time
        except requests.exceptions.TooManyRedirects:
            result.error = "Too many redirects"
            result.response_time = time.time() - start_time
        except requests.exceptions.RequestException as e:
            result.error = f"Request error: {str(e)}"
            result.response_time = time.time() - start_time
        except Exception as e:
            result.error = f"Unexpected error: {str(e)}"
            result.response_time = time.time() - start_time

        return result

    def probe_targets(self, targets: List[str]) -> List[ProbeResult]:
        """Probe multiple targets with concurrency, rate limiting, and error handling"""
        results = []
        rate_limiter = None

        # Setup rate limiting if specified
        if hasattr(self.args, 'rate_limit') and self.args.rate_limit:
            try:
                import time
                rate_limiter = {'last_request': 0, 'interval': 1.0 / self.args.rate_limit}
            except Exception:
                pass

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.args.threads) as executor:
                future_to_url = {executor.submit(self.probe_url, target): target for target in targets}
                for future in concurrent.futures.as_completed(future_to_url):
                    try:
                        # Apply rate limiting if configured
                        if rate_limiter:
                            current_time = time.time()
                            time_since_last = current_time - rate_limiter['last_request']
                            if time_since_last < rate_limiter['interval']:
                                time.sleep(rate_limiter['interval'] - time_since_last)
                            rate_limiter['last_request'] = time.time()

                        # Apply delay between requests if specified
                        if hasattr(self.args, 'delay') and self.args.delay > 0:
                            time.sleep(self.args.delay)

                        result = future.result(timeout=30)  # Add timeout for individual futures
                        results.append(result)
                    except concurrent.futures.TimeoutError:
                        target_url = future_to_url[future]
                        error_result = ProbeResult(target_url)
                        error_result.error = "Probe timeout"
                        results.append(error_result)
                    except Exception as e:
                        target_url = future_to_url[future]
                        error_result = ProbeResult(target_url)
                        error_result.error = f"Probe failed: {str(e)}"
                        results.append(error_result)
        except Exception as e:
            # Fallback to sequential processing if threading fails
            print(f"{Fore.YELLOW}[!] Threading failed, falling back to sequential processing: {str(e)}{Style.RESET_ALL}")
            for target in targets:
                try:
                    # Apply rate limiting for sequential mode too
                    if rate_limiter:
                        current_time = time.time()
                        time_since_last = current_time - rate_limiter['last_request']
                        if time_since_last < rate_limiter['interval']:
                            time.sleep(rate_limiter['interval'] - time_since_last)
                        rate_limiter['last_request'] = time.time()

                    if hasattr(self.args, 'delay') and self.args.delay > 0:
                        time.sleep(self.args.delay)

                    result = self.probe_url(target)
                    results.append(result)
                except Exception as e:
                    error_result = ProbeResult(target)
                    error_result.error = f"Sequential probe failed: {str(e)}"
                    results.append(error_result)

        return results


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='pyhttpx-pro - Fast HTTP probing tool')

    # Input options
    parser.add_argument('-u', '--target', nargs='+', help='Target URLs to probe')
    parser.add_argument('-l', '--list', help='File containing list of targets')
    parser.add_argument('-p', '--ports', default=['80', '443'], nargs='+',
                       help='Ports to probe (default: 80 443)')

    # Probe options
    parser.add_argument('-sc', '--status-code', action='store_true', help='Display status code')
    parser.add_argument('-cl', '--content-length', action='store_true', help='Display content length')
    parser.add_argument('-ct', '--content-type', action='store_true', help='Display content type')
    parser.add_argument('-title', action='store_true', help='Display page title')
    parser.add_argument('-server', action='store_true', help='Display server header')
    parser.add_argument('-rt', '--response-time', action='store_true', help='Display response time')
    parser.add_argument('-ip', action='store_true', help='Display host IP')
    parser.add_argument('-hash', nargs='+', help='Display response body hash (md5, sha256)')
    parser.add_argument('-favicon', action='store_true', help='Display favicon hash')
    parser.add_argument('-lc', '--line-count', action='store_true', help='Display line count')
    parser.add_argument('-wc', '--word-count', action='store_true', help='Display word count')
    parser.add_argument('-location', action='store_true', help='Display redirect location')

    # Request options
    parser.add_argument('-H', '--header', action='append', help='Custom headers')
    parser.add_argument('-timeout', type=int, default=10, help='Request timeout in seconds')
    parser.add_argument('-proxy', help='HTTP proxy to use')
    parser.add_argument('-insecure', action='store_true', help='Skip SSL verification')
    parser.add_argument('-follow-redirects', action='store_true', help='Follow HTTP redirects')
    parser.add_argument('-max-redirects', type=int, default=10, help='Maximum redirects to follow')
    parser.add_argument('-user-agent', help='Custom User-Agent string')

    # Performance options
    parser.add_argument('-t', '--threads', type=int, default=50, help='Number of threads (default: 50)')
    parser.add_argument('-rl', '--rate-limit', type=int, help='Rate limit requests per second')
    parser.add_argument('-delay', type=float, default=0, help='Delay between requests in seconds (default: 0)')

    # Output options
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-j', '--json', action='store_true', help='Output in JSON format')
    parser.add_argument('-csv', action='store_true', help='Output in CSV format')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode (no banner)')

    return parser.parse_args()


def get_targets(args: argparse.Namespace) -> List[str]:
    """Get list of targets from arguments or stdin with comprehensive error handling"""
    targets = []

    try:
        if args.target:
            targets.extend(args.target)
    except Exception as e:
        print(f"{Fore.RED}[-] Error processing target arguments: {str(e)}{Style.RESET_ALL}", file=sys.stderr)
        return []

    try:
        if args.list:
            with open(args.list, 'r', encoding='utf-8', errors='ignore') as f:
                targets.extend(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        print(f"{Fore.RED}[-] Target list file not found: {args.list}{Style.RESET_ALL}", file=sys.stderr)
        return []
    except PermissionError:
        print(f"{Fore.RED}[-] Permission denied reading target list: {args.list}{Style.RESET_ALL}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"{Fore.RED}[-] Error reading target list: {str(e)}{Style.RESET_ALL}", file=sys.stderr)
        return []

    if not targets:
        try:
            # Try to read from stdin
            if not sys.stdin.isatty():
                stdin_data = sys.stdin.read().strip()
                if stdin_data:
                    targets.extend(line.strip() for line in stdin_data.split('\n') if line.strip())
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Warning: Could not read from stdin: {str(e)}{Style.RESET_ALL}", file=sys.stderr)

    # Generate URLs with different schemes and ports
    urls = []
    try:
        for target in targets:
            try:
                if '://' not in target:
                    # Add http and https for each port
                    for port in args.ports:
                        if port == '443':
                            urls.append(f'https://{target}')
                        elif port == '80':
                            urls.append(f'http://{target}')
                        else:
                            urls.append(f'http://{target}:{port}')
                            urls.append(f'https://{target}:{port}')
                else:
                    urls.append(target)
            except Exception as e:
                print(f"{Fore.YELLOW}[!] Warning: Could not process target '{target}': {str(e)}{Style.RESET_ALL}", file=sys.stderr)
    except Exception as e:
        print(f"{Fore.RED}[-] Error generating URLs: {str(e)}{Style.RESET_ALL}", file=sys.stderr)
        return []

    return urls


def output_results(results: List[ProbeResult], args: argparse.Namespace):
    """Output results in specified format with error handling"""
    try:
        if args.json:
            for result in results:
                if result.probe_status or args.verbose:
                    try:
                        print(json.dumps(result.to_dict(), ensure_ascii=False))
                    except Exception as e:
                        print(f"{Fore.RED}[-] Error outputting JSON for {result.url}: {str(e)}{Style.RESET_ALL}", file=sys.stderr)
        elif args.csv:
            if results:
                try:
                    writer = csv.DictWriter(sys.stdout, fieldnames=results[0].to_dict().keys())
                    writer.writeheader()
                    for result in results:
                        if result.probe_status or args.verbose:
                            try:
                                writer.writerow(result.to_dict())
                            except Exception as e:
                                print(f"{Fore.RED}[-] Error writing CSV row for {result.url}: {str(e)}{Style.RESET_ALL}", file=sys.stderr)
                except Exception as e:
                    print(f"{Fore.RED}[-] Error creating CSV output: {str(e)}{Style.RESET_ALL}", file=sys.stderr)
        else:
            # Default colored text output
            for result in results:
                try:
                    if result.probe_status:
                        # Color code based on status
                        if result.status_code and 200 <= result.status_code < 300:
                            status_color = Fore.GREEN
                        elif result.status_code and 300 <= result.status_code < 400:
                            status_color = Fore.YELLOW
                        elif result.status_code and 400 <= result.status_code < 500:
                            status_color = Fore.RED
                        elif result.status_code and 500 <= result.status_code < 600:
                            status_color = Fore.MAGENTA
                        else:
                            status_color = Fore.WHITE

                        output = f"{Fore.CYAN}{result.url}{Style.RESET_ALL}"

                        if args.status_code and result.status_code:
                            output += f" {status_color}[{result.status_code}]{Style.RESET_ALL}"

                        if args.content_length and result.content_length:
                            output += f" {Fore.BLUE}[{result.content_length}]{Style.RESET_ALL}"

                        if args.title and result.title:
                            # Truncate long titles
                            title = result.title[:50] + "..." if len(result.title) > 50 else result.title
                            output += f" {Fore.MAGENTA}[{title}]{Style.RESET_ALL}"

                        if args.server and result.server:
                            output += f" {Fore.YELLOW}[{result.server}]{Style.RESET_ALL}"

                        if args.response_time and result.response_time:
                            # Color response time based on speed
                            if result.response_time < 1:
                                time_color = Fore.GREEN
                            elif result.response_time < 3:
                                time_color = Fore.YELLOW
                            else:
                                time_color = Fore.RED
                            output += f" {time_color}[{result.response_time:.2f}s]{Style.RESET_ALL}"

                        print(output)
                    elif args.verbose and result.error:
                        print(f"{Fore.CYAN}{result.url}{Style.RESET_ALL} {Fore.RED}[ERROR: {result.error}]{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[-] Error displaying result for {result.url}: {str(e)}{Style.RESET_ALL}", file=sys.stderr)
    except Exception as e:
        print(f"{Fore.RED}[-] Fatal error in output: {str(e)}{Style.RESET_ALL}", file=sys.stderr)


def main():
    """Main function with comprehensive error handling"""
    try:
        # Print banner unless silent mode
        args = parse_arguments()
        if not hasattr(args, 'silent') or not args.silent:
            print_banner()

        targets = get_targets(args)

        if not targets:
            print(f"{Fore.RED}[-] No targets specified. Use -u, -l, or pipe targets to stdin.{Style.RESET_ALL}", file=sys.stderr)
            sys.exit(1)

        print(f"{Fore.BLUE}[+] Starting probe of {len(targets)} targets with {args.threads} threads...{Style.RESET_ALL}")

        start_time = time.time()
        prober = HTTPProber(args)
        results = prober.probe_targets(targets)
        end_time = time.time()

        successful_probes = sum(1 for r in results if r.probe_status)
        print(f"{Fore.GREEN}[+] Completed in {end_time - start_time:.2f}s - {successful_probes}/{len(results)} targets responded{Style.RESET_ALL}")

        if args.output:
            try:
                print(f"{Fore.BLUE}[+] Saving results to {args.output}...{Style.RESET_ALL}")
                with open(args.output, 'w', encoding='utf-8') as f:
                    if args.json:
                        for result in results:
                            f.write(json.dumps(result.to_dict(), ensure_ascii=False) + '\n')
                    else:
                        for result in results:
                            if result.probe_status:
                                f.write(result.url + '\n')
                print(f"{Fore.GREEN}[+] Results saved successfully!{Style.RESET_ALL}")
            except PermissionError:
                print(f"{Fore.RED}[-] Permission denied writing to {args.output}{Style.RESET_ALL}", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"{Fore.RED}[-] Error saving results: {str(e)}{Style.RESET_ALL}", file=sys.stderr)
                sys.exit(1)
        else:
            output_results(results, args)

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Operation cancelled by user{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"{Fore.RED}[-] Fatal error: {str(e)}{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()