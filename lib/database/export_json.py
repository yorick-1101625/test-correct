import json


def convert_to_json(exported_questions):
    questions_list = []
    # Format the questions in a dictionary
    for questions in exported_questions:
        question_id = questions['questions_id']
        question = questions['question']
        taxonomy_bloom = questions['taxonomy_bloom']
        rtti = questions['rtti']

        question_dict = {
            "question_id": question_id,
            "question": question,
            "taxonomie": taxonomy_bloom,
            "rtti": rtti
        }
        # Adding all the questions in a list
        questions_list.append(question_dict)

    write_to_json(questions_list)


def write_to_json(questions_list):
    # Convert the list to a json object
    json_object = json.dumps(questions_list, indent=4)

    # Write the json object to a json file
    with open("lib/json/exported-questions.json", "w") as outfile:
        outfile.write(json_object)