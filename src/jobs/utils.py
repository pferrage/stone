import re
import pandas as pd
import os
from sqlalchemy import create_engine, MetaData


def getEngine(db: str):
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    host = os.getenv('MYSQL_HOST')
    port = os.getenv('MYSQL_PORT')

    connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'
    return create_engine(connection_string)

def loadDataFrameToSQL(df: pd.DataFrame, tabName: str, db: str) -> tuple[None]:
    engine = getEngine(db)
    df.to_sql(tabName, engine, if_exists='append', index=False)

def loadSQLToDataFrame(query: str, db: str) -> tuple[pd.DataFrame]:
    engine = getEngine(db)
    return pd.read_sql_query(query, engine)

    
def checkNumber(text: str) -> tuple[bool]:
    default = re.compile(r'\d')
    result = default.search(text)
    return bool(result)

def adjustText(text: str) -> tuple[str]:
    map = {
        'á': 'a', 'Á': 'A', 'â': 'a', 'Â': 'A', 'à': 'a', 'À': 'A', 'ã': 'a', 'Ã': 'A',
        'é': 'e', 'É': 'E', 'ê': 'e', 'Ê': 'E','è': 'e', 'È': 'E',
        'í': 'i', 'Í': 'I', 
        'ó': 'o', 'Ó': 'O', 'ô': 'o', 'Ô': 'O','õ': 'o', 'Õ': 'O',
        'ú': 'u', 'Ú': 'U',
        'ç': 'c', 'Ç': 'C'
    }
    rgx_specials = r'[.0123456789!@#$%¨&*()\-_´`^~\[\]{}<>:?,.;/\\|"\'\+]+'
    
    for with_accent, without_accent in map.items():
        text = text.replace(with_accent, without_accent)
    
    text = re.sub(rgx_specials, '', text)
    
    return text

def setTableName(text: str) -> tuple[str]:
    tabName = text.lower()
    tabName = tabName.replace('.csv','')
    tabName = 'tb_' + adjustText(tabName)
    
    return tabName


def getCSV(dir: str,csvFile: str) -> tuple[pd.DataFrame,str]:
    csvFilePath = dir + csvFile
    
    df = pd.read_csv(csvFilePath, encoding='ISO-8859-1',sep=';', header=None)
    tabName = setTableName(csvFile)
    
    return df,tabName
