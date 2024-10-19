# Template for evaluation prompt
EVAL_PROMPT = """
Expected Response: {}
Actual Response: {}
###
(Answer with 'True' or 'False: Does the actual response match the expected response?)
"""

# Strip leading/trailing whitespaces and convert to lowercase
retrieval_test_response = evaluation_results_str.strip().lower()

# Check if "true" or "false" is present in the response
if "true" in retrieval_test_response:
  return True
elif "false" in retrieval_test_response:
  return False
else:
  # Raise an error if neither "true" nor "false" is found
  raise ValueError("Did not return true or false")

  def test_retrieval_response():
  # Test function to validate retrieval response
  assert query_and_validate(
    prompt="a question about our data",
    expected_response="a known fact in our data"
  )
