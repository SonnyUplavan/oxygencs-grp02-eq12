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
    
   

if __name__ == '__main__':
    unittest.main()
