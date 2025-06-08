# ZoomeyeSearch
**A powerful CLI tool that uses ZoomEye to search exposed services, gather intelligence, and automate reconnaissance.**

![License](https://img.shields.io/github/license/RevoltSecurities/ZoomeyeSearch?style=flat-square)
![Python](https://img.shields.io/badge/python-3.13+-blue.svg?style=flat-square)
![ZoomEye API](https://img.shields.io/badge/zoomeye-API-green?style=flat-square)


## Features
- Seamless authentication with ZoomEye credentials and API key
- Search by:
  - Domain, IP, CIDR, ASN, Organization, Service, Product
  - Geolocation, SSL Certificate, Favicon Hash
- Support for facets, custom fields, pagination, and result limits
- GPT-assisted queries (`gpt` mode)
- Save output to a file for offline analysis
- Built-in updater to get the latest CLI version
---

## Installation
```bash
git clone https://github.com/RevoltSecurities/ZoomeyeSearch.git
cd ZoomeyeSearch
python3 -m venv zoomeye-venv
source zoomeye-venv/bin/activate
pip install .
```

---

## Quickstart

### Authenticate
```bash
zoomeyesearch auth
```
Enter your ZoomEye credentials and API key when prompted.

### Verify Login
```bash
zoomeyesearch login
```

---

## Usage

```
(zoomeye-venv) pugal@ubuntu:~/tools/ZoomeyeSearch$ zoomeyesearch --help
__  /                                               ___|                            |     
   /    _ \    _ \   __ `__ \    _ \  |   |   _ \ \___ \    _ \   _` |   __|   __|  __ \  
  /    (   |  (   |  |   |   |   __/  |   |   __/       |   __/  (   |  |     (     | | | 
____| \___/  \___/  _|  _|  _| \___| \__, | \___| _____/  \___| \__,_| _|    \___| _| |_| 
                                     ____/                                                

                     - RevoltSecurities

[20:50:09]  [WARN]: unable to get the latest version of zoomeyesearch
╭───────────────────────╮
│                       │
│    ZOOMEYE 🔎 HELP    │
│                       │
╰───────────────────────╯
DESCRIPTION

ZoomEye is a powerful cybersecurity search engine that enables searching for exposed devices, services, and vulnerabilities.
This CLI tool provides programmatic access to ZoomEye's capabilities for reconnaissance and threat intelligence.

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
MODES (zoomeye <global-options> <mode>)

┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Mode        ┃ Description                                                      ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ auth        │ Configure and save your ZoomEye API key for authenticated access │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ login       │ Verify your ZoomEye access level and API key validity            │
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
│ search      │ Perform a raw ZoomEye search query                               │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ gpt         │ Access ZoomEye GPT features                                      │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ update      │ Check for updates to the ZoomEyesearch CLI tool                  │
└─────────────┴──────────────────────────────────────────────────────────────────┘
USAGE
zoomeye <global-options> <mode> 
```

---

## Example Usage

```bash
# Domain search
zoomeyesearch domain -d hackerone.com

# CIDR range search with output
zoomeyesearch --output test.txt --limit 1000 cidr --cidr 8.8.8.0/24

# Search IP with limit
zoomeyesearch --limit 10 ip --ip 8.8.8.8

# SSL certificate filter
zoomeye ssl --subject-cn "example.com"
```
---

## Support Us
**ZoomeyeSearch** is built by RevoltSecurities Team with ❤️ and your support will encourage us to improve the `ZoomeyeSearch` more and Community contributors are Welcome to contribute for `ZoomeyeSearch` and If you love the `ZoomeyeSearch` support it by giving a ⭐ .