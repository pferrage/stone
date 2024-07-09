# Importando bibliotecas
import sqlite3
import re
import pandas as pd
import os


# Função para carregar um dataframe em uma tabela do SQLite
def loadDataFrameToSQL(df, table, db):
    try:
        con = sqlite3.connect('sqlite3/stonedb_'+ db)        
        df.to_sql(con=con, name=table, if_exists="replace",index=False)
        con.close()
    except:
        con.close()  

# Função para carregar uma tabela do SQLite em um dataframe 
def loadSQLToDataFrame(query, db):
    try: 
        con = sqlite3.connect('sqlite3/stonedb_'+ db)
        df = pd.read_sql(query,con=con)
        con.close()
        return df
    except:
        con.close()
    

# Função que retorna verdadeiro se o texto contiver números (usado para validar se o nome do arquivo baixo tem um indicativo de versão)
def checkNumber(text):
    default = re.compile(r'\d')
    result = default.search(text)
    return bool(result)

# Função para eliminar caracteres especiais e números do texto (para criação do nome da tabela)
def adjustText(text):

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

# Função para tratar a variável que irá nomear a tabela
def setTableName(text):
    tabName = text.lower()
    tabName = tabName.replace('.csv','')
    tabName = 'tb_' + adjustText(tabName)
    
    return tabName


#Função para capturar arquivo CSV compactado
def getCSV(dir,csvFile):
    
    csvFilePath = dir + csvFile
    
    #Armazena em um Dataframe os dados do CSV dentro do arquivo baixado
    df = pd.read_csv(csvFilePath, encoding='ISO-8859-1',sep=';', header=None)    
    tabName = setTableName(csvFile)
    
    return df,tabName