# import requests

# def fetch_prompts():
#     url = "https://api.github.com/repos/danielmiessler/fabric/contents/patterns"
#     headers = {"Accept": "application/vnd.github.v3+json"}
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     return response.json()

# def get_prompts():
#     prompt_data = fetch_prompts()
#     base_prompts = [item['name'] for item in prompt_data if item['type'] == 'file' and item['name'].endswith('.md')]
#     return base_prompts
import requests

def fetch_prompts():
    url = "https://api.github.com/repos/danielmiessler/fabric/contents/patterns"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_prompts():
    prompt_data = fetch_prompts()
    base_prompts = []
    for item in prompt_data:
        if item['type'] == 'file' and item['name'].endswith('.md'):
            file_url = item['download_url']
            file_content = requests.get(file_url).text
            base_prompts.append(file_content)
    return base_prompts
