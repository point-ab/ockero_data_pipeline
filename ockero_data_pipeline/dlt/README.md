# dlt

## SS12000 Data Pipeline with dlt
A data pipeline built with [dlt (data load tool)](https://dlthub.com/) to extract and load data from SS12000 API endpoints.

## About

This project uses **dlt**, an open-source Python library for building scalable data pipelines. dlt handles the complex parts of data ingestion including:
- Automatic schema inference and evolution
- Incremental loading
- Data normalization and type detection
- Pipeline state management

### SS12000 API

SS12000 is a specification for student information systems in Sweden, providing standardized endpoints for accessing student, course, and organizational data.

## Features

- 🔄 Automated data extraction from SS12000 endpoints
- 🔐 Secure credential management with dlt secrets
- 📈 Handles pagination and nested data structures
- 🚀 Incremental loading support

## Prerequisites

- Python 3.8+
- Access to SS12000 API (API key required)
- Azure Blob Storage account (or configure another destination)

## Installation

1. Clone the repository:
2. Create and activate a virtual environment:
3. Install dependencies: pip install -r requirements.txt

## Configuration
1. .Env  -- use this!
3. Edit `.dlt/secrets.toml` and add your credentials:
3. Configure your pipeline settings in `config.toml` if needed.

## Usage

Run the pipeline:
```bash
python main.py
```

The pipeline will:
1. Extract data from configured SS12000 endpoints
2. Transform and normalize nested structures
3. Load data to your destination (Azure Blob Storage)

## Project Structure
```
.
├── main.py             # Main pipeline execution
├── sources/
│   └── source.py       # SS12000 API source configuration
├── pipeline.py         # Pipeline utilities
├── .dlt/               # dlt configuration (not in git)
│   ├── config.toml
│   └── secrets.toml
├── requirements.txt        # Python dependencies
├── README.md
└── .env               # Store keys and stuff (not in git)
```

## Endpoints


## Development

**Authentication errors?**
- Verify your API key in `.env` or `.dlt/secrets.toml`
- Check API endpoint URLs and permissions

## Resources

- [dlt Documentation](https://dlthub.com/docs)
- [dlt Slack Community](https://dlthub.com/community)
