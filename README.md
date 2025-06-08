# zoomeyesearch
**A powerful CLI tool that uses zoomeyesearch to search exposed services, gather intelligence, and automate reconnaissance.**

![License](https://img.shields.io/github/license/RevoltSecurities/zoomeyesearch?style=flat-square)
![Python](https://img.shields.io/badge/python-3.13+-blue.svg?style=flat-square)
![zoomeyesearch API](https://img.shields.io/badge/zoomeyesearch-API-green?style=flat-square)

## Features
- Seamless authentication with zoomeyesearch credentials and API key
- Search by:
  - Domain, IP, CIDR, ASN, Organization, Service, Product
  - Geolocation, SSL Certificate, Favicon Hash
- Support for facets, custom fields, pagination, and result limits
- GPT-assisted queries (`gpt` mode)
- Save output to a file for offline analysis
- Built-in updater to get the latest CLI version



## Installation
```bash
git clone https://github.com/RevoltSecurities/zoomeyesearch.git
cd zoomeyesearch
python3 -m venv zoomeyesearch-venv
source zoomeyesearch-venv/bin/activate
pip install .
```

## Quickstart

### Authenticate
```bash
zoomeyesearch auth
```
Enter your zoomeyesearch credentials and API key when prompted.

### Verify Login
```bash
zoomeyesearch login
```

## Usage

```
GLOBAL OPTIONS

┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Option            ┃ Description                                         ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -fields, --fields │ Comma-separated list of fields to return in results │
├───────────────────┼─────────────────────────────────────────────────────┤
│ -facet, --facet   │ Comma-separated list of facets to group results by  │
├───────────────────┼─────────────────────────────────────────────────────┤
│ -mp, --max-page   │ Maximum number of pages to fetch (default: 5)       │
├───────────────────┼─────────────────────────────────────────────────────┤
│ -limit, --limit   │ Maximum number of results to fetch (default: 2000)  │
├───────────────────┼─────────────────────────────────────────────────────┤
│ -o, --output      │ Output file to save results                         │
└───────────────────┴─────────────────────────────────────────────────────┘
MODES (zoomeyesearch <global-options> <mode>)

┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Mode        ┃ Description                                                      ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ auth        │ Configure and save your zoomeyesearch API key for authenticated access │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ login       │ Verify your zoomeyesearch access level and API key validity            │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ asn         │ Search by Autonomous System Number (ASN)                         │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ ip          │ Search by IP address                                             │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ domain      │ Search by domain name                                            │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ org         │ Search by organization name                                      │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ cidr        │ Search by CIDR range                                             │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ service     │ Search by service name                                           │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ product     │ Search by product name                                           │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ enumerate   │ Enumerate subdomains or associated domains                       │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ geosearch   │ Search by geographic location (country, city, subdivision)       │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ faviconhash │ Search by favicon hash                                           │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ ssl         │ Advanced SSL certificate search                                  │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ stats       │ Get statistics for a specific field                              │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ search      │ Perform a raw zoomeyesearch search query                               │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ gpt         │ Access zoomeyesearch GPT features                                      │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ update      │ Check for updates to the zoomeyesearch CLI tool                  │
└─────────────┴──────────────────────────────────────────────────────────────────┘
USAGE
zoomeyesearch <global-options> <mode> 
```

## Available Modes

### ASN
**Search by Autonomous System Number (ASN) to find all assets belonging to a specific network.**
```
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag        ┃ Description                                                ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -asn, --asn │ The Autonomous System Number to search for (e.g., AS15169) │
└─────────────┴────────────────────────────────────────────────────────────┘

zoomeyesearch asn -asn 15169
zoomeyesearch --fields ip,port,org asn -asn 15169 --limit 500
```

### IP
**Search for information about a specific IP address in zoomeyesearch's database.**
```
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag      ┃ Description                  ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -ip, --ip │ The IP address to search for │
└───────────┴──────────────────────────────┘

zoomeyesearch ip -ip 8.8.8.8
zoomeyesearch --fields port,service,product ip -ip 1.1.1.1
```

### Domain
**Search for assets associated with a specific domain name.**
```
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag         ┃ Description                   ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -d, --domain │ The domain name to search for │
└──────────────┴───────────────────────────────┘

zoomeyesearch domain -d hackerone.com 
zoomeyesearch --limit 10 domain -d google.com
```

### Org
**Search for assets belonging to a specific organization.**
```
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag        ┃ Description                         ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -org, --org │ The organization name to search for │
└─────────────┴─────────────────────────────────────┘

zoomeyesearch org -org "Google LLC"
zoomeyesearch --max-page 10 org -org "Amazon"
```

### CIDR
**Search for assets within a specific CIDR range.**
```
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag          ┃ Description                                     ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -cidr, --cidr │ The CIDR range to search (e.g., 192.168.1.0/24) │
└───────────────┴─────────────────────────────────────────────────┘

zoomeyesearch cidr --cidr 192.168.1.0/24
zoomeyesearch --limit 1000 cidr --cidr 8.8.8.0/24
```

### Service
**Search for assets running a specific service.**
```
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag           ┃ Description                                             ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -sV, --service │ The service name to search for (e.g., http, ssh, mysql) │
└────────────────┴─────────────────────────────────────────────────────────┘

zoomeyesearch service -sV http
zoomeyesearch --facet country,org service -sV ssh
```

### Domains / Subdomains
**Discover subdomains or associated domains for a target domain.**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag                     ┃ Description                                         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -d, --domain             │ The domain to enumerate                             │
│ -as, --associated-domain │ Search for associated domains instead of subdomains │
│ -sub, --subdomain        │ Search for subdomains (default)                     │
└──────────────────────────┴─────────────────────────────────────────────────────┘

zoomeyesearch enumerate -d example.com
zoomeyesearch enumerate -d example.com --associated-domain
zoomeyesearch enumerate -d example.com --subdomain
```

### SSL
**Advanced search using SSL certificate attributes.**
```
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag             ┃ Description                                    ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ --ssl            │ Search by SSL certificate subject or issuer    │
│ --fingerprint    │ SSL certificate fingerprint (SHA-1)            │
│ --chain-count    │ Number of certificates in the chain            │
│ --alg            │ Certificate algorithm (e.g., RSA, ECDSA)       │
│ --issuer-cn      │ Issuer Common Name (e.g., 'Let's Encrypt')     │
│ --rsa-bits       │ RSA key size in bits (e.g., 2048, 4096)        │
│ --ecdsa-bits     │ ECDSA key size in bits (e.g., 256, 384)        │
│ --pubkey-type    │ Public key type (rsa/ecdsa/dsa)                │
│ --serial         │ Certificate serial number                      │
│ --cipher-bits    │ TLS cipher strength in bits                    │
│ --cipher-name    │ TLS cipher name (e.g., 'AES256-GCM-SHA384')    │
│ --cipher-version │ TLS cipher version                             │
│ --ssl-version    │ SSL/TLS version (e.g., TLSv1.2, TLSv1.3)       │
│ --subject-cn     │ Subject Common Name (target domain)            │
│ --jarm           │ JARM fingerprint for TLS server identification │
│ --ja3s           │ JA3S fingerprint for TLS client identification │
│ -h, --help       │ Show this help message                         │
└──────────────────┴────────────────────────────────────────────────┘

zoomeyesearch ssl --jarm 1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d
zoomeyesearch ssl --subject-cn "example.com"
zoomeyesearch ssl --fingerprint abc123def456
```

### Favicon
**Search for assets using a specific favicon hash.**
```
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag                 ┃ Description                    ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -hash, --faviconhash │ The favicon hash to search for │
└──────────────────────┴────────────────────────────────┘

zoomeyesearch faviconhash -hash -1234567890
zoomeyesearch --fields ip,port,title faviconhash -hash 1234567890 
```

### Search
**Perform a raw search query using zoomeyesearch's search syntax.**
```
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag          ┃ Description                     ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -sc, --search │ The raw search query to execute │
└───────────────┴─────────────────────────────────┘

zoomeyesearch search -sc "country:CN"
zoomeyesearch --limit 5000 search -sc "os:linux"
```

### Stats
**Get statistics for a specific field in the results of a query.**
```
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag    ┃ Description                          ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ --query │ The search query to analyze          │
│ --field │ The field to generate statistics for │
└─────────┴──────────────────────────────────────┘

zoomeyesearch stats --query "product:nginx" --field country
zoomeyesearch stats --query "service:http" --field org
```

### Geosearch
**Search for assets in specific geographic locations.**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag                        ┃ Description                    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -country, --country         │ Search by country name or code │
│ -city, --city               │ Search by city name            │
│ -subdivision, --subdivision │ Search by state/province name  │
└─────────────────────────────┴────────────────────────────────┘

zoomeyesearch geosearch --country US
zoomeyesearch geosearch --country CN --city Beijing
zoomeyesearch --max-page 10 geosearch --subdivision California
```

### Product
**Search for assets running a specific product.**
```
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag           ┃ Description                                                 ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -pd, --product │ The product name to search for (e.g., nginx, apache, mysql) │
└────────────────┴─────────────────────────────────────────────────────────────┘

zoomeyesearch product -pd nginx
zoomeyesearch --max-page 3 product -pd "Apache httpd"
```

## Credits & Contribution
Built by **RevoltSecurities** with ❤️
- Community contributions welcome.
- Found a bug? Want a feature? [Open an issue](https://github.com/RevoltSecurities/zoomeyesearch/issues) or [PR](https://github.com/RevoltSecurities/zoomeyesearch/pulls).

If you love the tool, support it by giving a ⭐ on GitHub!

**"The more we share, the more we grow — let’s build a powerful security community together."**
