import sqlite3
import uuid

class DB:
    DATABASE = 'nonagon.db'

    def get_conn(self) -> sqlite3.Connection:
        """Establishes and returns a database connection."""

        return sqlite3.connect(self.DATABASE)

    def __init__(self) -> None:
        """Initializes the database and creates tables if they do not exist."""

        self.create_tables()

    def create_tables(self) -> None:
        """Creates the jobs table in the database, if it doesn't exist."""

        conn = self.get_conn()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                conversation TEXT NOT NULL
            )
        ''')
        conn.commit()

    def create_job(self, conversation: str) -> str:
        """Creates a new job record in the database.
        Args:
            conversation (str): The conversation text associated with the job.
        Returns:
            str: ID of the created job.
        """

        conn = self.get_conn()
        job_id = uuid.uuid4().hex
        conn.execute('''
            INSERT INTO jobs (id, status, created_at, updated_at, conversation)
            VALUES (?, ?, datetime('now'), datetime('now'), ?)
        ''', (job_id, 'pending', conversation))
        conn.commit()
        return job_id
    
    def get_pending_jobs(self) -> list[tuple]:
        """Retrieves all jobs with a 'pending' status, oldest first.
        Returns:
            list of tuples: A list of tuples containing job IDs and conversation texts.
        """
        
        conn = self.get_conn()
        cursor = conn.execute('''
            SELECT id, conversation FROM jobs WHERE status = 'pending' ORDER BY updated_at ASC
        ''')
        rows = cursor.fetchall()
        return rows
    
    def get_job_status(self, job_id: str) -> str:
        """Gets the status of a specific job, if it exists.
        Args:
            job_id (str): The ID of the job.
        Returns:
            str: The status of the job or None if not found.
        """
               
        conn = self.get_conn()
        cursor = conn.execute('''
            SELECT status FROM jobs WHERE id = ?
        ''', (job_id,))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None
        
    def set_job_status(self, job_id: str, status: str) -> str:
        """Updates the status of a specific job.
        Args:
            job_id (str): The ID of the job.
            status (str): The new status to be set.
        """
               
        conn = self.get_conn()
        conn.execute('''
            UPDATE jobs SET status = ?, updated_at = datetime('now') WHERE id = ?
        ''', (status, job_id))
        conn.commit()