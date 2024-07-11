from jobs.processBronzeLayer import processBronzeLayer 
from jobs.processSilverLayer import processSilverLayer 
from jobs.processGoldLayer import processGoldLayer 
#from jobs.processCheckQuality import processCheckQuality

def main(files: tuple) -> tuple[None]:
    try:
        for file in files:
            try: tabName,dt_ingestion = processBronzeLayer(file)
            except: ('There was a problem loading the table in the Bronze layer')

            try: processSilverLayer(tabName,dt_ingestion)
            except: ('There was a problem loading the table in the Silver layer')
        
        try: processGoldLayer(dt_ingestion)
        except: print('Check that all tables are properly created in the Silver layer')
        
        print('Process completed successfully!')
    except: 
        print("The process hasn't been completed completely. Contact your system administrator.")

if __name__ == "__main__":
    main(['empresas','socios'])
