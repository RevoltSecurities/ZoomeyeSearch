from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

class Helper:
    def __init__(self) -> None:
        self.console = Console()
        
    def main_help(self):
        self.console.print(Panel.fit(
            Text("ZOOMEYE 🔎 HELP", justify="center", style="bold blue"),
            border_style="blue",
            padding=(1, 4)
        ))

        self.console.print("[bold blue]DESCRIPTION[/bold blue]")
        self.console.print(
            "[bold white]\nZoomEye is a powerful cybersecurity search engine that enables searching for exposed devices, services, and vulnerabilities.\n"
            "This CLI tool provides programmatic access to ZoomEye's capabilities for reconnaissance and threat intelligence.\n[/bold white]"
        )

        self.console.print("[bold blue]GLOBAL OPTIONS[/bold blue]\n")
        global_table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        global_table.add_column("Option", style="bold cyan", no_wrap=True)
        global_table.add_column("Description", style="bold white")

        globals = [
            ("-fields, --fields", "Comma-separated list of fields to return in results"),
            ("-facet, --facet", "Comma-separated list of facets to group results by"),
            ("-mp, --max-page", "Maximum number of pages to fetch (default: 5)"),
            ("-limit, --limit", "Maximum number of results to fetch (default: 2000)"),
            ("-o, --output", "Output file to save results "),
        ]
        for opt, desc in globals:
            global_table.add_row(opt, desc)
        self.console.print(global_table)

        self.console.print("[bold blue]MODES (zoomeye <global-options> <mode>)[/bold blue]\n")
        mode_table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        mode_table.add_column("Mode", style="bold cyan", no_wrap=True)
        mode_table.add_column("Description", style="bold white")

        modes = [
            ("auth", "Configure and save your ZoomEye API key for authenticated access"),
            ("login", "Verify your ZoomEye access level and API key validity"),
            ("asn", "Search by Autonomous System Number (ASN)"),
            ("ip", "Search by IP address"),
            ("domain", "Search by domain name"),
            ("org", "Search by organization name"),
            ("cidr", "Search by CIDR range"),
            ("service", "Search by service name"),
            ("product", "Search by product name"),
            ("enumerate", "Enumerate subdomains or associated domains"),
            ("geosearch", "Search by geographic location (country, city, subdivision)"),
            ("faviconhash", "Search by favicon hash"),
            ("ssl", "Advanced SSL certificate search"),
            ("stats", "Get statistics for a specific field"),
            ("search", "Perform a raw ZoomEye search query"),
            ("gpt", "Access ZoomEye GPT features"),
            ("update", "Check for updates to the ZoomEyesearch CLI tool"),
        ]
        for mode, desc in modes:
            mode_table.add_row(mode, desc)
        self.console.print(mode_table)

        self.console.print("[bold blue]USAGE[/bold blue]")
        self.console.print("[bold white]zoomeye <global-options> <mode> [options][/bold white]\n")

    def _print_mode_help(self, title: str, description: str, flags: list, examples: list = None):
        self.console.print(Panel.fit(
            Text(title, justify="center", style="bold blue"),
            border_style="blue",
            padding=(1, 4)
        ))
        self.console.print(f"[bold blue]DESCRIPTION[/bold blue]\n[bold white]{description}[/bold white]\n")

        self.console.print("[bold blue]FLAGS[/bold blue]")
        flag_table = Table(show_header=True, header_style="bold magenta")
        flag_table.add_column("Flag", style="bold cyan", no_wrap=True)
        flag_table.add_column("Description", style="bold white")
        for flag, desc in flags:
            flag_table.add_row(flag, desc)
        self.console.print(flag_table)

        if examples:
            self.console.print("\n[bold blue]EXAMPLES[/bold blue]")
            for example in examples:
                self.console.print(f"[bold white]{example}[/bold white]")

    def help_asn(self):
        self._print_mode_help(
            "ASN MODE",
            "Search by Autonomous System Number (ASN) to find all assets belonging to a specific network.",
            [
                ("-asn, --asn", "The Autonomous System Number to search for (e.g., AS15169)"),
            ],
            [
                "zoomeye asn -asn 15169",
                "zoomeye --fields ip,port,org asn -asn 15169 --limit 500"
            ]
        )

    def help_ip(self):
        self._print_mode_help(
            "IP MODE",
            "Search for information about a specific IP address in ZoomEye's database.",
            [
                ("-ip, --ip", "The IP address to search for"),
            ],
            [
                "zoomeye ip -ip 8.8.8.8",
                "zoomeye --fields port,service,product ip -ip 1.1.1.1"
            ]
        )

    def help_domain(self):
        self._print_mode_help(
            "DOMAIN MODE",
            "Search for assets associated with a specific domain name.",
            [
                ("-d, --domain", "The domain name to search for"),
            ],
            [
                "zoomeye domain -d hackerone.com ",
                "zoomeye --limit 10 domain -d google.com"
            ]
        )

    def help_org(self):
        self._print_mode_help(
            "ORG MODE",
            "Search for assets belonging to a specific organization.",
            [
                ("-org, --org", "The organization name to search for"),
            ],
            [
                "zoomeye org -org \"Google LLC\"",
                "zoomeye --max-page 10 org -org \"Amazon\""
            ]
        )

    def help_cidr(self):
        self._print_mode_help(
            "CIDR MODE",
            "Search for assets within a specific CIDR range.",
            [
                ("-cidr, --cidr", "The CIDR range to search (e.g., 192.168.1.0/24)"),
            ],
            [
                "zoomeye cidr --cidr 192.168.1.0/24",
                "zoomeye --limit 1000 cidr --cidr 8.8.8.0/24"
            ]
        )

    def help_service(self):
        self._print_mode_help(
            "SERVICE MODE",
            "Search for assets running a specific service.",
            [
                ("-sV, --service", "The service name to search for (e.g., http, ssh, mysql)"),
            ],
            [
                "zoomeye service -sV http",
                "zoomeye --facet country,org service -sV ssh"
            ]
        )

    def help_product(self):
        self._print_mode_help(
            "PRODUCT MODE",
            "Search for assets running a specific product.",
            [
                ("-pd, --product", "The product name to search for (e.g., nginx, apache, mysql)"),
            ],
            [
                "zoomeye product -pd nginx",
                "zoomeye --max-page 3 product -pd \"Apache httpd\""
            ]
        )

    def help_enumerate(self):
        self._print_mode_help(
            "ENUMERATE MODE",
            "Discover subdomains or associated domains for a target domain.",
            [
                ("-d, --domain", "The domain to enumerate"),
                ("-as, --associated-domain", "Search for associated domains instead of subdomains"),
                ("-sub, --subdomain", "Search for subdomains (default)"),
            ],
            [
                "zoomeye enumerate -d example.com",
                "zoomeye enumerate -d example.com --associated-domain",
                "zoomeye enumerate -d example.com --subdomain"
            ]
        )

    def help_geosearch(self):
        self._print_mode_help(
            "GEOSEARCH MODE",
            "Search for assets in specific geographic locations.",
            [
                ("-country, --country", "Search by country name or code"),
                ("-city, --city", "Search by city name"),
                ("-subdivision, --subdivision", "Search by state/province name"),
            ],
            [
                "zoomeye geosearch --country US",
                "zoomeye geosearch --country CN --city Beijing",
                "zoomeye --max-page 10 geosearch --subdivision California"
            ]
        )

    def help_faviconhash(self):
        self._print_mode_help(
            "FAVICONHASH MODE",
            "Search for assets using a specific favicon hash.",
            [
                ("-hash, --faviconhash", "The favicon hash to search for"),
            ],
            [
                "zoomeye faviconhash -hash -1234567890",
                "zoomeye --fields ip,port,title faviconhash -hash 1234567890 "
            ]
        )

    def help_ssl(self):
        self._print_mode_help(
            "SSL MODE",
            "Advanced search using SSL certificate attributes.",
            [
            ("--ssl", "Search by SSL certificate subject or issuer"),
            ("--fingerprint", "SSL certificate fingerprint (SHA-1)"),
            ("--chain-count", "Number of certificates in the chain"),
            ("--alg", "Certificate algorithm (e.g., RSA, ECDSA)"),
            ("--issuer-cn", "Issuer Common Name (e.g., 'Let's Encrypt')"),
            ("--rsa-bits", "RSA key size in bits (e.g., 2048, 4096)"),
            ("--ecdsa-bits", "ECDSA key size in bits (e.g., 256, 384)"),
            ("--pubkey-type", "Public key type (rsa/ecdsa/dsa)"),
            ("--serial", "Certificate serial number"),
            ("--cipher-bits", "TLS cipher strength in bits"),
            ("--cipher-name", "TLS cipher name (e.g., 'AES256-GCM-SHA384')"),
            ("--cipher-version", "TLS cipher version"),
            ("--ssl-version", "SSL/TLS version (e.g., TLSv1.2, TLSv1.3)"),
            ("--subject-cn", "Subject Common Name (target domain)"),
            ("--jarm", "JARM fingerprint for TLS server identification"),
            ("--ja3s", "JA3S fingerprint for TLS client identification"),
            ("-h, --help", "Show this help message"),
            ],
            [
                "zoomeye ssl --jarm 1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d",
                "zoomeye ssl --subject-cn \"example.com\"",
                "zoomeye ssl --fingerprint abc123def456"
            ]
        )

    def help_stats(self):
        self._print_mode_help(
            "STATS MODE",
            "Get statistics for a specific field in the results of a query.",
            [
                ("--query", "The search query to analyze"),
                ("--field", "The field to generate statistics for"),
            ],
            [
                "zoomeye stats --query \"product:nginx\" --field country",
                "zoomeye stats --query \"service:http\" --field org"
            ]
        )

    def help_search(self):
        self._print_mode_help(
            "SEARCH MODE",
            "Perform a raw search query using ZoomEye's search syntax.",
            [
                ("-sc, --search", "The raw search query to execute"),
            ],
            [
                "zoomeye search -sc \"country:CN\"",
                "zoomeye --limit 5000 search -sc \"os:linux\" "
            ]
        )

    def help_auth(self):
        self._print_mode_help(
            "AUTH MODE",
            "Configure and save your ZoomEye API key for authenticated access.",
            [],
            [
                "zoomeye auth"
            ]
        )

    def help_login(self):
        self._print_mode_help(
            "LOGIN MODE",
            "Verify your ZoomEye access level and API key validity.",
            [],
            [
                "zoomeye login"
            ]
        )

    def help_gpt(self):
        self._print_mode_help(
            "GPT MODE",
            "Access ZoomEye GPT to generate and search zoomeye queries using ZOOMEYE's AI capabilities.",
            [
            ],
            [
                "zoomeye gpt"
            ]
        )
        
    def help_update(self):
        self._print_mode_help(
            "UPDATE MODE",
            "Check for updates to the ZoomEyeSearch CLI tool.",
            [
                ('-h', '--help', 'Show this help message'),
                ('-sup', '--show-update', 'Show the latest update information'),
                ('-up', '--update', 'Update the ZoomEyeSearch CLI tool to the latest version'),
            ],
            [
                "zoomeye update"
            ]
        )