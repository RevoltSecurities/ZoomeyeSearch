from pathlib import Path
from appdirs import user_config_dir

class Config:
    def __init__(self, app_name: str = "Zoomeye"):
        self.app_name = app_name
        if not self.app_name:
            raise ValueError("App name is required")
        self._ensure_config_dir_exists()
        self._ensure_config_files_exist()
        
    @property
    def config_dir(self) -> Path:
        return Path(user_config_dir(self.app_name))
    
    def config_auth(self) -> Path:
        return self.config_dir / "provider-config.yaml"
    
    def config_jwt(self) -> Path:
        return self.config_dir / "jwt.yaml"
    
    def _ensure_config_dir_exists(self) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
    def _ensure_config_files_exist(self) -> None:
        files = {
        self.config_auth(): "zoomeye:\n    username:wiener\n    password:peter\n    apikey:DIOBSFOUBGFOUBSOFBOFBF\n",
        self.config_jwt(): "jwt:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZha2V1c2VyIiwiZW1haWwiOiJmYWtlQGdtYWlsLmNvbSIsImV4cCI6MTc0NzgyNzYzMy4wfQ.Xkn8jeSWb_mf907QtmbpA6wWKEU3uNYknd9qMhsmkic\n"
       }
        for path, default_content in files.items():
            if not path.exists():
                path.write_text(default_content)