from src.load import load_database
from src.extract import download_bills


if __name__ == '__main__':
    
    print('baixando faturas')
    download_bills()
    
    print('carregando para o banco de dados')
    load_database()
    
    