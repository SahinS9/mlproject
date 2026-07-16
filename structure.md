mlproject/
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   └── model_evaluation.py
│   │
│   ├── pipeline/
│   │   ├── training_pipeline.py
│   │   └── prediction_pipeline.py
│   │
│   ├── api/
│   │   ├── main.py
│   │   ├── dependencies.py
│   │   ├── schemas.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── predictions.py
│   │   │   ├── pages.py
│   │   │   └── health.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   └── prediction_service.py
│   │   ├── templates/
│   │   └── static/
│   │
│   ├── database/
│   │   ├── engine.py
│   │   ├── models.py
│   │   └── repository.py
│   │
│   ├── exception.py
│   ├── logger.py
│   └── utils.py
│
├── tests/
├── requirements.txt
├── README.md
└── .env