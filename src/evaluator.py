import random
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def evaluate_prompt(generated_prompt, user_input):
    embeddings1 = model.encode(generated_prompt, convert_to_tensor=True)
    embeddings2 = model.encode(user_input, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
    return cosine_scores.item()

def evaluate_prompts(prompts, user_input):
    evaluations = {prompt: evaluate_prompt(prompt, user_input) for prompt in prompts}
    return sorted(evaluations.items(), key=lambda item: item[1], reverse=True)

def evaluate_prompt(prompt, test_cases):
    scores = []
    for test_case in test_cases:
        # Simulate prompt performance, e.g., matching expected output
        score = random.uniform(0, 1)  # Placeholder for actual evaluation logic
        scores.append(score)
    return scores

def compute_metrics(scores):
    average_score = sum(scores) / len(scores)
    return {"average_score": average_score}
