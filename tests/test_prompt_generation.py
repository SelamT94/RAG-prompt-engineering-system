import unittest
import sys , os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.prompt_generator import generate_prompt

class TestPromptGenerator(unittest.TestCase):

    def test_generate_prompt(self):
        user_input = "Test user input"
        scenarios = "Test scenarios"
        prompts = generate_prompt(user_input, scenarios)
        self.assertTrue(len(prompts) > 0)

if __name__ == '__main__':
    unittest.main()
