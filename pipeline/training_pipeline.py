from src.data_processing import DataProcessing
from src.common_functions import read_yaml
from config.paths_config import *
from src.data_ingestion import DataIngestionAzure
from src.model_training import ModelTraining

if __name__ == "__main__":
    config = read_yaml(file_path=CONFIG_PATH)

    azure_params = {
        "connection_string": config['azure_storage_account_config']['connection_string'],
        "container_name": config['azure_storage_account_config']['container_name'],
        "blob_name": config['azure_storage_account_config']['blob_name'],
    }

    data_ingestion = DataIngestionAzure(azure_params=azure_params, output_dir=RAW_DATA_DIR)
    data_ingestion.run()

    data_processor = DataProcessing(RAW_DATA)
    data_processor.run()

    trainer = ModelTraining()
    trainer.run()
