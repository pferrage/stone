#Importa bibliotecas necessárias
import requests
import pandas as pd
import zipfile as zip
import os
from bs4 import BeautifulSoup
from datetime import datetime as dt
import tools.utils as ut

# Função que extrai um arquivo página "https://dadosabertos.rfb.gov.br/CNPJ/" e armazena localmente
def extractFileAndSave(file):
    
    dirFiles = 'files/'
    dirFliesCSV = 'files/csv/'
    os.makedirs(os.path.dirname(dirFiles), exist_ok=True)
    os.makedirs(os.path.dirname(dirFliesCSV), exist_ok=True)
    
    url = "https://dadosabertos.rfb.gov.br/CNPJ/"
    dat_ingestion = dt.now()
    
    #Função para raspagem de lista de arquivos disponíveis
    df_scraping = scrapingURL(url)

    file = selectBestFile(df_scraping,file)    
    getFile(url,file,dirFiles)

    fileCSV = file.replace('.zip','.csv')
    df,tabName = ut.getCSV(dirFliesCSV,fileCSV)
    
    df[['dat_ingestion']] = dat_ingestion
    
    return df,tabName,dat_ingestion

def scrapingURL(url):
    
    # Raspagem na URL indicada
    response = requests.get(url)
    response.raise_for_status() 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')


    # Converte extração em dataframe
    df = pd.read_html(str(table))[0]
    return df

def selectBestFile(df_scraping,file):

    # Filtra arquivo mais recente da lista
    df = df_scraping[df_scraping['Name'].str.contains(file, case=False, na=False)]
    df = df.sort_values(by='Last modified')
    file_name = df.iloc[-1]['Name']
    
    return file_name


# Extrai arquivos *.csv do diretório indicado
def extractZipFile(fileName,dir):

    filePath = dir + fileName
    dirCSV = dir + 'csv/'

    with zip.ZipFile(filePath, 'r') as zip_ref:
        zip_ref.extractall(dirCSV)

        for _fileName in zip_ref.namelist():
            newFileName = fileName.replace('.zip','.csv')

            if os.path.isfile(dirCSV + newFileName):
                os.remove(dirCSV + newFileName)

            os.rename(dirCSV + _fileName, dirCSV + newFileName)


# Função para extração arquivo do site indicado
def getFile(url,file,dir):
    try:
        
        filePath = dir + file
        fileName = file
        
        response = requests.get(url+file)
        response.raise_for_status()  

        if os.path.isfile(filePath):
            os.remove(filePath)
        
        with open(filePath, 'wb') as file:
            file.write(response.content)
        
        extractZipFile(fileName,dir)    
    except requests.RequestException as e:
        print(f"Falha ao baixar o arquivo. Erro: {e}")

