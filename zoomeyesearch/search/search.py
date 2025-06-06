import httpx
import base64
from zoomeyesearch.logger.logger import Logger
from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.columns import Columns
from rich.text import Text
from rich.style import Style
from typing import List, Dict, Optional
from datetime import datetime

class ZoomeyeSearch():
    def __init__(
        self,
        apikey: str,
        query: str,
        fields: str,
        facet: str,
        sub_type = "web,v4,v6",
        max_page=5,
        max_size=1000,
        verbose=True
    ):
        self._url = "https://api.zoomeye.ai/v2/search"
        self.logger = Logger()
        self.apikey = apikey
        self.query = query.encode('utf-8')
        self.qbase64 = base64.b64encode(self.query).decode('utf-8')
        self.fields = fields
        self.sub_type = sub_type
        self.facet = facet
        self.max_page = max_page
        self.max_size = max_size
        self.verbose = verbose
        self.results = []
        self.headers = {
            "API-KEY": self.apikey
        }
        self.console = Console()
        self.styles = {
            "header": Style(color="bright_green", bold=True),
            "key": Style(color="cyan", bold=True),
            "value": Style(color="white"),
            "critical": Style(color="red", bold=True),
            "warning": Style(color="yellow"),
            "info": Style(color="blue"),
            "success": Style(color="green"),
            "ssl": Style(color="magenta"),
            "org": Style(color="bright_blue"),
            "geo": Style(color="bright_yellow"),
            "security": Style(color="bright_red", bold=True)
        }

    async def search(self):
        page = 1
        try:
            async with httpx.AsyncClient(verify=False) as session:
                while page <= self.max_page:
                    jdata = {
                        "qbase64": self.qbase64,
                        "fields": self.fields,
                        "sub_type": self.sub_type,
                        "pagesize": self.max_size,
                        "facets": self.facet,
                        "page": page
                    }
                    response: httpx.Response = await session.request("POST",self._url, headers=self.headers, json=jdata, timeout=60)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("code") == 60000:
                            data = data.get("data", [])
                            self.results.extend(data)
                            page += 1
                        else:
                            if self.verbose:
                                self.logger.warn(f"API responded with bad api response code: {data.get('code')}, stopping.")
                            break
                    else:
                        if self.verbose:
                            self.logger.warn(f"API responded with bad HTTP status code: {response.status_code}, stopping.")
                        break
        except Exception as e:
            if self.verbose:
                self.logger.warn(f"Exception occurred in Zoomeye API search due to: {e}")
            else:
                raise
        return self.results
    
    def _format_timestamp(self, ts: str) -> str:
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M UTC")
        except:
            return ts

    def _create_security_panel(self, result: Dict) -> Optional[Panel]:
        security_data = []
        
        honeypot = result.get("honeypot", 0)
        honeypot_status = Text("YES", style="bold red") if honeypot else Text("NO", style="green")
        security_data.append(("Honeypot", honeypot_status))
        
        idc = result.get("idc", 0)
        idc_status = Text("YES", style="yellow") if idc else Text("NO", style="green")
        security_data.append(("IDC Hosted", idc_status))
        
        if header_hash := result.get("header_hash"):
            security_data.append(("Header Hash", header_hash))
        if body_hash := result.get("body_hash"):
            security_data.append(("Body Hash", body_hash))
        if security_md5 := result.get("security_md5"):
            security_data.append(("Security MD5", security_md5))
        
        if not security_data:
            return None
            
        table = Table.grid(padding=(0, 1))
        table.add_column(style=self.styles["key"], justify="right")
        table.add_column(style=self.styles["value"])
        
        for key, value in security_data:
            table.add_row(key, value)
        
        return Panel(
            table,
            title="Security Information",
            border_style=self.styles["security"],
            box=box.ROUNDED
        )

    def _create_network_overview(self, result: Dict) -> Panel:

        table = Table.grid(padding=(0, 1))
        table.add_column(style=self.styles["key"], justify="right")
        table.add_column(style=self.styles["value"])
        
        table.add_row("IP Address", result.get("ip", "N/A"))
        table.add_row("Port", str(result.get("port", "N/A")))
        table.add_row("Protocol", result.get("protocol", "N/A").upper())
        
        service = result.get("service", "N/A").upper()
        if service in ["HTTP", "TELNET", "FTP", "RDP"]:
            service = Text(service, style="bold yellow")
        table.add_row("Service", service)
        
        if domain := result.get("domain"):
            table.add_row("Domain", domain)
        
        if hostname := result.get("hostname"):
            table.add_row("Hostname", hostname)
        
        if asn := result.get("asn"):
            table.add_row("ASN", f"AS{asn}")
        
        return Panel(
            table,
            title="Network Overview",
            border_style=self.styles["info"],
            box=box.ROUNDED
        )

    def _create_organization_panel(self, result: Dict) -> Optional[Panel]:
        org_data = []
        
        if org_name := result.get("organization.name"):
            org_data.append(("Organization", org_name))
        if isp := result.get("isp.name"):
            org_data.append(("ISP", isp))
        if industry := result.get("primary_industry"):
            sub_industry = result.get("sub_industry", "")
            industry_str = f"{industry}"
            if sub_industry:
                industry_str += f" ({sub_industry})"
            org_data.append(("Industry", industry_str))
        if rank := result.get("rank"):
            org_data.append(("Rank", str(rank)))
        
        if not org_data:
            return None
            
        table = Table.grid(padding=(0, 1))
        table.add_column(style=self.styles["key"], justify="right")
        table.add_column(style=self.styles["value"])
        
        for key, value in org_data:
            table.add_row(key, value)
        
        return Panel(
            table,
            title="Organization Details",
            border_style=self.styles["org"],
            box=box.ROUNDED
        )

    def _create_ssl_panels(self, result: Dict) -> List[Panel]:
        ssl_panels = []
        
        if jarm := result.get("ssl.jarm"):
            panel = Panel(
                jarm,
                title="JARM Fingerprint",
                border_style=self.styles["ssl"],
                box=box.ROUNDED
            )
            ssl_panels.append(panel)
        
        if ja3s := result.get("ssl.ja3s"):
            panel = Panel(
                ja3s,
                title="JA3S Fingerprint",
                border_style=self.styles["ssl"],
                box=box.ROUNDED
            )
            ssl_panels.append(panel)
        
        if ssl_info := result.get("ssl"):
            panel = Panel(
                Syntax(ssl_info, "text", theme="monokai", line_numbers=False, word_wrap=True),
                title="SSL Certificate Details",
                border_style=self.styles["ssl"],
                box=box.ROUNDED
            )
            ssl_panels.append(panel)
        
        return ssl_panels

    def _create_geolocation(self, result: Dict) -> Optional[Panel]:
        geo_data = []
        
        if continent := result.get("continent.name"):
            geo_data.append(("Continent", continent))
        if country := result.get("country.name"):
            geo_data.append(("Country", country))
        if province := result.get("province.name"):
            geo_data.append(("Region", province))
        if city := result.get("city.name"):
            geo_data.append(("City", city))
        if lat := result.get("lat"):
            lon = result.get("lon", "?")
            geo_data.append(("Coordinates", f"{lat}, {lon}"))
        if zipcode := result.get("zipcode"):
            geo_data.append(("Zip Code", zipcode))
        
        if not geo_data:
            return None
            
        table = Table.grid(padding=(0, 1))
        table.add_column(style=self.styles["key"], justify="right")
        table.add_column(style=self.styles["value"])
        
        for key, value in geo_data:
            table.add_row(key, value)
        
        return Panel(
            table,
            title="Geolocation",
            border_style=self.styles["geo"],
            box=box.ROUNDED
        )

    def _create_host_details(self, result: Dict) -> Optional[Panel]:
        host_data = []
        
        if os := result.get("os"):
            host_data.append(("OS", os))
        if device := result.get("device"):
            host_data.append(("Device", device))
        if product := result.get("product"):
            version = result.get("version", "")
            host_data.append(("Software", f"{product} {version}".strip()))
        if server := result.get("header.server.name"):
            server_ver = result.get("header.server.version", "")
            host_data.append(("Server", f"{server} {server_ver}".strip()))
        
        if not host_data:
            return None
            
        table = Table.grid(padding=(0, 1))
        table.add_column(style=self.styles["key"], justify="right")
        table.add_column(style=self.styles["value"])
        
        for key, value in host_data:
            table.add_row(key, value)
        
        return Panel(
            table,
            title="Host Details",
            border_style=self.styles["warning"],
            box=box.ROUNDED
        )

    def _create_content_section(self, result: Dict) -> Optional[Panel]:
        content_panels = []
        
        if titles := result.get("title"):
            title_text = "\n".join(titles) if isinstance(titles, list) else titles
            content_panels.append(
                Panel(
                    Syntax(title_text, "text", theme="monokai", line_numbers=False, word_wrap=True),
                    title="Page Titles",
                    border_style=self.styles["info"]
                )
            )
        
        if headers := result.get("header"):
            content_panels.append(
                Panel(
                    Syntax(headers[:800], "http", theme="monokai", line_numbers=True, word_wrap=True),
                    title="HTTP Headers",
                    border_style=self.styles["warning"]
                )
            )
        
        if banner := result.get("banner"):
            content_panels.append(
                Panel(
                    Syntax(banner, "text", theme="monokai", line_numbers=False, word_wrap=True),
                    title="Service Banner",
                    border_style=self.styles["success"]
                )
            )
        
        if not content_panels:
            return None
            
        return Panel(
            Group(*content_panels),
            title="Content Analysis",
            border_style=self.styles["header"]
        )

    def visualize_results(self, results: List[Dict]):

        for i, result in enumerate(results, 1):

            self.console.print("\n" * 2)
            
            ip = result.get("ip", "N/A")
            port = result.get("port", "N/A")
            service = result.get("service", "N/A").upper()
            last_seen = self._format_timestamp(result.get("update_time", "Unknown"))
            
            header_text = Text.assemble(
                (f"TARGET {i}: ", self.styles["header"]),
                (f"{ip}:{port} ", self.styles["critical"]),
                (f"({service})", self.styles["info"]),
                ("\nLast observed: ", self.styles["key"]),
                (last_seen, self.styles["value"])
            )
            
            if result.get("honeypot"):
                header_text.append("\n⚠️ POTENTIAL HONEYPOT DETECTED ⚠️", style="blink bold red")
            
            self.console.print(Panel(header_text, box=box.HEAVY, border_style=self.styles["header"]))
            
            first_row = []
            first_row.append(self._create_network_overview(result))
            
            if security_panel := self._create_security_panel(result):
                first_row.append(security_panel)
            
            if geo_panel := self._create_geolocation(result):
                first_row.append(geo_panel)
            
            self.console.print(Columns(first_row, equal=False, expand=True))
            
            second_row = []
            if org_panel := self._create_organization_panel(result):
                second_row.append(org_panel)
            
            if host_panel := self._create_host_details(result):
                second_row.append(host_panel)
            
            if ssl_panels := self._create_ssl_panels(result):
                second_row.extend(ssl_panels)
            
            if second_row:
                self.console.print(Columns(second_row, equal=False, expand=True))
            
            if content_panel := self._create_content_section(result):
                self.console.print(content_panel)
            
            if url := result.get("url"):
                self.console.print(
                    Panel(
                        url,
                        title="URL",
                        border_style=self.styles["info"],
                        box=box.SIMPLE
                    )
                )
            
            if i < len(results):
                self.console.rule(style=self.styles["info"])
                

