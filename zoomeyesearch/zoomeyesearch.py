import asyncio
from zoomeyesearch.search.search import ZoomeyeSearch
from zoomeyesearch.zoomeyeauth.zoomeyeauth import ZoomeyeAuth
from zoomeyesearch.zoomeyelogin.zoomeyelogin import ZoomeyeLogin
from zoomeyesearch.subdomain.subdomain import ZoomeyeSubenum
from zoomeyesearch.zoomeyegpt.zoomeyegpt import ZoomeyeGPT
from zoomeyesearch.zoomeyestats.zoomeyestats import ZoomeyeStats
from zoomeyesearch.config.config import Config
from zoomeyesearch.logger.logger import Logger
from zoomeyesearch.utils.utils import Utils
from zoomeyesearch.banner.banner import Banner
from zoomeyesearch.version.version import Version
from zoomeyesearch.gitutils.gitutils import GitUtils
from zoomeyesearch.help.help import Helper
from zoomeyesearch.save.save import Save
import tempfile
import click
import sys

class Zoomeye():
    def __init__(self) -> None:
        self._utils = Utils()
        self._configloader = Config()
        self._provider_config = self._configloader.config_auth()
        self._jwt_config = self._configloader.config_jwt()
        self._logger = Logger()
        self._username, self._password = self._utils.load_creds(self._provider_config)
        self._apikey = self._utils.load_key(self._provider_config)
        self._jwt = self._utils.load_jwt(self._jwt_config)
        self.banner = Banner(tool_name="ZoomeyeSearch")
        self._saver = Save(self._logger)
        self._version = Version()
        self.tmpdir = tempfile.gettempdir()
        self.git = GitUtils("RevoltSecurities/ZoomeyeSearch", "zoomeyesearch", self.tmpdir)
        self.git_version = self._version.version
        self.pypi_version = self._version.pypi
        self.banner.render()
        self.Version()
        
    def _run_async(self, coro):
        try:
            loop = asyncio.get_running_loop()
            future = asyncio.create_task(coro)
            loop.run_until_complete(future)  
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(coro)
            loop.close()
        
    def Version(self):
        async def versions():
            currentgit = await self.git.git_version()
            if not currentgit:
                self._logger.warn("unable to get the latest version of zoomeyesearch")
                return
            
            if currentgit == self.git_version:
                print(f"[{self._logger.blue}{self._logger.bold}version{self._logger.reset}]:{self._logger.bold}{self._logger.white}zoomeyesearch current version {self.git_version} ({self._logger.green}latest{self._logger.reset}{self._logger.bold}{self._logger.white}){self._logger.reset}", file=sys.stderr)
            else:
                print(f"[{self._logger.blue}{self._logger.bold}version{self._logger.reset}]:{self._logger.bold}{self._logger.white}zoomeyesearch current version {self.git_version} ({self._logger.red}outdated{self._logger.reset}{self._logger.bold}{self._logger.white}){self._logger.reset}", file=sys.stderr)
            return
        self._run_async(versions())

    async def auth(self) -> None:
        data = await ZoomeyeAuth().shell()
        self._utils.set_auth(self._provider_config,data["email"], data["password"], data["apikey"])

    async def login(self) -> str|None:
        data = ZoomeyeLogin(self._username, self._password)
        jwt = await data.login()
        self._jwt = jwt
        if self._jwt is None:
            self._logger.error("Failed to authenticate, Credentials might be incorrect or Try again.")
            return None
        self._utils.set_jwt(self._jwt_config, jwt)
        self._jwt = jwt
        return jwt

    async def search(
        self,
        query:str, 
        fields:str="ip,port,domain,update_time,ssl,product,country,ssl.jarm,ssl.ja3s,hostname,os,service,title,protocol,header,version,device,header.server.name,banner,rdns,continent.name,country.name,organization.name,lon,lat,asn,city,province.name,isp.name,zipcode,honeypot,url", 
        facet:str="country,subdivisions,city,product,service,device,os,ssl", 
        max_page:int=5, 
        max_size:int=2000,
        output=None) -> None:
        
        searcher = ZoomeyeSearch(
            self._apikey,
            query=query, 
            fields=fields,  
            facet=facet, 
            max_page=max_page,
            max_size=max_size,
            verbose=False,
            sub_type="v4,v6,web"
        ) 
        data = await searcher.search()   
        if not data:
            self._logger.error("No results found for the given query.")
            return
        if output:
            await self._saver.save(output,data,True)
        searcher.visualize_results(data)

    async def subdomain(self, domain:str, type=1, output=None) -> None:
        enumerator = ZoomeyeSubenum(self._apikey, domain, type=type)
        data = await enumerator.enumerate()
        for sub in data:
            print(sub)
            if output:
                await self._saver.save(output, sub)
        print(f"Total found: {len(data)}")

    async def GPT(self) -> None:
        isvalid = self._utils.is_valid(self._jwt)
        if not isvalid:
            self._logger.warn("JWT Token is expired, Authenticating again...")
            jwt = await self.login()
            if not jwt:
                self._logger.error("Failed to authenticate, exiting...")
                return
            self._utils.set_jwt(self._jwt_config,self._jwt)
        gpt = ZoomeyeGPT(self._jwt, self._apikey)
        await gpt.chat()
        
    async def stats(self, query:str, field: str, limit: int = 1000, output=None) -> None:
        try:
            isvalid = self._utils.is_valid(self._jwt)
            if not isvalid:
                self._logger.warn("JWT Token is expired, Authenticating again...")
                jwt = await self.login()
                self._jwt = jwt
                if not self._jwt:
                    self._logger.error("Failed to authenticate, exiting...")
                    return
                self._utils.set_jwt(self._jwt_config,self._jwt)
            stats = ZoomeyeStats(self._jwt,field,query,False,limit)
            data = await stats.search()
            if not data:
                self._logger.error("No statistical results found for the given query.")
                return
            if output:
                await self._saver.save(output, data, True)
            stats.display(data)
        except Exception as e:
            self._logger.error(f"An error occurred in the stats mode due to: {e}")
            return None
        
    async def update(self,update,show_updates) -> None:
        if show_updates:
            await self.git.show_update_log()
            return
        
        if update:
            current = await self.git.git_version()
            if not current:
                self._logger.warn("unable to get the latest version of Zoomeyesearch")
                return
                
            if current == self.git_version:
                self._logger.info("Zoomeyesearch is already in latest version")
                return
                
            zipurl = await self.git.fetch_latest_zip_url()
            if not zipurl:
                self._logger.warn("unable to get the latest source code of Zoomeyesearch")
                return
                
            await self.git.download_and_install(zipurl)
            newpypi = self.git.current_version()
            if newpypi == self.pypi_version:
                self._logger.warn("unable to update Zoomeyesearch to the latest version, please try manually")
                return
                
            self._logger.info(f"Zoomeyesearch has been updated to version")
            await self.git.show_update_log()
            return
        

