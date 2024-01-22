import unittest
from unittest.mock import patch
from nonagon.backend import Backend


class TestBackend(unittest.TestCase):
    @patch("nonagon.extractor.Extractor")
    @patch("nonagon.issue_tracker.IssueTracker")
    @patch("nonagon.db.DB")
    def test_backend_no_related_tickets(
        self, mock_extractor, mock_issue_tracker, mock_db
    ):
        # Set up the mock return value for the extract method
        mock_extractor_instance = mock_extractor.return_value
        mock_extractor_instance.extract.return_value = {
            "feature_request": {
                "description": "some_description",
                "related_tickets": [],
            },
            "bug_report": None,
        }
        mock_issue_tracker_instance = mock_issue_tracker.return_value
        mock_db.get_pending_jobs.return_value = [(1, "some_conversation")]

        # Instantiate the Backend with the mocked Extractor
        backend = Backend(mock_extractor_instance, mock_issue_tracker_instance, mock_db)
        backend._process_job(mock_db)

        # Assertions
        mock_extractor_instance.extract.assert_called_once()
        mock_issue_tracker_instance.make_ticket.assert_called_once()
        mock_issue_tracker_instance.add_comment.assert_not_called()

    @patch("nonagon.extractor.Extractor")
    @patch("nonagon.issue_tracker.IssueTracker")
    @patch("nonagon.db.DB")
    def test_backend_some_related_tickets(
        self, mock_extractor, mock_issue_tracker, mock_db
    ):
        # Set up the mock return value for the extract method
        mock_extractor_instance = mock_extractor.return_value
        mock_extractor_instance.extract.return_value = {
            "feature_request": {
                "description": "some_description",
                "related_tickets": ["1234"],
            },
            "bug_report": None,
        }
        mock_issue_tracker_instance = mock_issue_tracker.return_value
        mock_issue_tracker_instance.get_tickets.return_value = {
            "team": {"issues": {"nodes": []}}
        }
        mock_db.get_pending_jobs.return_value = [(1, "some_conversation")]

        # Instantiate the Backend with the mocked Extractor
        backend = Backend(mock_extractor_instance, mock_issue_tracker_instance, mock_db)
        backend._process_job(mock_db)

        # Assertions
        mock_extractor_instance.extract.assert_called_once()
        mock_issue_tracker_instance.add_comment.assert_called_once()
        mock_issue_tracker_instance.make_ticket.assert_not_called()


if __name__ == "__main__":
    unittest.main()
