import json
from pathlib import Path
from dotenv import load_dotenv
from src.utils import require_env

# load enviroments
import os

def load_env():
    load_dotenv()
    return {
        "host" : require_env(os.getenv('HOST')),
        "user" : require_env(os.getenv('USER')),
        "pwd"  :require_env(os.getenv('APP_PWD'))
    }

# load json parameters
config_path = Path('config/config.json')

root_path = Path(__file__).parent.parent
default_file_path = Path(root_path, 'arc')

def load_config():
    with open(config_path, 'r', encoding='utf-8') as j:
        return json.load(j)


class ConfigManager:
    def __init__(self, config: dict | list):
        
        self.email_subject = self.require(config, "email.email_subject")
        self.email_from = self.require( config, "email.email_from")
        self.email_folder = self.require(config, "email.email_folder")
        self.file_type = self.require(config, "file.types")
        self.file_path = config.get("paths", {}).get("download") or default_file_path
    
    def require(self, config: dict|list, param: str):
        value = config
        keys = param.split('.')
               
        for key in keys:
            if key not in value:
                raise ValueError(f"Mandatory configuration missing: {param}")
            value = value[key]
        return value

if __name__ == '__main__':
    config = load_config()
    
    load_param = ConfigManager(config)
    print(
        load_param.email_folder, 
        load_param.email_from, 
        load_param.email_subject, 
        load_param.file_path, 
        load_param.file_type,
        sep="\n"
        )


