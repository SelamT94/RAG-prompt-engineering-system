import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.prompt_generator import generate_prompt
from src.evaluator import evaluate_prompts

def main():
    user_input = "Explain the impact of climate change on marine life."
    scenarios = "1. Rising sea temperatures\n2. Ocean acidification\n3. Coral bleaching"
    
    generated_prompts = generate_prompt(user_input, scenarios)
    evaluations = evaluate_prompts(generated_prompts, user_input)
    
    for prompt, score in evaluations:
        print(f"Prompt: {prompt}\nScore: {score}\n")

if __name__ == "__main__":
    main()
