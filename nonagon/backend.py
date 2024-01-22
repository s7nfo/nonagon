import threading
from .db import DB
from .issue_tracker import IssueTracker
from .extractor import Extractor


class Backend:
    def __init__(
        self, extractor: Extractor, issue_tracker: IssueTracker, db: DB
    ) -> None:
        """Initializes the Backend with an extractor and an issue tracker.
        Args:
            classifier: An instance of the classifier object.
            issue_tracker: An instance of the IssueTracker object.
        """

        self.extractor = extractor
        self.issue_tracker = issue_tracker
        self.DB = db

    def _process_jobs(self) -> None:
        """Continually processes each pending job by extracting data from text and updating the issue tracker."""
        db = self.DB()

        while True:
            self._process_job(db)

    def _process_job(self, db: DB) -> None:
        """Processes a single pending job by extracting data from text and updating the issue tracker.
        Separated from _process_jobs for to simplify testing.
        Args:
            db: An instance of the DB object.
        """
        pending_jobs = db.get_pending_jobs()

        if len(pending_jobs) > 0:
            print(f"🧠 Found {len(pending_jobs)} new pending jobs.")

        for job_id, conversation in pending_jobs:
            print("🧠 Processing job {}...".format(job_id))

            try:
                existing_tickets = self.issue_tracker.get_tickets()

                extract = self.extractor.extract(conversation, existing_tickets)

                # If we've extracted a feature request and there are related tickets,
                # add a comment to each ticket. Otherwise, make a new ticket.
                if extract["feature_request"]:
                    if extract["feature_request"]["related_tickets"]:
                        for ticket_id in extract["feature_request"]["related_tickets"]:
                            self.issue_tracker.add_comment(ticket_id, conversation)
                    else:
                        self.issue_tracker.make_ticket(
                            title="Feature request: "
                            + extract["feature_request"]["description"],
                            description=conversation,
                        )

                # If we've extracted a bug report and there are related tickets,
                # add a comment to each ticket. Otherwise, make a new ticket.
                if extract["bug_report"]:
                    if extract["bug_report"]["related_tickets"]:
                        for ticket_id in extract["bug_report"]["related_tickets"]:
                            self.issue_tracker.add_comment(ticket_id, conversation)
                    else:
                        self.issue_tracker.make_ticket(
                            title="Bug report: " + extract["bug_report"]["description"],
                            description=conversation,
                        )
            except Exception as e:
                print(f"🧠 Job {job_id} failed: {e}")
                db.set_job_status(job_id, "failed")
                continue

            db.set_job_status(job_id, "complete")

    def run(self) -> None:
        """Starts the job processing thread."""

        threading.Thread(target=self._process_jobs).start()