settings = dict(help_option_names=['-h', '--help'])
zoomeyesearcher = Zoomeye()

def customizer(ctx, param, value): 
    
    if value and not ctx.resilient_parsing:
        if not ctx.invoked_subcommand:
            Helper().main_help()
            exit()
        else:
            ctx.invoke(ctx.command, ['--help'])

@click.group(context_settings=settings)
@click.option("-h", "--help", is_flag=True, is_eager=True, expose_value=False, callback=customizer)
@click.option('-fields','--fields', default="ip,port,domain,update_time,ssl,product,country,ssl.jarm,ssl.ja3s,hostname,os,service,title,protocol,header,version,device,header.server.name,banner,rdns,continent.name,country.name,organization.name,lon,lat,asn,city,province.name,isp.name,zipcode,honeypot,url")
@click.option('-facet','--facet', default="country,subdivisions,city,product,service,device,os,ssl")
@click.option('-mp','--max-page', default=5, type=int, help='Maximum number of pages to fetch')
@click.option('-limit','--limit', default=2000, type=int, help='Maximum number of results to fetch')
@click.option('-o', '--output', type=str)
@click.pass_context
def cli(ctx, fields,facet, max_page, limit, output) -> None:
    ctx.ensure_object(dict)
    ctx.obj['fields'] = fields
    ctx.obj['facet'] = facet
    ctx.obj['max_page'] = max_page
    ctx.obj['limit'] = limit
    ctx.obj['output'] = output
    

