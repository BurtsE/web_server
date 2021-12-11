from flask import Blueprint, render_template, session, request, current_app
from access import login_permission_required
from sql import work_with_db
from sql_provider import SQLProvider


auth_app = Blueprint('auth', __name__, template_folder='templates')

provider = SQLProvider("sql/")


@auth_app.route('/',  methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('auth.html')
    else:
        schema = ['role']
        context = {}
        login = request.form.get('login', None)
        password = request.form.get('password', None)
        if login and password:
            _SQL = provider.get("get_user.sql", login=login, password=password)
            print(_SQL)
            table = work_with_db(current_app.config['DB_CONFIG'], _SQL, schema)
            if table:
                context['login'] = table[0]['role']
                session['group_name'] = table[0]['role']
                session['login'] = login
        return render_template('return.html', **context)
