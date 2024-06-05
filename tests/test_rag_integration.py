import unittest
from src.rag_integration.retriever import fetch_similar_prompts

class TestRAGIntegration(unittest.TestCase):
    def test_fetch_similar_prompts(self):
        query = "example query"
        similar_prompts = fetch_similar_prompts(query)
        self.assertIsInstance(similar_prompts, list)

if __name__ == '__main__':
    unittest.main()
