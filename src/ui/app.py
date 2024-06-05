from flask import Flask, render_template, request
from src.prompt_generation.generator import generate_prompts
from src.evaluation.metrics import evaluate_prompt

def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            description = request.form['description']
            scenarios = request.form.getlist('scenarios')
            prompts = generate_prompts(description, scenarios)
            # Evaluate and rank prompts here
            evaluations = [evaluate_prompt(prompt, []) for prompt in prompts]
            return render_template('index.html', prompts=prompts, evaluations=evaluations)
        return render_template('index.html')

    return app
