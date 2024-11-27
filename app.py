from flask import Flask, render_template, request

from lib.model.users import Users
from lib.model.questions import Questions
from lib.model.prompts import Prompts

from lib.gpt.bloom_taxonomy import get_bloom_category

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('log-in.html')

@app.route('/overview/<offset>', methods=['GET', 'POST'])
def overview(offset):
    questions_model = Questions()
    offset = int(offset)
    # Search Arguments
    search_term = request.args.get('search-term')
    subject = request.args.get('subject')
    indexed_filter = request.args.get('indexed')
    arguments = (search_term, subject, indexed_filter)

    # Check if there are arguments
    # & Return the filtered results
    if list(filter(lambda x: x != None, arguments)):
        questions = questions_model.show_filtered_questions(str(subject), str(indexed_filter), offset, str(search_term))
        arguments_url = f"?search-term={search_term}&subject={subject}&indexed={indexed_filter}"
    # Return standard results
    else:
        questions = questions_model.show_ten_questions(offset=offset)
        arguments_url = ""

    return render_template('overview.html', questions=questions, offset=offset, arguments_url=arguments_url)

@app.route('/vraag/<questions_id>', methods=['GET'])
def single_question_page(questions_id):
    # Show question
    questions_model = Questions()
    single_question = questions_model.show_single_question(questions_id)
    # Show all prompts
    prompts_model = Prompts()
    prompts = prompts_model.show_prompts()
    # Check if question exists
    if single_question is None:
        return "<h1>404: Question does not exist</h1>"
    else:
        return render_template('single-question.html', single_question=single_question, prompts=prompts)

@app.route('/vraag/<questions_id>/antwoord', methods=['GET', 'POST'])
def prompt_answer(questions_id):
    prompts_id = request.form.get('prompt')
    prompt_model = Prompts()
    prompt = prompt_model.show_single_prompt(prompts_id)['prompt']

    questions_model = Questions()
    question = questions_model.show_single_question(questions_id)['question']

    get_bloom_category(question, prompt, 'rac_test')

    return render_template('prompt-answer.html')


@app.route('/login')
def login():
    users_model = Users()
    user_info = users_model.log_in()
    print(user_info)
    return render_template('log-in.html')

if __name__ == "__main__":
    app.run(debug=True)