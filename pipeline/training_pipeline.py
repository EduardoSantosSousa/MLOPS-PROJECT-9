from src.data_processing import DataProcessing
from src.common_functions import read_yaml
from config.paths_config import *
from src.data_ingestion import DataIngestionAzure
from src.model_training import ModelTraining

if __name__ == "__main__":
    #config = read_yaml(file_path=CONFIG_PATH)

    #azure_params = {
    #    "connection_string": config['azure_storage_account_config']['connection_string'],
    #    "container_name": config['azure_storage_account_config']['container_name'],
    #    "blob_name": config['azure_storage_account_config']['blob_name'],
    #}

    # lê secrets primeiro, senão cai no YAML
    connection_string = os.getenv("CONNECTION_STRING")
    container_name    = os.getenv("CONTAINER_NAME")
    blob_name         = os.getenv("BLOB_NAME")
    
    if not (connection_string and container_name and blob_name):
        config = read_yaml(file_path=CONFIG_PATH)
        connection_string = connection_string or config['azure_storage_account_config']['connection_string']
        container_name    = container_name    or config['azure_storage_account_config']['container_name']
        blob_name         = blob_name         or config['azure_storage_account_config']['blob_name']

    azure_params = {
        "connection_string": connection_string,
        "container_name":    container_name,
        "blob_name":         blob_name,
    }

    data_ingestion = DataIngestionAzure(azure_params=azure_params, output_dir=RAW_DATA_DIR)
    data_ingestion.run()

    data_processor = DataProcessing(RAW_DATA)
    data_processor.run()

    trainer = ModelTraining()
    trainer.run()
