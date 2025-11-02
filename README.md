# pyhttpx

[![PyPI](https://img.shields.io/pypi/v/pyhttpx.svg)](https://pypi.org/project/pyhttpx/)
[![Python](https://img.shields.io/pypi/pyversions/pyhttpx.svg)](https://pypi.org/project/pyhttpx/)
[![Downloads](https://img.shields.io/pypi/dm/pyhttpx.svg)](https://pypi.org/project/pyhttpx/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-5.0.0-orange.svg)](https://github.com/LifeJiggy/pyhttpx-pro)

A fast and multi-purpose HTTP toolkit written in Python, inspired by [httpx](https://github.com/projectdiscovery/httpx) and [httprobe](https://github.com/tomnomnom/httprobe). Designed for security researchers, penetration testers, and developers who need to quickly probe and analyze web endpoints.

## ✨ Features

- 🚀 **Fast HTTP/HTTPS probing** with concurrent requests
- 🎯 **Multiple probes**: status code, title, content-length, server, response time, etc.
- 🌐 **Custom ports and protocols** support
- 📊 **Multiple output formats**: JSON, CSV, and colored text
- 🔧 **Flexible configuration**: custom headers, user agents, proxies
- ⚡ **High performance**: configurable threading and rate limiting
- 🎨 **Colorful output** for better user experience
- 🔒 **SSL/TLS support** with verification control

## 📦 Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Install from PyPI (Recommended)
```bash
pip install pyhttpx-pro
```

### Install from source
```bash
git clone https://github.com/LifeJiggy/pyhttpx-pro.git
cd pyhttpx-pro
pip install -r requirements.txt
```

### Direct usage (Development)
```bash
# Install dependencies
pip install requests beautifulsoup4 mmh3 colorama

# Run the tool
python pyhttpx-pro.py -u example.com
```

### Verify Installation
```bash
pyhttpx-pro --help
# or
python -c "import pyhttpx-pro; print('pyhttpx-pro installed successfully!')"
```

## 🚀 Usage

### Basic Usage

```bash
# Probe a single target
python pyhttpx-pro.py -u example.com

# Probe multiple targets
python pyhttpx-pro.py -u example.com google.com github.com

# Read targets from file
python pyhttpx-pro.py -l targets.txt

# Read from stdin
echo "example.com" | python pyhttpx-pro.py
cat targets.txt | python pyhttpx-pro.py
```

### Advanced Usage

```bash
# Probe with multiple options
python pyhttpx-pro.py -u example.com -sc -title -cl -rt -server

# Custom ports
python pyhttpx-pro.py -u example.com -p 80 443 8080 8443

# JSON output
python pyhttpx-pro.py -u example.com -j

# CSV output
python pyhttpx-pro.py -u example.com -csv

# Save to file
python pyhttpx-pro.py -u example.com -o results.txt

# Custom headers
python pyhttpx-pro.py -u example.com -H "Authorization: Bearer token" -H "X-API-Key: key"

# Use proxy
python pyhttpx-pro.py -u example.com -proxy http://127.0.0.1:8080

# Skip SSL verification
python pyhttpx-pro.py -u example.com -insecure

# Silent mode (no banner)
python pyhttpx-pro.py -u example.com -s
```

## 📋 Command Line Options

### Input Options
- `-u, --target`: Target URLs to probe
- `-l, --list`: File containing list of targets
- `-p, --ports`: Ports to probe (default: 80 443)

### Probe Options
- `-sc, --status-code`: Display response status code
- `-cl, --content-length`: Display response content length
- `-ct, --content-type`: Display response content type
- `-title`: Display page title
- `-server`: Display server header
- `-rt, --response-time`: Display response time
- `-ip`: Display host IP (planned)
- `-hash`: Display response body hash (md5, sha256)
- `-favicon`: Display favicon hash
- `-lc, --line-count`: Display response body line count
- `-wc, --word-count`: Display response body word count
- `-location`: Display redirect location

### Request Options
- `-H, --header`: Custom HTTP headers
- `-timeout`: Request timeout in seconds (default: 10)
- `-proxy`: HTTP proxy to use
- `-insecure`: Skip SSL verification
- `-follow-redirects`: Follow HTTP redirects
- `-max-redirects`: Maximum redirects to follow (default: 10)
- `-user-agent`: Custom User-Agent string

### Performance Options
- `-t, --threads`: Number of threads (default: 50)
- `-rl, --rate-limit`: Rate limit requests per second

### Output Options
- `-o, --output`: Output file
- `-j, --json`: Output in JSON format
- `-csv`: Output in CSV format
- `-v, --verbose`: Verbose output
- `-s, --silent`: Silent mode (no banner)

## 🎨 Color Coding

The tool uses colors to provide visual feedback:

- 🟢 **Green**: Successful responses (2xx status codes)
- 🟡 **Yellow**: Redirects (3xx status codes)
- 🔴 **Red**: Client errors (4xx status codes)
- 🟣 **Magenta**: Server errors (5xx status codes)
- 🔵 **Blue**: Information (content length, response time)
- 🟠 **Cyan**: URLs
- 🟣 **Magenta**: Page titles
- 🟡 **Yellow**: Server information

## 📊 Output Examples

### Default Output
```bash
python pyhttpx-pro.py -u example.com -sc -title -cl -rt
```

Output:
```
🔍 Starting probe of 2 targets with 50 threads...
✅ Completed in 1.23s - 2/2 targets responded
https://example.com [200] [1256] [Example Domain] [1.23s]
http://example.com [200] [1256] [Example Domain] [0.89s]
```

### JSON Output
```bash
python pyhttpx-pro.py -u example.com -j
```

Output:
```json
{"url": "https://example.com", "status_code": 200, "title": "Example Domain", "content_length": 1256, "content_type": "text/html", "server": "", "response_time": 1.234567, "ip": null, "cname": null, "webserver": null, "websocket": false, "http2": false, "tls": false, "body_hash": null, "header_hash": null, "favicon_hash": null, "line_count": null, "word_count": null, "location": "", "asn": null, "cdn": null, "probe_status": true, "error": null}
```

## 🔧 Configuration

### Environment Variables
- `HTTP_PROXY`: Default HTTP proxy
- `HTTPS_PROXY`: Default HTTPS proxy

### Configuration File
You can create a configuration file at `~/.pyhttpx-pro/config.yaml` for default settings.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [httpx](https://github.com/projectdiscovery/httpx) by ProjectDiscovery
- Inspired by [httprobe](https://github.com/tomnomnom/httprobe) by @tomnomnom
- Built with [requests](https://github.com/psf/requests) library

## 📞 Support

If you have any questions or issues, please open an issue on GitHub.

---

**Made with ❤️ by ArkhAngelLifeJiggy**