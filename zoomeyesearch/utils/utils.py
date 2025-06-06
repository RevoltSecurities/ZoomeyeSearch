import aiofiles
import yaml
from fake_useragent import UserAgent
import time
import json
import base64



class Utils:
    def __init__(self):
        pass

    @staticmethod
    def load_creds(filename: str):
        try:
            with open(filename, "r") as streamr:
                contents = streamr.read()
                data = yaml.safe_load(contents)
                return data.get('zoomeye', {}).get('username'), data.get('zoomeye', {}).get('password')
        except Exception as e:
            return None, None

    @staticmethod
    def load_key(filename: str):
        try:
            with open(filename, "r") as streamr:
                contents = streamr.read()
                data = yaml.safe_load(contents)
                return data.get('zoomeye', {}).get('apikey')
        except Exception as e:
            return None

    @staticmethod
    def load_jwt(filename: str):
        try:
            with open(filename, "r") as streamr:
                contents = streamr.read()
                data = yaml.safe_load(contents)
                return data.get('jwt', None)
        except Exception as e:
            return None

    @staticmethod
    def set_auth(filename: str, username: str, password: str, apikey: str):
        new_data = {
            'zoomeye': {
                'username': username,
                'password': password,
                'apikey': apikey
            }
        }
        with open(filename, "w") as file:
            file.write(yaml.dump(new_data, default_flow_style=False))

    @staticmethod
    def set_jwt(filename: str, jwt: str):
        new_data = {"jwt": jwt}
        with open(filename, "w") as file:
            file.write(yaml.dump(new_data, indent=4))

        
    @staticmethod
    def random_useragent()-> str:
        return UserAgent().random
    
    @staticmethod
    async def async_reader(filename: str):
        try:
            async with aiofiles.open(filename, "r") as file:
                content = await file.readlines()
                return [line.strip() for line in content if line.strip()]
        except Exception:
            return None
            
    @staticmethod
    def is_valid(jwt: str) -> bool:
        try:
            parts = jwt.split('.')
            if len(parts) != 3:
                return False  
            payload_b64 = parts[1]
            padding = '=' * (-len(payload_b64) % 4)
            payload_b64 += padding
            payload_json = base64.urlsafe_b64decode(payload_b64).decode('utf-8')
            payload = json.loads(payload_json)
            exp = payload.get("exp")
            if not exp:
                return False 
            current_time = int(time.time())
            return current_time < exp 
        except Exception:
            return False