from flask import Flask, render_template, request, redirect, send_file, session, url_for, flash
from flask_session import Session

from lib.model.users import Users, hash_password
from lib.model.questions import Questions
from lib.model.prompts import Prompts
from lib.database.load_json import Json

from lib.gpt.bloom_taxonomy import get_bloom_category

import json
from lib.database.export_json import convert_to_json


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_request
def check_login():
    open_routes = ['login', 'static']

    admin_routes = ['admin_config', 'create_user', 'edit_user']
    logged_in = session.get('user_id')
    user_model = Users()
    is_admin = user_model.admin_check(logged_in)

    if logged_in is None and request.endpoint not in open_routes:
        return redirect(url_for('login'))

    if logged_in is not None:
        if request.endpoint in admin_routes and not is_admin:
            return redirect(url_for('home'))

@app.route('/')
def home():
    # If not logged in:
    if not session.get("user_id"):
        return redirect('/login')
    else:
        return redirect('/overview/0')


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
    if list(filter(lambda x: x is not None, arguments)):
        questions = questions_model.show_filtered_questions(str(subject), str(indexed_filter), offset, str(search_term))
        arguments_url = f"?search-term={search_term}&subject={subject}&indexed={indexed_filter}"
    # Return standard results
    else:
        questions = questions_model.show_ten_not_indexed_questions(offset=offset)
        arguments_url = ""

    return render_template('overview.html.jinja', questions=questions, offset=offset, arguments_url=arguments_url)


@app.route('/export', methods=['GET', 'POST'])
def export():
    questions_model = Questions()
    exported_questions = questions_model.get_indexed_questions()

    if request.method == "POST":
        # Set questions as exported in database
        for question in exported_questions:
            questions_model.set_exported(question['questions_id'])
        return send_file("lib/json/exported-questions.json", as_attachment=True)
    else:
        # Export questions to json
        convert_to_json(exported_questions)
        return render_template("export.html.jinja", exported_questions=exported_questions)


@app.route('/prompt/overview')
def prompt_overview():
    prompts_model = Prompts()
    prompts_info = prompts_model.prompts_info()
    return render_template('prompt-overview.html.jinja', prompts_info=prompts_info)


@app.route('/prompt/create', methods=['GET', 'POST'])
def prompt_create():
    if request.method == 'POST':
        prompt_name = request.form.get("prompt_name")
        prompt = request.form.get("prompt")
        prompts_model = Prompts()
        user_id = session.get('user_id')
        prompt_category = request.form.get("prompt_category")
        created_prompt = prompts_model.create_prompt(prompt_name, prompt, user_id, prompt_category)

        if created_prompt:
            flash('Prompt succesvol aangemaakt!', 'succes')
            return redirect('/prompt/overview')
    else:
        return render_template('prompt-create.html.jinja')


@app.route('/prompt/<prompts_id>', methods=['GET', 'POST'])
def prompt_details(prompts_id):
    prompts_model = Prompts()
    prompt = prompts_model.show_single_prompt(prompts_id)
    prompt_info = prompts_model.show_single_prompt_info(prompts_id)
    if request.method == 'POST':
        is_deleted = prompts_model.delete_prompt(prompts_id)
        if is_deleted:
            flash('Prompt succesvol verwijderd!', 'succes')
            return redirect('/prompt/overview')
    else:
        return render_template('prompt-details.html.jinja',prompt=prompt, prompt_info=prompt_info,
                               username=session['name'], admin=session['admin'])

@app.route('/prompt/edit/<prompts_id>', methods=['GET', 'POST'])
def prompt_edit(prompts_id):
    prompts_model = Prompts()
    prompt = prompts_model.show_single_prompt(prompts_id)
    if request.method == 'POST':
        prompt_name = request.form.get("prompt_name")
        prompt = request.form.get("prompt")
        prompts_model = Prompts()
        user_id = session.get('user_id')
        prompt_category = request.form.get("prompt_category")
        created_prompt = prompts_model.create_prompt(prompt_name, prompt, user_id, prompt_category)
        if created_prompt:
            flash('Prompt succesvol aangemaakt!', 'succes')
            return redirect('/prompt/overview')
    else:
        return render_template('prompt-edit.html.jinja', prompt=prompt)



@app.route('/<taxonomy>/<questions_id>')
def single_question_page(taxonomy, questions_id):
    # Show question
    questions_model = Questions()
    single_question = questions_model.show_single_question(questions_id)
    # Show all prompts
    prompts_model = Prompts()
    prompts = prompts_model.show_prompts_per_category(taxonomy)
    return render_template('single-question.html.jinja', single_question=single_question, prompts=prompts, taxonomy=taxonomy)


@app.route('/<taxonomy>/<questions_id>/antwoord', methods=['GET', 'POST'])
def prompt_answer(taxonomy, questions_id):
    prompts_id = request.form.get('prompt')
    prompt_model = Prompts()
    prompt = prompt_model.show_single_prompt(prompts_id)['prompt']

    questions_model = Questions()
    single_question = questions_model.show_single_question(questions_id)
    question = single_question['question']

    # Add JSON structure directions to prompt
    structured_prompt = prompt
    if taxonomy == 'bloom':
        structured_prompt = prompt_model.structure_bloom_prompt(prompt)
    elif taxonomy == 'rtti':
        structured_prompt = prompt_model.structure_rtti_prompt(prompt)

    gpt_response = get_bloom_category(question, structured_prompt, 'rac_test')

    # Try 3 times to get a valid answer
    is_valid = False
    for i in range(3):
        try:
            valid_answers = ["onthouden", "begrijpen", "toepassen", "analyseren", "evalueren", "creëren", "r", "t1", "t2", "i"]
            for ans in valid_answers:
                if gpt_response['categorie'].lower() == ans:
                    is_valid = True
                    break
        except:
            pass

        if not is_valid:
            gpt_response = get_bloom_category(question, structured_prompt, 'rac_test')

    return render_template('prompt-answer.html.jinja', single_question=single_question, gpt_response=gpt_response, prompts_id=prompts_id, is_valid=is_valid, taxonomy=taxonomy)

