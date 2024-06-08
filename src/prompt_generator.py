# import os
# import openai
# from sentence_transformers import SentenceTransformer, util
# from src.fetch_prompts import get_prompts

# openai.api_key = os.getenv('OPENAI_API_KEY')
# model = SentenceTransformer('all-MiniLM-L6-v2')

# def get_similar_prompts(user_input, base_prompts):
#     user_embedding = model.encode(user_input, convert_to_tensor=True)
#     prompt_embeddings = model.encode(base_prompts, convert_to_tensor=True)
#     cosine_scores = util.pytorch_cos_sim(user_embedding, prompt_embeddings)
#     similar_prompts = [(score.item(), prompt) for score, prompt in zip(cosine_scores[0], base_prompts)]
#     similar_prompts = sorted(similar_prompts, key=lambda x: x[0], reverse=True)
#     return [prompt for _, prompt in similar_prompts[:5]]  # Return top 5 similar prompts

# def generate_prompt(user_input, scenarios):
#     base_prompts = get_prompts()
#     similar_prompts = get_similar_prompts(user_input, base_prompts)
#     generated_prompts = []
#     for prompt in similar_prompts:
#         response = openai.Completion.create(
#             engine="davinci",
#             prompt=f"{prompt}\nUser input: {user_input}\nScenarios: {scenarios}",
#             max_tokens=150
#         )
#         generated_prompts.append(response.choices[0].text.strip())
#     return generated_prompts

from sentence_transformers import SentenceTransformer, util
from src.fetch_prompts import get_prompts
from src.test_case_generator import generate_test_cases
from src.evaluator import evaluate_prompt, compute_metrics

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_similar_prompts(user_input, base_prompts):
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    prompt_embeddings = model.encode(base_prompts, convert_to_tensor=True)
    
    print(f"User embedding shape: {user_embedding.shape}")
    print(f"Prompt embeddings shape: {prompt_embeddings.shape}")
    
    if prompt_embeddings.shape[0] == 0:
        raise ValueError("No valid prompt embeddings found.")
    
    cosine_scores = util.pytorch_cos_sim(user_embedding, prompt_embeddings)
    return cosine_scores

def generate_prompt(user_input, scenarios):
    base_prompts = get_prompts()
    print(f"Base prompts: {base_prompts}")
    
    similar_prompts = get_similar_prompts(user_input, base_prompts)
    sorted_prompts = sorted(zip(base_prompts, similar_prompts[0].tolist()), key=lambda x: x[1], reverse=True)
    return [prompt for prompt, score in sorted_prompts]

def main():
    user_input = input("Enter a description of your objective or task: ")
    scenarios = input("Enter a few scenarios (comma separated): ").split(',')

    generated_prompts = generate_prompt(user_input, scenarios)
    for idx, prompt in enumerate(generated_prompts):
        print(f"Prompt {idx + 1}: {prompt}")

    # Generate test cases
    test_cases = generate_test_cases(user_input, scenarios)
    print("Generated Test Cases:")
    for test_case in test_cases:
        print(test_case)

    # Evaluate prompts
    for prompt in generated_prompts:
        scores = evaluate_prompt(prompt, test_cases)
        metrics = compute_metrics(scores)
        print(f"Evaluation Metrics for Prompt: {prompt}")
        print(metrics)

if __name__ == "__main__":
    main()
