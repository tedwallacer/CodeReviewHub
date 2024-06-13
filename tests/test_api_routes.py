import os
import json
import unittest
from your_flask_app import create_app
from flask import url_for

class FlaskAppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()
        self.demo_user_token = os.getenv('DEMO_USER_TOKEN')

    def tearDown(self):
        pass

    def test_health_endpoint_response(self):
        response = self.client.get('/health_check')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        responseData = json.loads(response.data)
        self.assertIn('status', responseData)
        self.assertEqual(responseData['status'], 'OK')  

    def test_user_authentication_flows(self):
        failed_login_response = self.client.post('/auth/login',
                                    data=json.dumps({'username': 'invalidUser', 'password': 'invalidPass'}),
                                    content_type='application/json')
        self.assertNotEqual(failed_login_response.status_code, 200)
        self.assertEqual(failed_login_response.content_type, "application/json")
        errorData = json.loads(failed_login_response.data)
        self.assertIn('error', errorData)

        success_login_response = self.client.post('/auth/login',
                                    data=json.dumps({'username': 'validUser', 'password': 'validPass'}),
                                    content_type='application/json')
        self.assertEqual(success_login_response.status_code, 200)
        self.assertEqual(success_login_response.content_type, "application/json")
        successData = json.loads(success_login_response.data)
        self.assertIn('token', successData)

    def test_code_snippet_creation(self):
        create_code_response = self.client.post('/code_snippets',
                                    data=json.dumps({'code': 'print("Hello, World!")', 'language': 'Python'}),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.demo_user_token}'})
        self.assertEqual(create_code_response.status_code, 201)
        self.assertEqual(create_code_response.content_type, "application/json")
        creationData = json.new(load(create_code_response.data)
        self.assertIn('id', creationData)  

    def test_external_service_integration(self):
        external_service_response = self.client.get('/external_service_logo', headers={'Authorization': f'Bearer {self.demo_user_token}'})
        self.assertEqual(external_service_response.status_code, 200)
        self.assertEqual(external_service_response.content_type, "image/png")

if __name__ == '__main__':
    unittest.main()