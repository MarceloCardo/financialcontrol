import yaml
from pathlib import Path

config_path = Path('config/config.yaml')

root_path = Path(__file__).parent.parent
default_file_path = Path(root_path, 'arc')

with open(config_path, 'r') as f:
    try:
        config=yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise exc


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
        print(keys)
        print(value)
        
        for key in keys:
            if key not in value:
                raise ValueError(f"Mandatory configuration missing: {param}")
            value = value[key]
   
            
load = ConfigManager(config)

# print(load.file_type, load.file_path, load.email_subject)