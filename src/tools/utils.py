import sqlite3
import re
import pandas as pd
import os


def loadDataFrameToSQL(df: pd.DataFrame, table: str, db: str) -> tuple[None]:
    try:
        db_path = 'sqlite3/stndb_' + db
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        con = sqlite3.connect(db_path)        
        df.to_sql(con=con, name=table, if_exists="replace",index=False)
        con.close()
    except:
        con.close()  

def loadSQLToDataFrame(query: str, db: str) -> tuple[pd.DataFrame]:
    try: 
        db_path = 'sqlite3/stndb_' + db
        con = sqlite3.connect(db_path)
        df = pd.read_sql(query,con=con)
        con.close()
        return df
    except:
        con.close()
    
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