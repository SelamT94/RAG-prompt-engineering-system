import random

def generate_test_cases(description, scenarios):
    test_cases = []
    for scenario in scenarios:
        test_case = {
            "description": description,
            "scenario": scenario,
            "input": f"{description} in the context of {scenario}",
            "expected_output": f"Expected outcome for {scenario}"
        }
        test_cases.append(test_case)
    return test_cases
