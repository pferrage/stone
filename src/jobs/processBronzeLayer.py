import requests
import pandas as pd
import zipfile as zip
import os
from bs4 import BeautifulSoup
from datetime import datetime as dt
import jobs.utils as ut


def processBronzeLayer(source: str) -> tuple[str,object]:
    df, tabName, dat_ingestion = extractFileAndSave(source)
    ut.loadDataFrameToSQL(df,tabName,'bronze')
        
    return tabName,dat_ingestion
    
def extractFileAndSave(file: str) -> tuple[pd.DataFrame, str, object]:
    dirFiles = 'files/'
    dirFliesCSV = 'files/csv/'
    url = "https://dadosabertos.rfb.gov.br/CNPJ/"
    dat_ingestion = dt.now()

    os.makedirs(os.path.dirname(dirFiles), exist_ok=True)
    os.makedirs(os.path.dirname(dirFliesCSV), exist_ok=True)    
        
    df_scraping = scrapingURL(url)
    file = selectBestFile(df_scraping,file)    
    getFile(url,file,dirFiles)
    
    fileCSV = file.replace('.zip','.csv')
    df,tabName = ut.getCSV(dirFliesCSV,fileCSV)
    df[['dat_ingestion']] = dat_ingestion

    return df,tabName,dat_ingestion

def scrapingURL(url: str) -> tuple[pd.DataFrame]:
    
    response = requests.get(url)
    response.raise_for_status() 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')

    df = pd.read_html(str(table))[0]

    return df

def selectBestFile(df_scraping: pd.DataFrame,file: str) -> tuple[str]:

    df = df_scraping[df_scraping['Name'].str.contains(file, case=False, na=False)]
    df = df.sort_values(by='Last modified')
    file_name = df.iloc[-1]['Name']
    
    return file_name

def getFile(url: str,file: str,dir: str) -> tuple[None]:
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
        print(f"Failed to download the file. Error: {e}")


def extractZipFile(fileName: str,dir: str) -> tuple[None]:

    filePath = dir + fileName
    dirCSV = dir + 'csv/'

    with zip.ZipFile(filePath, 'r') as zip_ref:
        zip_ref.extractall(dirCSV)

        for _fileName in zip_ref.namelist():
            newFileName = fileName.replace('.zip','.csv')

            if os.path.isfile(dirCSV + newFileName):
                os.remove(dirCSV + newFileName)

            os.rename(dirCSV + _fileName, dirCSV + newFileName)
