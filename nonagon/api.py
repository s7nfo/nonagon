from flask import Flask, request, jsonify
from .db import DB

db = DB()

API = Flask("nonagon-api")


@API.route("/ingest", methods=["POST"])
def ingest_convo():
    """
    Endpoint to ingest a conversation and enque a job.

    Returns:
        A JSON response indicating the success status and job ID, or an error message.
    """

    data = request.get_json()

    if "conversation" not in data or not isinstance(data["conversation"], str):
        print(
            f"🤖 Invalid request to /ingest: 'conversation' key missing or not a string"
        )
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Invalid request: 'conversation' key missing or not a string",
                }
            ),
            400,
        )

    conversation = data["conversation"]
    job_id = db.create_job(conversation)

    print(f"🤖 Created job: {job_id}")

    return jsonify({"status": "success", "job_id": job_id})


@API.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    """
    Endpoint to retrieve the status of a specific job.

    Args:
        job_id (str): The unique identifier of the job.

    Returns:
        A JSON response containing the status of the job.
    """

    return jsonify({"status": "success", "job_status": db.get_job_status(job_id)})
