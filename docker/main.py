from src.bronze.processBronzeLayer import processBronzeLayer 
from src.silver.processSilverLayer import processSilverLayer 
from src.gold.processGoldLayer import processGoldLayer
#from src.quality.processCheckQuality import processCheckQuality



def processETL(file):
    try:
        tabName,dt_ingestion = processBronzeLayer(file)
        processSilverLayer(tabName,dt_ingestion)
        processGoldLayer(dt_ingestion)
        print(f'O arquivo foi carregado com sucesso na tabela {tabName} em todos os ambientes.')
    except: 
        print('O arquivo não foi carregado, contacte o administrador')