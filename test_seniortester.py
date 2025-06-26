from agents.senior_tester_agent import senior_tester_agent
from langchain_core.messages import HumanMessage

# Sample field definitions (simulating contents from your data_dictionary.csv)
sample_data_dictionary = """
Field Name: Drug_ID
Data Type: Integer
Required: Yes
Format: N/A
Valid Values: 1000-9999

Field Name: Drug_Name
Data Type: String
Required: Yes
Format: Alphanumeric
Valid Values: N/A
"""

# Sample test cases for critique (simulating a previously generated RTC)
sample_test_cases = """
**Test Case ID:** TC_DrugID_001
**Title:** Valid Drug ID
**Description:** Check if application accepts valid Drug ID
**Input:** 1234
**Expected Result:** Accepted and stored successfully

**Test Case ID:** TC_DrugID_002
**Title:** Drug ID too short
**Description:** Input below valid range
**Input:** 999
**Expected Result:** Error - value below valid range

**Test Case ID:** TC_DrugName_001
**Title:** Empty Drug Name
**Description:** Test with blank string
**Input:** ""
**Expected Result:** Error - field is required
"""

# Create state to simulate agent input
state = {
    "data_dictionary": sample_data_dictionary,
    "test_cases": sample_test_cases,
    "messages": []
}


# Run the critique logic
output = senior_tester_agent.invoke(state)
print(output["messages"][-1].content)
