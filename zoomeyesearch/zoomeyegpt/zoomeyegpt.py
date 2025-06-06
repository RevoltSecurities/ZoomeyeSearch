import asyncio
import httpx
import time
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.prompt import Prompt
from rich.box import ROUNDED
from rich.text import Text
from rich.align import Align
from zoomeyesearch.utils.utils import Utils
from zoomeyesearch.search.search import ZoomeyeSearch

class ZoomeyeGPT:
    def __init__(self, jwt: str, apikey:str,verbose: bool = True):
        self.jwt = jwt
        self.apikey = apikey
        self.verbose = verbose
        self._url = "https://www.zoomeye.ai/api/search/gpt"
        self._headers = {"cube-authorization": self.jwt}
        self.console = Console()
        self.session = httpx.AsyncClient(verify=False)
        self._utils = Utils()

    def show_welcome_panel(self):
        panel_text = Text(justify="center")
        panel_text.append("\n🌐  Welcome to ", style="bold bright_magenta")
        panel_text.append("ZoomeyeGPT CLI\n", style="bold bright_cyan")
        panel_text.append("\nYour smart assistant to generate Zoomeye search queries using GPT\n", style="cyan")
        panel_text.append("\nType your natural language query, and let GPT generate a powerful dork for you!\n", style="bright_white")
        panel_text.append("\nPress Ctrl+C or type 'quit' to exit.\n", style="yellow")
        panel = Panel(
            Align.center(panel_text, vertical="middle"),
            title="[bold bright_magenta]Zoomeye x GPT Assistant[/bold bright_magenta]",
            border_style="bright_cyan",
            box=ROUNDED,
            padding=(1, 4),
        )
        self.console.clear()
        self.console.print(panel)

    def _error_panel(self, message: str):
        self.console.print(Panel.fit(f"[red]{message}[/red]", title="❌ Error", border_style="red"))

    def _create_spinner_panel(self, message: str) -> Progress:
        return Progress(
            SpinnerColumn(style="bright_cyan"),
            TextColumn(f"[cyan]{message}"),
            transient=True,
            console=self.console
        )

    async def request(self, query: str) -> Optional[str]:
        try:
            payload = {"query": query}
            self._headers["User-Agent"] = self._utils.random_useragent()
            with self._create_spinner_panel("Thinking... Generating query using GPT") as progress:
                task = progress.add_task("thinking", total=None)
                response = await self.session.post(
                    self._url,
                    headers=self._headers,
                    json=payload,
                    timeout=60
                )
                progress.update(task, completed=1)

            if response.status_code != 200:
                self._error_panel(f"HTTP error: {response.status_code}")
                return None

            data = response.json()
            if data.get("status") != 200:
                self._error_panel("API returned a failure status.")
                return None

            return data.get("result", {}).get("grammar")

        except Exception as e:
            self._error_panel(str(e))
            if self.verbose:
                import traceback
                self.console.print(traceback.format_exc())
            return None

    async def chat(self):
        self.show_welcome_panel()

        while True:
            try:
                query = Prompt.ask("[bold bright_green]> Enter your query[/bold bright_green]")

                if query.lower() in ("quit", "exit", "q"):
                    self.console.print("[bold yellow]👋 Exiting ZoomeyeGPT. Goodbye![/bold yellow]")
                    break

                if not query.strip():
                    continue

                with Live(Align.center("[cyan]🔄 Processing your query...[/cyan]", vertical="middle"), refresh_per_second=6, transient=True):
                    result = await self.request(query)

                if not result:
                    continue

                self.console.print("\n[bold bright_white]💡 Generated Zoomeye Dork:[/bold bright_white]\n")
                self.console.print(Panel(result, border_style="bright_green"))

                confirm = Prompt.ask("\n[bold magenta]→ Proceed with this query?[/bold magenta]", choices=["y", "n"], default="y")
                if confirm.lower() == "y":
                    self.console.print(Panel.fit("[green]✅ Proceeding...[/green]", border_style="green"))
                    searcher = ZoomeyeSearch(self.apikey, result,"ip,port,domain,update_time,ssl,product,country,ssl.jarm,ssl.ja3s,hostname,os,service,title,protocol,header,version,device,header.server.name,banner,rdns,continent.name,country.name,organization.name,lon,lat,asn,city,province.name,isp.name,zipcode,honeypot,url",
                                             "country,subdivisions,city,product,service,device,os,ssl")
                    data = await searcher.search()
                    searcher.visualize_results(data)
                    return result
                else:
                    self.console.print(Panel.fit("[yellow]❌ Cancelled[/yellow]", border_style="yellow"))

            except KeyboardInterrupt:
                self.console.print("\n[bold yellow]Interrupted. Use 'quit' to exit.[/bold yellow]")
            except Exception as e:
                self._error_panel(str(e))
                if self.verbose:
                    import traceback
                    self.console.print(traceback.format_exc())