@cli.command()
@click.option('-asn','--asn', type=str)
@click.option('-h', '--help', is_flag=True)
@click.pass_context
def asn(ctx,asn,help) -> None:
    if help:
        Helper().help_asn()
        return
    asyncio.run(zoomeyesearcher.search(
        query=f"asn={asn}",
        fields=ctx.obj['fields'],
        max_page=ctx.obj['max_page'],
        max_size=ctx.obj['limit'],
        facet=ctx.obj['facet'],
        output=ctx.obj.get('output', None)
        
    ))
    

@cli.command()
@click.option('-ip','--ip' ,type=str)
@click.option('-h', '--help', is_flag=True)
@click.pass_context
def ip(ctx, ip,help) -> None:
    if help:
        Helper().help_ip()
        return
    asyncio.run(zoomeyesearcher.search(
        query=f"ip={ip}",
        fields=ctx.obj['fields'],
        max_page=ctx.obj['max_page'],
        max_size=ctx.obj['limit'],
        facet=ctx.obj['facet'],
        output=ctx.obj.get('output', None)
    ))
    
@cli.command()
@click.option('-d','--domain', type=str)
@click.option('-h', '--help', is_flag=True)
@click.pass_context
def domain(ctx, domain,help) -> None:
    if help:
        Helper().help_domain()
        return
    asyncio.run(zoomeyesearcher.search(
        query=f"domain={domain}",
        fields=ctx.obj['fields'],
        max_page=ctx.obj['max_page'],
        max_size=ctx.obj['limit'],
        facet=ctx.obj['facet'],
        output=ctx.obj.get('output', None)
    ))
    
@cli.command()
@click.option('-org','--org', type=str)
@click.option('-h', '--help', is_flag=True)
@click.pass_context
def org(ctx,org,help) -> None:
    if help:
        Helper().help_org()
        return
    asyncio.run(zoomeyesearcher.search(
        query=f"org={org}",
        fields=ctx.obj['fields'],
        max_page=ctx.obj['max_page'],
        max_size=ctx.obj['limit'],
        facet=ctx.obj['facet'],
        output=ctx.obj.get('output', None)
    ))

@cli.command()
@click.option('-cidr','--cidr', type=str)
@click.option('-h', '--help', is_flag=True)
@click.pass_context
def cidr(ctx, cidr,help) -> None:
    if help:
        Helper().help_cidr()
        return
    asyncio.run(zoomeyesearcher.search(
        query=f"cidr={cidr}",
        fields=ctx.obj['fields'],
        max_page=ctx.obj['max_page'],
        max_size=ctx.obj['limit'],
        facet=ctx.obj['facet'],
        output=ctx.obj.get('output', None)
    ))
    
@cli.command()
@click.option('-sV','--service', type=str)
@click.option('-h', '--help', is_flag=True)
@click.pass_context
def service(ctx, service,help) -> None:
    if help:
        Helper().help_service()
        return
    asyncio.run(zoomeyesearcher.search(
        query=f"service={service}",
        fields=ctx.obj['fields'],
        max_page=ctx.obj['max_page'],
        max_size=ctx.obj['limit'],
        facet=ctx.obj['facet'],
        output=ctx.obj.get('output', None)
    ))
    
