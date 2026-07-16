import os
from pathlib import Path

import kagglehub
import pandas as pd
import numpy as np
from dotenv import load_dotenv


from src.exception import CustomException
from src.logger import logger

load_dotenv()

class DataIngestion:
    def __init__(self)->None:
        self.dataset_name = os.getenv("KAGGLE_DATASET")

        if not self.dataset_name:
            raise ValueError(
                "KAGGLE_DATASET is not configured in the [.env] file"
            )
    
    def download_dataset(self) -> Path:
        try:
            logger.info(
                "Downloading Kaggle dataset: %s"
                ,self.dataset_name
            )

            dataset_path = Path(
                kagglehub.dataset_download(self.dataset_name)
            )

            logger.info(
                "Dataset downloaded to: %s"
                ,dataset_path
            )

            return dataset_path
        
        except Exception as exc:
            logger.exception("Dataset download failed")
            raise CustomException(exc) from exc
        
    
    def list_dataset_files(self, dataset_path: Path) -> list[Path]:
        try:
            files = [
            path
            for path in dataset_path.rglob("*")
            if path.is_file()
        ]

            for file_path in files:
                logger.info("Dataset file found: %s", file_path) #because of lazy evaluation use %s | Efficiency: If logger is set to only show ERROR messages, it won't waste CPU power merging ("interpolating") those strings together for an INFO message that never gets displayed.

            return files
        
        except Exception as exc:
            logger.exception("Failed to list dataset files")
            raise CustomException(exc) from exc
        
    def find_csv_file(
            self
            ,dataset_files: list[Path]
    ) -> None:
        try:
            csv_files= [ 
                file_path
                for file_path in dataset_files
                if file_path.suffix.lower() == ".csv"
            ]

            if not csv_files:
                raise FileNotFoundError(
                    "Np csv file was found in the downloaded dataset"
                )
            
            if len(csv_files) >1:
                raise ValueError(
                    f"Expected one CSV file, but found {len(csv_files)}"
                )
            
            csv_file = csv_files[0]

            logger.info(
                "CSV file selected: %s"
                ,csv_file
            )

            return csv_file
        except Exception as exc:
            logger.exception(
                "Failed to select the dataset CSV file"
            )
            raise CustomException(exc) from exc

    def read_dataset(
            self
            ,csv_file: Path
    ) -> pd.DataFrame:
        try:
            logger.info(
                "Readin dataset from: %s"
                ,csv_file
            )

            dataframe = pd.read_csv(csv_file)

            logger.info(
                "Dataset data types: %s"
                ,dataframe.dtypes.astype(str).to_dict()
            )

            return dataframe
        
        except Exception as exc:
            logger.exception("Failed to read the dataset")
            raise CustomException(exc) from exc
        

if __name__=="__main__":
    ingestion = DataIngestion()

    downloaded_path = ingestion.download_dataset()
    dataset_files = ingestion.list_dataset_files(downloaded_path)

    csv_file = ingestion.find_csv_file(
        dataset_files
    )

    dataframe = ingestion.read_dataset(
        csv_file
    )

    print("\nDataset technical structure:")
    print(f"CSV file: {csv_file}")
    print(f"Rows: {dataframe.shape[0]}")
    print(f"Column: {dataframe.shape[1]}")

    print("\nColumn data types:")
    print(dataframe.dtypes)
