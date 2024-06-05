import unittest
from src.prompt_generation.generator import generate_prompts

class TestPromptGeneration(unittest.TestCase):
    def test_generate_prompts(self):
        description = "Test description"
        scenarios = ["Scenario 1", "Scenario 2"]
        prompts = generate_prompts(description, scenarios)
        self.assertEqual(len(prompts), 2)
        self.assertIn("Scenario: Scenario 1", prompts[0])
        self.assertIn("Scenario: Scenario 2", prompts[1])

if __name__ == '__main__':
    unittest.main()