@cli.command()
@click.option('-pd','--product', type=str)
@click.option('-h', '--help', is_flag=True)
@click.pass_context
def product(ctx, product,help) -> None:
    if help:
        Helper().help_product()
        return
    asyncio.run(zoomeyesearcher.search(
        query=f"product={product}",
        fields=ctx.obj['fields'],
        max_page=ctx.obj['max_page'],
        max_size=ctx.obj['limit'],
        facet=ctx.obj['facet'],
        output=ctx.obj.get('output', None)
    ))
    
    
@cli.command()
@click.option('-d','--domain', type=str)
@click.option('-as', '--associated-domain', is_flag=True)
@click.option('-sub', '--subdomain', is_flag=True)
@click.option('-h', '--help', is_flag=True)
@click.pass_context
def enumerate(ctx,domain, associated_domain,subdomain,help) -> None:
    if help:
        Helper().help_enumerate()
        return
    types = 1
    if associated_domain:
        types = 0
    if subdomain:
        types = 1
    
    asyncio.run(zoomeyesearcher.subdomain(
        domain=domain,
        type=types,
        output=ctx.obj.get('output', None)
    ))
    
@cli.command()
@click.option('-country', '--country', type=str)
@click.option('-city', '--city', type=str)
@click.option('-subdivision', '--subdivision', type=str)
@click.option('-h', '--help', is_flag=True)
@click.pass_context
def geosearch(ctx, country, city, subdivision,help) -> None:
    if help:
        Helper().help_geosearch()
        return
    query = None
    if country:
        query = f"country={country}"
    if city:
        query = f"city={city}"
    if subdivision:
        query = f"subdivision={subdivision}"
    if query is None:
       zoomeyesearcher._logger.error("No search parameters provided. Use --country, --city, or --subdivision to specify search criteria.")
       return
   
    asyncio.run(zoomeyesearcher.search(
        query=query,
        fields=ctx.obj['fields'],
        max_page=ctx.obj['max_page'],
        max_size=ctx.obj['limit'],
        facet=ctx.obj['facet'],
        output=ctx.obj.get('output', None)
    ))
    
@cli.command()
@click.option('-hash','--faviconhash', type=str)
@click.option('-h', '--help', is_flag=True)
@click.pass_context
def faviconhash(ctx, faviconhash,help) -> None:
    if help:
        Helper().help_faviconhash()
        return
    asyncio.run(zoomeyesearcher.search(
        query=f"iconhash={faviconhash}",
        fields=ctx.obj['fields'],
        max_page=ctx.obj['max_page'],
        max_size=ctx.obj['limit'],
        facet=ctx.obj['facet'],
        output=ctx.obj.get('output', None)
    ))
    
