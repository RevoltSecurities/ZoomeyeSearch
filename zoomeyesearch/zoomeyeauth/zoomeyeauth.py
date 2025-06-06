import httpx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
import datetime
from zoomeyesearch.logger.logger import Logger
import getpass
from rich.prompt import Confirm
from typing import Optional

class ZoomeyeAuth:
    def __init__(self,apikey: str = None,verbose:bool = True) ->None:
        self.apikey = apikey
        self.logger = Logger()
        self.console = Console()
        self._url = "https://api.zoomeye.ai/"
        self._headers = {
            "API-KEY": self.apikey
        }
        self.verbose = verbose

        
    async def _request(self,method:str = None, url:str = None, body:str = None, params = None, jdata=None, timeout=60) -> httpx.Response | None:
        try:
            async with httpx.AsyncClient(verify=False) as session:
                response: httpx.Response = await session.request(
                    method=method.upper(),
                    url=url,
                    content=body,
                    json=jdata,
                    headers=self._headers,
                    timeout=timeout,
                    params=params
                )
                return response
        except Exception as e:
            if self.verbose:
                self.logger.warn(f"Exception occured in the auth request method due to: {e}")
            return None
        
    async def userinfo(self) -> dict | None:
        try:
            if self.apikey is None:
                if self.verbose:
                    self.logger.warn("please pass the Zoomeye API key to get user information")
                    return None
                else:
                    raise ValueError("please pass the Zoomeye API key")
            response = await self._request("POST", f"{self._url}v2/userinfo")
            if not response or response.status_code != 200:
                if self.verbose:
                    self.console.print("[bold red]❌ Failed to retrieve user info from ZoomEye API.[/bold red]")
                return
            data = response.json()
            if self.verbose:
                self.display_userinfo(data)
            return response
        except Exception as e:
            return None
        
    def display_userinfo(self, json_data):
        if json_data.get("code") != 60000:
            self.console.print(f"[bold red]API Error:[/bold red] {json_data.get('message', 'Unknown error')}")
            return

        data = json_data.get("data", {})
        sub = data.get("subscription", {})

        user_table = Table(title="[bold cyan]👤 ZoomEye User Profile[/bold cyan]", box=box.DOUBLE_EDGE, padding=(0, 1))
        user_table.add_column("Field", style="bold green")
        user_table.add_column("Value", style="bold white")

        user_table.add_row("Username", str(data.get("username", "N/A")))
        user_table.add_row("Email", str(data.get("email", "N/A")))
        user_table.add_row("Phone", str(data.get("phone", "N/A")))
        
        created = data.get("created_at", "N/A")
        if created != "N/A":
            try:
                created = datetime.datetime.fromisoformat(created.replace("Z", "")).strftime("%Y-%m-%d %H:%M")
            except ValueError:
                pass
        user_table.add_row("Created", created)

        sub_table = Table(title="[bold magenta]🚀 Subscription Details[/bold magenta]", box=box.MINIMAL_DOUBLE_HEAD, padding=(0, 1))
        sub_table.add_column("Type", style="bold yellow")
        sub_table.add_column("Status", style="bold white")

        sub_table.add_row("Plan", str(sub.get("plan", "N/A")))
        sub_table.add_row("End Date", str(sub.get("end_date", "N/A")))
        sub_table.add_row("Points", str(sub.get("points", "0")))
        sub_table.add_row("ZoomEye Points", str(sub.get("zoomeye_points", "0")))

        self.console.rule("[bold green]ZoomEye Account Information[/bold green]")
        self.console.print(user_table)
        self.console.print(Panel.fit(sub_table, border_style="magenta", title="[bold cyan]Access Stats[/bold cyan]"))
        self.console.rule("[bold green]End[/bold green]")

    @staticmethod
    async def shell() -> Optional[dict]:
        console = Console()

        welcome_text = Text("Welcome to ZoomEye Auth Configuration\n\nPlease provide your ZoomEye credentials to proceed.", style="bold green")
        welcome_panel = Panel.fit(
            welcome_text,
            title="[bold blue]ZoomEye Authentication Setup[/]",
            border_style="bright_blue",
            padding=(1, 4),
            style="bold white"
        )
        console.print(welcome_panel)

        try:
            email = input("ZoomEye Email    : ").strip()
            password = getpass.getpass("ZoomEye Password : ").strip()
            api_key = getpass.getpass("ZoomEye API Key  : ").strip()

            if not all([email, password, api_key]):
                console.print("[bold red]❌ All fields are required. Aborting setup.[/bold red]")
                return None

            masked_password = "*" * len(password)
            masked_apikey = "*" * len(api_key)

            confirmation = Text()
            confirmation.append(f"Email    : ", style="bold white")
            confirmation.append(f"{email}\n", style="cyan")
            confirmation.append(f"Password : ", style="bold white")
            confirmation.append(f"{masked_password}\n", style="magenta")
            confirmation.append(f"API Key  : ", style="bold white")
            confirmation.append(f"{masked_apikey}\n\n", style="yellow")
            confirmation.append("Please confirm that the above details are correct.", style="bold green")

            console.print(Panel.fit(
                confirmation,
                title="[bold green]🔍 Confirmation[/]",
                border_style="green",
                padding=(1, 4)
            ))

            if not Confirm.ask("[bold yellow]Are these details correct?[/bold yellow]"):
                console.print("[bold red]❌ Configuration cancelled by user.[/bold red]")
                return None

            return {
                "email": email,
                "password": password,
                "apikey": api_key
            }

        except KeyboardInterrupt:
            console.print("\n[bold red]⚠️  Input interrupted by user.[/bold red]")
            return None
        except Exception as e:
            console.print(f"[bold red]💥 Unexpected error: {e}[/bold red]")
            return None
        
    
        
    
        
    
        
    