from config.settings import ConfigManager, ConfigEnv, load_config
from src.load import load_database
from src.extract import download_bills


config = ConfigManager(load_config())
env = ConfigEnv()

if __name__ == '__main__':
    
    print('baixando faturas')
    download_bills(config, host=env.host, user=env.app_user, pwd=env.pwd)
    
    # print('carregando para o banco de dados')
    load_database(config.file_path)
    
    