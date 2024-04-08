import unittest
from unittest.mock import patch, MagicMock
from src.main import App
import psycopg2

class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up your App instance with mocked environment variables
        with patch.dict(
            "os.environ",
            {
                "HOST_ENV": "http://mocked_host",
                "HOST_TOKEN": "mocked_token",
                "OXYGEN_T_MAX": "30",
                "OXYGEN_T_MIN": "10",
                "OXYGEN_DATABASE_URL": "postgresql://mocked_user:mocked_password@mocked_host:5432/mock_db",
            },
        ):
            self.app = App()
            # Ensure that the database connection is set up before each test
            self.app.setup_database_connection()


    def test_environment_variables(self):
        # Test that environment variables are correctly set in the App instance
        self.assertEqual(self.app.HOST, "http://mocked_host")
        self.assertEqual(self.app.TOKEN, "mocked_token")
        self.assertEqual(self.app.T_MAX, "30")
        self.assertEqual(self.app.T_MIN, "10")
        self.assertEqual(
            self.app.DATABASE_URL,
            "postgresql://mocked_user:mocked_password@mocked_host:5432/mock_db",
        )
    
    def test_insert_value_into_database(self):
        # Define your database connection parameters
        DB_CONNECTION_PARAMS = {
            "dbname": "db02eq12",
            "user": "user02eq12",
            "password": "E84YDXF2l5P4FkFG",
            "host": "157.230.69.113",
            "port": "5432",
        }

        # Establish a connection to the database
        try:
            conn = psycopg2.connect(**DB_CONNECTION_PARAMS)
        except psycopg2.Error as e:
            self.fail(f"Error connecting to the database: {e}")

        # Define the data you want to insert into the database
        data = ("2024-04-04 12:00:00", 25.0, "None")

        # Define the SQL statement to insert data into the table
        insert_query = """
            INSERT INTO hvac_events (timestamp_event, temperature, event_type)
            VALUES (%s, %s, %s)
        """

        # Insert data into the database
        try:
            with conn.cursor() as cursor:
                cursor.execute(insert_query, data)
                conn.commit()
        except psycopg2.Error as e:
            self.fail(f"Error inserting data into the database: {e}")
        finally:
            # Close the database connection
            conn.close()

if __name__ == '__main__':
    unittest.main()
