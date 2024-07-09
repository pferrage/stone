import src.tools.utils as ut
import src.silver.auxSilver as aux



def processSilverLayer(tabName,dt):
    df = aux.getAllRecordsFromABronzeTable(tabName,dt)
    df = aux.treatColumns(df,tabName)

    df = df.drop_duplicates()
    ut.loadDataFrameToSQL(df,tabName,'silver')
