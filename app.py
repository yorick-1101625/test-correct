from flask import Flask, render_template, request, redirect

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

    return render_template('overview.html.jinja', questions=questions, offset=offset, arguments_url=arguments_url)


@app.route('/prompt/overview')
def prompt_overview():
    prompt_nr = 0
    prompts_model = Prompts()
    prompts = prompts_model.show_prompts()
    return render_template('prompt-overview.html', prompts=prompts)


@app.route('/prompt/create', methods=['GET', 'POST'])
def prompt_create():
    if request.method == 'POST':
        prompt_name = request.form.get("prompt_name")
        prompt = request.form.get("prompt")
        prompts_model = Prompts()
        created_prompt = prompts_model.create_prompt(prompt_name, prompt)

        if created_prompt:
            return redirect('/prompt/overview')
    else:
        return render_template('prompt-create.html')


@app.route('/prompt/<prompts_id>')
def prompt_details(prompts_id):
    prompts_model = Prompts()
    prompt = prompts_model.show_single_prompt(prompts_id)
    user = 'Kees'
    return render_template('prompt-details.html', prompt=prompt, user=user)


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
        return render_template('single-question.html.jinja', single_question=single_question, prompts=prompts)


@app.route('/vraag/<questions_id>/antwoord', methods=['GET', 'POST'])
def prompt_answer(questions_id):
    prompts_id = request.form.get('prompt')
    prompt_model = Prompts()
    prompt = prompt_model.show_single_prompt(prompts_id)['prompt']

    questions_model = Questions()
    single_question = questions_model.show_single_question(questions_id)
    question = single_question['question']

    gpt_response = get_bloom_category(question, prompt, 'dry_run')

    return render_template('prompt-answer.html.jinja', single_question=single_question, gpt_response=gpt_response)

@app.route('/admin/configuration')
def admin_config():
    users_model = Users()
    users = users_model.show_users()
    return render_template('admin-configuration.html', users=users)

@app.route('/admin/create-user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        display_name = request.form.get('display_name')
        login = request.form.get('login')
        password = request.form.get('password')
        user_model = Users()
        created_user = user_model.create_users(display_name, login, password)
        if created_user:
            return redirect('configuration')
    else:
        return render_template('create-user.html')

@app.route('/admin/edit-user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user_model = Users()
    user_info = user_model.show_single_user(user_id)
    if request.method == 'POST':
        if request.form['submit'] == 'Opslaan':
            display_name = request.form.get('display_name')
            login = request.form.get('login')
            password = request.form.get('password')
            is_admin = request.form.get('admin')
            try:
                if is_admin[0] == '1':
                    is_admin = 1
                else:
                    is_admin = 0
            except:
                is_admin = 0
            edited_user = user_model.edit_users(
                display_name=display_name, login=login, password=password, user_id=user_id, is_admin=is_admin)
            if edited_user:
                return redirect('/admin/configuration')
        if request.form['submit'] == 'Verwijderen':
            deleted_user = user_model.delete_users(
                user_id=user_id)
            if deleted_user:
                return redirect('/admin/configuration')
    else:
        return render_template('edit-user.html', display_name=user_info[3], login=user_info[1], password=user_info[2], is_admin=user_info[5])


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    users_model = Users()
    is_logged_in = users_model.log_in(username, password)

    if is_logged_in:
        return redirect('/overview/0')  # Redirect to a success page
    else:
        error = "Invalid username or password"
        return render_template('log-in.html', error=error)




if __name__ == "__main__":
    app.run(debug=True)
