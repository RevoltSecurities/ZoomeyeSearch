from playwright.async_api import async_playwright
from zoomeyesearch.logger.logger import Logger


class ZoomeyeLogin:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.login_url = f"https://www.zoomeye.ai/cas/en-US/ui/loginin?service=https%3A%2F%2Fwww.zoomeye.ai%2Flogin"
        self.logger = Logger()
        self.context = None
        self.page = None
        self.cookies = []
        self.local_storage = {}

    async def _init_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False, slow_mo=100)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def login(self):
        try:
            await self._init_browser()
            await self.page.goto(self.login_url)

            await self.page.wait_for_selector('input.rc-input[type="text"]')
            await self.page.fill('input.rc-input[type="text"]', self.email)

            await self.page.wait_for_selector('input.rc-input[type="password"]')
            await self.page.fill('input.rc-input[type="password"]', self.password)

            await self.page.wait_for_selector('button.formBtn')
            await self.page.click('button.formBtn')
            await self.page.wait_for_timeout(10000)

            self.cookies = await self.context.cookies()
        
            self.local_storage = await self.page.evaluate("""() => {
            const data = {};
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                data[key] = localStorage.getItem(key);
            }
            return data;
            }""") #just to get the local storage data and save it securely

            await self.browser.close()
            await self.playwright.stop()

            jwt_token = next((cookie['value'] for cookie in self.cookies if cookie['name'] == 'token'), None)
            return jwt_token
        except Exception as e:
            self.logger.warn(f"Error occured in the zoomeye login module due to: {e}")
            
