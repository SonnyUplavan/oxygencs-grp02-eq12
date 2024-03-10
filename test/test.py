import unittest
from unittest.mock import patch
from src.main import App
import psycopg2

class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up your App instance with mocked environment variables
        with patch.dict('os.environ', {
            'HOST_ENV': 'http://mocked_host',
            'HOST_TOKEN': 'mocked_token',
            'OXYGEN_T_MAX': '30',
            'OXYGEN_T_MIN': '10',
            'OXYGEN_DATABASE_URL': 'postgresql://mocked_user:mocked_password@mocked_host:5432/mock_db',
        }):
            self.app = App()

    @patch('psycopg2.connect')
    def test_database_connection(self, mock_connect):
        # Set up mocked values for database connection
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value

        # Set up the mock to raise an exception when execute is called
        mock_cursor.execute.side_effect = psycopg2.Error('Error saving HVAC event to the database:')

        # Test database connection and insertion
        with self.assertRaises(psycopg2.Error) as context:
            self.app.save_event_to_database('2024-03-10 12:00:00', 25.0)

        # Assert that the appropriate methods are called
        mock_connect.assert_called_once_with(
            dbname='db02eq12',
            user='user02eq12',
            password='E84YDXF2l5P4FkFG',
            host='157.230.69.113',
            port='5432',
        )

        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO hvac_events (timestamp_event, temperature, event_type) VALUES (%s, %s, %s)",
            ('2024-03-10 12:00:00', 25.0, 'None'),
        )
        # Assert that commit, close, and close are NOT called in case of an exception
        mock_connection = mock_connect.return_value
        mock_connection.commit.assert_not_called()
        mock_cursor.close.assert_not_called()
        mock_connection.close.assert_not_called()

        # Ensure that the exception was raised with the expected error message
        self.assertEqual(str(context.exception), "Error saving HVAC event to the database:")

    def test_environment_variables(self):
        # Test that environment variables are correctly set in the App instance
        self.assertEqual(self.app.HOST, 'http://mocked_host')
        self.assertEqual(self.app.TOKEN, 'mocked_token')
        self.assertEqual(self.app.T_MAX, '30')
        self.assertEqual(self.app.T_MIN, '10')
        self.assertEqual(
            self.app.DATABASE_URL,
            'postgresql://mocked_user:mocked_password@mocked_host:5432/mock_db',
        )

if __name__ == '__main__':
    unittest.main()
