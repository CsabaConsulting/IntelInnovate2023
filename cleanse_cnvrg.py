import json
from pathlib import Path

# Define the input and output paths
input_filepath = Path('./data/cnvrg_docs.json')
output_filepath = Path('./data/cnvrg_cleansed.json')

cnvrg_clean = dict(messages=[])
# Expecting the JSON with an array of { source, question, answer } pair tuples.
with open(input_filepath, 'r') as input_file:
    input_json = json.load(input_file)
    cnvrg = input_json["messages"]

    for qa in cnvrg:
        q = qa["content"].strip()
        a = qa["response"].strip()
        if not q or not a:
            continue
        # Is it upside down? 431 out of 464 non empty was
        if (a.startswith("How ") or a.startswith("What ") or a.startswith("Who ") or a.startswith("Can ") or a.startswith("Where ") or a.startswith("Are ")) and not (
            q.startswith("How ") or q.startswith("What ") or q.startswith("Who ") or q.startswith("Can ") or q.startswith("Where ") or q.startswith("Are ")
        ):
            q, a = a, q
        
        cnvrg_clean["messages"].append(dict(role="user", content=q, response=a))

    with open(output_filepath, 'w') as output_file:
        json.dump(cnvrg_clean, output_file, indent=2)
        print(f"Results have been saved to {output_filepath}.")
