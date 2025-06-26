# test_tester_agent.py

import pandas as pd
from agents.tester_agent import generate_test_cases

# Load sample field from data dictionary
df = pd.read_csv(r"C:\Users\850081683\OneDrive - Genpact\Desktop\Intern\work\Regression Test Case Generation\testgen-agentic\data\data_dictionary.csv")
sample_field = df.iloc[0].to_dict()  # just testing the first field

# Generate test cases
prompt, test_cases = generate_test_cases(sample_field)


print("\n=== Test Cases Generated ===\n")
print(test_cases)