@app.route('/<taxonomy>/<questions_id>/save/prompt=<prompts_id>', methods=['POST'])
def save_answer(taxonomy, questions_id, prompts_id):
    prompt_model = Prompts()
    questions_model = Questions()

    # Get info from webpage
    taxonomy_input = request.form.get('taxonomy')
    user_id = session.get('user_id')

    # Check if the answer was change by user or not
    changed_by_user = True
    if taxonomy_input[:3] == 'gpt':
        changed_by_user = False
        taxonomy_input = taxonomy_input[4:]

    # Save taxonomy in DB
    is_prompt_updated = prompt_model.update_prompt_stats(prompts_id, changed_by_user)
    is_question_updated = questions_model.update_question_stats(questions_id, prompts_id, taxonomy_input, user_id, taxonomy)
    flash('Taxonomie succesvol opgeslagen!','succes')

    # Redirect to next question
    if is_prompt_updated and is_question_updated:
        next_question = None
        # Should redirect to next question
        if taxonomy == 'bloom':
            next_question = questions_model.show_first_not_indexed_question('bloom')
        elif taxonomy == 'rtti':
            next_question = questions_model.show_first_not_indexed_question('rtti')

        next_question_url = f"/{taxonomy}/{next_question['questions_id']}"
        return redirect(next_question_url)


@app.route('/admin/configuration')
def admin_config():
    users_model = Users()
    users = users_model.show_users()
    active_user = users_model.show_single_user(session.get('user_id'))
    return render_template('admin-configuration.html.jinja', users=users, active_user=active_user)

@app.route('/admin/create-user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        user_model = Users()
        display_name = request.form.get('display_name')
        login = request.form.get('login').lower()
        password = request.form.get('password')
        is_admin = request.form.get('admin')
        try:
            if is_admin[0] == '1':
                is_admin = 1
            else:
                is_admin = 0
        except:
            is_admin = 0

        created_user = user_model.create_users(display_name, login, password, is_admin)
        if created_user:
            flash('Gebruiker succesvol aangemaakt!', 'succes')
            return redirect('configuration')
    else:
        return render_template('create-user.html.jinja')

@app.route('/admin/edit-user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user_model = Users()
    user_info = user_model.show_single_user(user_id)

    if request.method == 'POST':
        if request.form['submit'] == 'Opslaan':
            display_name = request.form.get('display_name')
            login = request.form.get('login').lower()
            password = request.form.get('password')
            is_admin = request.form.get('admin')
            try:
                if is_admin == '1':
                    is_admin = 1
                else:
                    is_admin = 0
            except:
                is_admin = 0

            edited_user = user_model.edit_users(
                display_name=display_name, login=login, password=password, user_id=user_id, is_admin=is_admin)
            if edited_user:
                if str(user_id) == str(session.get('user_id')):
                    session['name'] = display_name
                    session['admin'] = is_admin
                    flash('Gegevens succesvol veranderd!', 'succes')
                else:
                    flash('Gebruiker succesvol aangepast!', 'succes')
                return redirect('/admin/configuration')
        if request.form['submit'] == 'Verwijderen':
            deleted_user = user_model.delete_users(
                user_id=user_id)
            if deleted_user:
                if str(user_id) == str(session.get('user_id')):
                    session['name'] = None
                    session['admin'] = None
                    session['user_id'] = None
                flash('Gebruiker succesvol verwijderd!', 'succes')
                return redirect('/admin/configuration')
    else:
        return render_template('edit-user.html.jinja', display_name=user_info['display_name'], login=user_info['login'], is_admin=user_info['is_admin'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')
        users_model = Users()
        user = users_model.log_in(email, password)
        if user:
            session['user_id'] = user['user_id']
            session['name'] = user['display_name']
            session['admin'] = user['is_admin']
            flash('U bent succesvol ingelogd!', 'succes')
            return redirect('/overview/0')  # Redirect to a success page

        else:
            flash('Verkeerde inlog-gegevens, probeer het opnieuw.', 'error')
            return redirect('/login')
    else:
        return render_template('log-in.html')


@app.route('/logout', methods=[ 'GET','POST'])
def logout():
    session['user_id'] = None
    session['name'] = None
    session['admin'] = None
    flash('U bent uitgelogd.', 'succes')
    return redirect('/')


@app.route('/upload', methods=['GET', 'POST'])
def json_upload():
    if request.method == 'POST':
        file = request.files['json_file']
        json_model = Json()
        json_uploaded = json_model.open_file(file)
        if json_uploaded:
            flash('JSON bestand is succesvol geüpload!', 'succes')
            return redirect('/')
    else:
        return render_template('upload-json.html')


@app.errorhandler(404)
def not_found(error):
    return f"<h2>{error}</h2>"


if __name__ == "__main__":
    app.run(debug=False)
