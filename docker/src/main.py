from bronze.processBronzeLayer import processBronzeLayer 
from silver.processSilverLayer import processSilverLayer 
from gold.processGoldLayer import processGoldLayer
#from src.quality.processCheckQuality import processCheckQuality

def main(file):
    try:
        try: tabName,dt_ingestion = processBronzeLayer(file)
        except: ('Houve um problema na carga da tabela na camada Bronze')

        try: processSilverLayer(tabName,dt_ingestion)
        except: ('Houve um problema na carga da tabela na camada Silver')
        
        try: processGoldLayer(dt_ingestion)
        except: print('Verifique se as tabelas tb_empresas e tb_socios estão criadas na camada Silver')
        
        print(f'O arquivo foi carregado com sucesso na tabela {tabName} em todos os ambientes.')
    except: 
        print('O arquivo não foi carregado, contacte o administrador')

if __name__ == "__main__":
    main('empresas')
    main('socios')
