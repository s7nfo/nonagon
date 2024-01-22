import toml

from nonagon.extractor import Extractor
from nonagon.issue_tracker import IssueTracker
from nonagon.api import API
from nonagon.backend import Backend
from nonagon.db import DB

if __name__ == "__main__":
    config = toml.load("config.toml")

    extractor = Extractor(**config["OpenAI"])
    issue_tracker = IssueTracker(**config["Linear"])

    backend = Backend(extractor, issue_tracker, DB)
    backend.run()

    API.run()
