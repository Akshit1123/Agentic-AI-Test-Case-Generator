import pandas as pd
from agents.test_lead_agent import review_data_dictionary

# Load and stringify your CSV data dictionary
df = pd.read_csv(r"C:\Users\850081683\OneDrive - Genpact\Desktop\Intern\work\Regression Test Case Generation\testgen-agentic\data\data_dictionary.csv")
data_dict_text = df.to_string(index=False)

# Call the review function with correct structure
result = review_data_dictionary({
    "data_dictionary": data_dict_text,
    "messages": []
})

print(result["messages"][-1].content)
