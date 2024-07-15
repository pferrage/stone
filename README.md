# Data engineer - Challenge

## Overview
Insights on data extracted from the Brazilian Federal Revenue Service's Open Data Portal. 
The data is available via the link: https://dadosabertos.rfb.gov.br/CNPJ/

## Data Processing Project
This project is responsible for downloading, processing and storing company and member data, dividing processing into three layers: bronze, silver and gold.
The process also allows for the storage of other data from the same public repository.

### Project architecture
![image](https://github.com/user-attachments/assets/269e6866-b39f-46f9-b2e4-11f385a4deb8)

### Data project structure
src/</br>
├── jobs/</br>
│ ├── processBronzeLayer.py</br>
│ ├── processSilverLayer.py</br>
│ ├── processGoldLayer.py</br>
│ └── processDataQuality.py</br>
├── tools/</br>
│ └── utils.py</br>
└── main.py</br>

#### Process Bronze Layer (processBronzeLayer.py)
><b>Scraping and Download:</b> It uses a python data scraping library on the page with open data, to search for the list of available files and their respective update dates. The tool also selects the most up-to-date file to be uploaded and downloads it.

><b>Extract and Save:</b> This step is responsible for extracting the *.csv file from within the *.zip downloaded from the portal. The *.csv file is then stored locally and renamed.

><b>Database loading:</b> This step is responsible for converting the *.csv data into a "stndb_bronze" dataset, without any processing.

#### Process Silver Layer (processSilverLayer.py)
><b>Preparing data:</b> Essa etapa seleciona os dados recém carregados na camada Bronze, trata a tipagem correta de cada coluna e as renomeia.
><b>Database loading:</b> Com os dados tratados, essa etapa carrega nuam tabela com o mesmo nome no dataset: "stndb_silver".

#### Process Gold Layer (processGoldLayer.py)
><b>Consolidated data:</b> After loading the tables needed for the flow, the Gold layer process is responsible for selecting existing (and relevant) data from the "stndb_silver" dataset, extracting relevant insights and loading a table with the consolidated data into a table in the "stndb_gold" dataset.

#### Layers
><b>Bronze layer:</b> Used by ingest applications to write data replicated from the source. May contain duplicates and columns added during ingestion:</br>
✅ Ingestion-specific columns and tags (dat_ingestion, max_ref_date, etc);</br>
✅ Duplicate data;</br>
✅ Columns without type treatment;</br>
❌ Used by other applications.

><b>Silver layer:</b> Mapping of business entities. First layer available for business areas:</br>
✅ Deduplicated data;</br>
✅ Treated columns (type and name);</br>
❌ Aggregations;</br>
❌ Metrics.

><b>Gold layer:</b> Activation layer. Data ready to be consumed and with added value:</br>
✅ Metrics;</br>
✅ Separated by domain or area of interest;</br>
✅ Accessible for dataviz;</br>
❌ Uses data directly from the Bronze layer.

### Database management
The system uses MySQL as the data management tool for all layers. 

#### MySQL connection
    - MYSQL_HOST=mysql
    - MYSQL_PORT=3306
    - MYSQL_USER=root
    - MYSQL_PASSWORD=root_password
#### Tables
***stndb/bronze*** </br>
Tables with all the records extracted from the *csv file contained within the *.zip downloaded from the public repository. Following the premises of the Bronze layer 
- tb_empresas
- tb_socios</br>

***stndb/silver***</br>
Tables taken from the bronze layer, with column treatment (naming and typing). Following the premises of the silver layer
</br>
- tb_empresas
- tb_socios</br>

***stndb/gold***</br>
In this project, only one table was created in the Gold layer. The " tb_consolidado_socios " table is a consolidation of the " tb_empresas " and " tb_socios " tables. It returns the number of partners in each company, a flag indicating whether or not the company has any foreign partners and a flag indicating whether the company is size 3. Following the assumptions of the gold layer</br>
- tb_consolidado_socios

## Run project
### Requirements
1. Internet connection (to download files)
2. 16GB of RAM
3. ```Docker``` latest version.
### Step-by-step
1. Clone this repository
2. Unzip the folder
3. Use cmd to access the project folder
4. type: ```docker-compose down && docker-compose up -d```
5. Wait for the services to start and for the data ingestion pipeline to run
6. Next the service has been run, the following message should appear on the console: ***"All tables have been properly created"***
