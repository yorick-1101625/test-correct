import json

def convert_to_json(exported_questions):
    json = []
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
        json.append(question_dict)
    print(json)