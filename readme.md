# Nonagon

![Nonagon Architecture](/diagram.png)

## Installation

To install Nonagon, follow these steps:

1. Clone the repository:
```bash
git clone git@github.com:s7nfo/nonagon.git
cd nonagon
pip install -r requirements.txt
```

## Configuration

Nonagon requires a `config.toml` in the root directory:

```toml
[OpenAI]
api_key = "your_openai_api_key"

[Linear]
api_key = "your_linear_api_key"
team_id = "your_linear_team_id"
```

## Running Nonagon

```bash
python nonagon.py
```

## Ingesting conversations

```bash
./ingest.sh "sudo make me a sandwich"
```

## System Overview

### Endpoints

1. **Ingest Endpoint (`/ingest`)**

   - **Method**: POST
   - **Functionality**: This endpoint is used to submit text conversations to Nonagon.
   - **Parameters**:
     - `conversation`: A string containing the text conversation to be processed.
   - **Returns**:
     - `status`: Indicates the success or error of the ingestion call.
     - `job_id`: A unique identifier for the submitted job, used for tracking the processing status.

2. **Job Status Endpoint (`/jobs/<job_id>`)**

   - **Method**: GET
   - **Functionality**: Retrieves the processing status of a submitted job using its `job_id`.
   - **Usage**: Replace `<job_id>` with the actual job ID received from the ingest endpoint.
   - **Returns**:
     - `status`: Indicates the success or error of the job status call.
     - `job_status`: Indicates status of the referenced job.