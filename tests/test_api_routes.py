import os
import json
import unittest
from your_flask_app import create_app

class FlaskAppTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment for each test method."""
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()
        self.demo_user_token = os.getenv('DEMO_USER_TOKEN')

    def tearDown(self):
        """Clean up after each test method."""
        pass

    def test_health_endpoint_response(self):
        """Test the health check endpoint for expected response."""
        response = self.client.get('/health_check')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        responseData = response.get_json()
        self.assertIn('status', responseData)
        self.assertEqual(responseData['status'], 'OK')  

    def test_user_authentication_flows(self):
        """Test user authentication flows."""
        failed_login_response = self.client.post('/auth/login',
                                    json={'username': 'invalidUser', 'password': 'invalidPass'})
        self.assertNotEqual(failed_login_response.status_code, 200)
        self.assertEqual(failed_login_response.content_type, "application/json")
        errorData = failed_login_response.get_json()
        self.assertIn('error', errorAlexa)

        success_login_response = self.client.post('/auth/login',
                                    json={'username': 'validUser', 'password': 'validPass'})
        self.assertEqual(success_login_response.status_code, 200)
        self.assertEqual(success_login_response.content_type, "application/json")
        successData = success_login_response.get_json()
        self.assertIn('token', successData)

    def test_code_snippet_creation(self):
        """Test code snippet creation."""
        create_code_response = self.client.post('/code_snippets',
                                    json={'code': 'print("Hello, World!")', 'language': 'Python'},
                                    headers={'Authorization': f'Bearer {self.demo_user_token}'})
        self.assertEqual(create_code_response.status_code, 201)
        self.assertEqual(create_code_response.content_type, "application/json")
        creationData = create_code_response.get_json()
        self.assertIn('id', creationData)  

    def test_external_service_integration(self):
        """Test external service integration by checking response status and content type."""
        external_service_response = self.client.get('/external_service_logo', headers={'Authorization': f'Bearer {self.demo_user_token}'})
        self.assertEqual(external_service_response.status_code, 200)
        self.assertEqual(external_service_response.content_type, "image/png")

if __name__ == '__main__':
    unittest.main()