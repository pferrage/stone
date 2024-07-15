from jobs.processBronzeLayer import processBronzeLayer 
from jobs.processSilverLayer import processSilverLayer 
from jobs.processGoldLayer import processGoldLayer 

def main(files: tuple) -> tuple[None]:
    try:
        for file in files:
            tabName,dt_ingestion = processBronzeLayer(file)
            processSilverLayer(tabName)
            
        processGoldLayer(dt_ingestion)
        print('All tables have been properly created')
    except Exception as e:
        error_message = f"Data processing error: : {str(e)}"
        return None, error_message  

if __name__ == "__main__":
    main(['empresas','socios'])