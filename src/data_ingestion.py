# data_ingestion.py
import pandas as pd
from azure.storage.blob import BlobServiceClient
import os
import sys
from src.logger import get_logger
from src.custom_exception import CustomException
from src.common_functions import read_yaml
from config.paths_config import *

logger = get_logger(__name__)

class DataIngestionAzure:

    def __init__(self, azure_params, output_dir):
        """
        azure_params deve conter:
          - "connection_string": "<sua_connection_string>"
          - "container_name": "<nome_do_container>"
          - "blob_name": "<nome_do_arquivo_no_blob>"
        """
        self.azure_params = azure_params
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

    def extract_data(self):
        """
        Baixa o CSV do Azure Blob Storage.
        """
        try:
            logger.info("Starting Azure Blob download...")

            blob_service_client = BlobServiceClient.from_connection_string(self.azure_params['connection_string'])
            blob_client = blob_service_client.get_blob_client(container=self.azure_params['container_name'],
                                                              blob=self.azure_params['blob_name'])

            local_file = os.path.join(self.output_dir, self.azure_params['blob_name'])

            with open(local_file, "wb") as f:
                f.write(blob_client.download_blob().readall())

            logger.info("Downloaded CSV from Azure Blob Storage.")
            df = pd.read_csv(local_file)
            return df

        except Exception as e:
            logger.error(f"Error while downloading from Azure Blob: {e}")
            raise CustomException(str(e), sys)

    def save_data(self, df):
        try:
            local_file = os.path.join(self.output_dir, "data.csv")
            df.to_csv(local_file, index=None)
            logger.info("Data saved locally.")
        except Exception as e:
            logger.error(f"Error while saving data: {e}")
            raise CustomException(str(e), sys)

    def run(self):
        try:
            logger.info("Data Ingestion Pipeline Started....")
            df = self.extract_data()
            self.save_data(df)
            logger.info("End of Data Ingestion Pipeline....")
        except Exception as e:
            logger.error(f"Error in data ingestion pipeline: {e}")
            raise CustomException(str(e), sys)


if __name__ == "__main__":
    config = read_yaml(file_path=CONFIG_PATH)

    azure_params = {
        "connection_string": config['azure_storage_account_config']['connection_string'],
        "container_name": config['azure_storage_account_config']['container_name'],
        "blob_name": config['azure_storage_account_config']['blob_name'],
    }

    data_ingestion = DataIngestionAzure(azure_params=azure_params, output_dir=RAW_DATA_DIR)
    data_ingestion.run()

