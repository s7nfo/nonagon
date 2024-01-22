from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


class IssueTracker:
    def __init__(self, api_key: str, team_id: str) -> None:
        """Initializes IssueTracker with API key and team ID.
        Args:
            api_key (str): Your Linear API key.
            team_id (str): Your Linear team ID.
        """

        self.team_id = team_id

        transport = RequestsHTTPTransport(
            url="https://api.linear.app/graphql",
            headers={"Authorization": f"{api_key}"},
        )
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    def make_ticket(self, title: str, description: str) -> dict[str, any]:
        """Creates a ticket in Linear with a given title and description.

        Args:
            title (str): The title of the ticket.
            description (str): The description of the ticket.
        """

        print(f"🎟️ Making ticket {title}.")

        query = gql(
            """
            mutation IssueCreate($title: String!, $description: String!, $team_id: String!) {
                issueCreate(
                    input: {
                        title: $title
                        description: $description
                        teamId: $team_id
                    }
                ) {
                    success
                    issue {
                        id
                        title
                    }
                }
            }
        """
        )

        return self.client.execute(
            query,
            variable_values={
                "title": title,
                "description": description,
                "team_id": self.team_id,
            },
        )

    def get_tickets(self) -> dict[str, any]:
        """Retrieves all tickets for the specified team."""

        print(f"🎟️ Listing tickets.")
        # Define your GraphQL query
        query = gql(
            """
            query($team_id: String!) {
                team(id: $team_id) {
                    issues {
                    nodes {
                        id
                        title
                        description
                        state {
                        name
                        }
                    }
                    }
                }
                }

        """
        )

        return self.client.execute(
            query,
            variable_values={
                "team_id": self.team_id,
            },
        )[
            "team"
        ]["issues"]["nodes"]

    def add_comment(self, ticket_id: str, body: str) -> dict[str, any]:
        """Adds a comment to a specified ticket.
        Args:
            ticket_id (str): The ID of the ticket.
            body (str): The comment text.
        """

        print(f"🎟️ Adding comment to ticket {ticket_id}.")

        query = gql(
            """
            mutation commentCreate($issue_id: String!, $body: String!) {
                commentCreate(
                    input: {
                        issueId: $issue_id
                        body: $body
                    }
                ) {
                    success
                }
            }
        """
        )

        return self.client.execute(
            query,
            variable_values={
                "issue_id": ticket_id,
                "body": body,
            },
        )
