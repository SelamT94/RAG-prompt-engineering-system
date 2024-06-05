import unittest
from src.evaluation.metrics import evaluate_prompt

class TestEvaluation(unittest.TestCase):
    def test_evaluate_prompt(self):
        prompt = "Test prompt"
        test_cases = ["Test case 1", "Test case 2"]
        score = evaluate_prompt(prompt, test_cases)
        self.assertIsInstance(score, float)

if __name__ == '__main__':
    unittest.main()
