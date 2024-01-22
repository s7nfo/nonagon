#!/bin/bash

# API endpoints
INGEST_ENDPOINT="http://127.0.0.1:5000/ingest"
STATUS_ENDPOINT="http://127.0.0.1:5000/jobs/"

CONVERSATION_JSON="{\"conversation\": \"${*}\"}"

# POST request to the ingest endpoint and capture the response
RESPONSE=$(curl -s -X POST $INGEST_ENDPOINT \
               -H "Content-Type: application/json" \
               -d "$CONVERSATION_JSON")

echo "Response from server: $RESPONSE"
