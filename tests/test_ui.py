import unittest
from flask_testing import TestCase
from src.ui.app import create_app

class TestUI(TestCase):
    def create_app(self):
        return create_app()

    def test_index(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assertTemplateUsed('index.html')

    def test_generate_prompts(self):
        response = self.client.post('/', data={
            'description': 'Test description',
            'scenarios': ['Scenario 1', 'Scenario 2']
        })
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertIn(b'Test description - Scenario: Scenario 1', response.data)

if __name__ == '__main__':
    unittest.main()
