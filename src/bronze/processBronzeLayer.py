import bronze.auxBronze as aux
import tools.utils as ut


# Função para carga no nível Bronze do modelo Medalhão
def processBronzeLayer(source):
    try:
        df, tabName, dat_ingestion = aux.extractFileAndSave(source)
        
        # Carga na camada bronze
        ut.loadDataFrameToSQL(df,tabName,'bronze')

        return tabName,dat_ingestion
    except:
        print(f'A tabela {tabName} não foi criada/sobrescrita')