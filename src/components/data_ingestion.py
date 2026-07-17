import os
from pathlib import Path

import kagglehub
import pandas as pd
from dotenv import load_dotenv

from src.database.engine import engine
from src.database.repository import load_raw_loan_data
from src.database.setup import initialize_database

from src.exception import CustomException
from src.logger import logger

load_dotenv()

class DataIngestion:
    def __init__(self) -> None:
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
        
    
    def list_dataset_files(
            self
            ,dataset_path: Path
            ) -> list[Path]:
        try:
            logger.info("Searching for dataset files in: %s"
                        ,dataset_path)

            files = [
            path
            for path in dataset_path.rglob("*")
            if path.is_file()
        ]

            for file_path in files:
                logger.info("Dataset file found: %s", file_path) #because of lazy evaluation use %s | Efficiency: If logger is set to only show ERROR messages, it won't waste CPU power merging ("interpolating") those strings together for an INFO message that never gets displayed.

            logger.info(
                "Dataset file search completed: %s files found"
                ,len(files)
            )
            
            return files
        
        except Exception as exc:
            logger.exception("Failed to list dataset files")
            raise CustomException(exc) from exc
        
    def find_csv_file(
            self
            ,dataset_files: list[Path]
    ) -> Path:
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
                "Dataset loaded successfully: %s rows, %s columns"
                ,dataframe.shape[0]
                ,dataframe.shape[1]
            )

            logger.info(
                "Dataset data types: %s"
                ,dataframe.dtypes.astype(str).to_dict()
            )

            return dataframe
        
        except Exception as exc:
            logger.exception("Failed to read the dataset")
            raise CustomException(exc) from exc
        

    def normalize_column_names(
            self
            ,dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        
        try:
            logger.info("Starting dataset column normalization")

            column_mapping = {
                "LoanID" :"loan_id"
                ,"Age" : "age"
                ,"Income" : "income"
                ,"LoanAmount" : "loan_amount"
                ,"CreditScore" : "credit_score"
                ,"MonthsEmployed" : "months_employed"
                ,"NumCreditLines" : "num_credit_lines"
                ,"InterestRate" : "interest_rate"
                ,"LoanTerm" : "loan_term"
                ,"DTIRatio" : "dti_ratio"
                ,"Education" : "education"
                ,"EmploymentType" : "employment_type"
                ,"MaritalStatus" : "marital_status"
                ,"HasMortgage" : "has_mortgage"
                ,"HasDependents" : "has_dependents"
                ,"LoanPurpose" : "loan_purpose"
                ,"HasCoSigner" : "has_cosigner"
                ,"Default" : "default"
            }

            missing_columns = set(column_mapping) - set (
                dataframe.columns
            )

            if missing_columns:
                raise ValueError(
                    "Dataset is missing expected columns: "
                    f"{sorted(missing_columns)}"
                )
            
            normalized_dataframe = dataframe.rename(
                columns = column_mapping
            ).copy()

            logger.info(
                "Dataset columns normalized successfully: %s"
                ,normalized_dataframe.columns.to_list()
            )

            return normalized_dataframe

        except Exception as exc:
            logger.exception(
                "Failed to normalize dataset columns"
            )

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

    normalized_dataframe = ingestion.normalize_column_names(
        dataframe
    )

    initialize_database(engine)

    loaded_rows = load_raw_loan_data(
        dataframe = normalized_dataframe
        ,engine = engine
        ,replace_existing = True
    )

    logger.info(
        "Data ingestion workflow completed successfully: %s rows loaded"
        , loaded_rows
    )

    print("\nDataset technical completed:")
    print(f"CSV file: {csv_file}")

    print(f"Rows loaded: {loaded_rows}")
    print(f"Columns: {normalized_dataframe.shape[1]}")
    print("\nColumn data types:")
    print(normalized_dataframe.dtypes)

    print("Destination: ml.raw_loan_defaults")