@cli.command()
@click.option('--ssl', type=str)
@click.option('--fingerprint', type=str)
@click.option('--chain-count', type=str)
@click.option('--alg', type=str)
@click.option('--issuer-cn', type=str)
@click.option('--rsa-bits', type=str)
@click.option('--ecdsa-bits', type=str)
@click.option('--pubkey-type', type=str)
@click.option('--serial', type=str)
@click.option('--cipher-bits', type=str)
@click.option('--cipher-name', type=str)
@click.option('--cipher-version', type=str)
@click.option('--ssl-version', type=str)
@click.option('--subject-cn', type=str)
@click.option('--jarm', type=str)
@click.option('--ja3s', type=str)
@click.option('-h', '--help', is_flag=True)
@click.pass_context
def ssl(ctx, ssl, fingerprint, chain_count, alg, issuer_cn, rsa_bits, ecdsa_bits, pubkey_type, serial,
        cipher_bits, cipher_name, cipher_version, ssl_version, subject_cn, jarm, ja3s,help):
    
    if help:
        Helper().help_ssl()
        return
    
    query = None

    if ssl:
        query = f'ssl="{ssl}"'
    if fingerprint:
        query = f'ssl.cert.fingerprint="{fingerprint}"'
    if chain_count is not None:
        
        query = f'ssl.chain_count={chain_count}'
    if alg:
        query = f'ssl.cert.alg="{alg}"'
    if issuer_cn:
        query = f'ssl.cert.issuer.cn="{issuer_cn}"'
    if rsa_bits:
        query = f'ssl.cert.pubkey.rsa.bits={rsa_bits}'
    if ecdsa_bits:
        query = f'ssl.cert.pubkey.ecdsa.bits={ecdsa_bits}'
    if pubkey_type:
        query = f'ssl.cert.pubkey.type="{pubkey_type}"'
    if serial:
        query = f'ssl.cert.serial="{serial}"'
    if cipher_bits:
        query = f'ssl.cipher.bits="{cipher_bits}"'
    if cipher_name:
        query = f'ssl.cipher.name="{cipher_name}"'
    if cipher_version:
        query = f'ssl.cipher.version="{cipher_version}"'
    if ssl_version:
        query = f'ssl.version="{ssl_version}"'
    if subject_cn:
        query = f'ssl.cert.subject.cn="{subject_cn}"'
    if jarm:
        query = f'ssl.jarm="{jarm}"'
    if ja3s:
        query = f'ssl.ja3s={ja3s}'
    
    if query is None:
        zoomeyesearcher._logger.warn("No search parameters provided. Use --ssl, --fingerprint, --chain-count, --alg, --issuer-cn, --rsa-bits, --ecdsa-bits, --pubkey-type, --serial, --cipher-bits, --cipher-name, --cipher-version, --ssl-version, --subject-cn, --jarm or --ja3s to specify search criteria.")
        return

    asyncio.run(zoomeyesearcher.search(
        query=query,
        fields=ctx.obj['fields'],
        max_page=ctx.obj['max_page'],
        max_size=ctx.obj['limit'],
        facet=ctx.obj['facet'],
        output=ctx.obj.get('output', None)
    ))

@cli.command()
@click.option('--query', type=str)
@click.option('--field', type=str)
@click.option('-h', '--help', is_flag=True)
@click.pass_context
def stats(ctx, query, field,help) -> None:
    if help:
        Helper().help_stats()
        return
    if not query or not field:
        zoomeyesearcher._logger.error("Both --query and --field options are required for stats mode.")
        return

    try:
        asyncio.run(zoomeyesearcher.stats(
            query=query,
            field=field,
            limit=ctx.obj['limit'],
        output=ctx.obj.get('output', None)
        ))
    except Exception as e:
        zoomeyesearcher._logger.error(f"An error occurred while fetching stats data of Zoomeye: {e}")
    
@cli.command()
@click.option('-sc','--search', type=str)
@click.option('-h', '--help', is_flag=True)
@click.pass_context
def search(ctx, search,help) -> None:
    if help:
        Helper().help_search()
        return
    asyncio.run(zoomeyesearcher.search(
        query=search,
        fields=ctx.obj['fields'],
        max_page=ctx.obj['max_page'],
        max_size=ctx.obj['limit'],
        facet=ctx.obj['facet'],
        output=ctx.obj.get('output', None)
    ))

@cli.command()
@click.option('-h', '--help', is_flag=True)
def gpt(help) -> None:
    if help:
        Helper().help_gpt()
        return
    asyncio.run(zoomeyesearcher.GPT())
    

@cli.command()
@click.option('-h', '--help', is_flag=True)
def auth(help) -> None:
    if help:
        Helper().help_auth()
        return
    asyncio.run(zoomeyesearcher.auth())
    

@cli.command()
@click.option('-h', '--help', is_flag=True)
def login(help) -> None:
    if help:
        Helper().help_login()
        return
    asyncio.run(zoomeyesearcher.login())
    
@cli.command()
@click.option('-u', '--update', is_flag=True)
@click.option('-sup', '--show-updates', is_flag=True)
@click.option('-h', '--help', is_flag=True)
def update(update, show_updates, help) -> None:
    if help:
        Helper().help_update()
        return
    asyncio.run(zoomeyesearcher.update(update, show_updates))
    
def main():
    try:
        cli(obj={})
    except Exception as e:
        zoomeyesearcher._logger.error(f"An error occurred in the main module: {e}")
        exit(1)
        
if __name__ == "__main__":
    main()