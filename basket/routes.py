from flask import Blueprint, render_template, request, current_app, redirect, session, url_for
from sql import work_with_db, make_update
from sql_provider import SQLProvider
from basket.utils import add_to_basket
from access import login_permission_required
from datetime import datetime, date

basket_app = Blueprint('basket', __name__, template_folder='templates')
provider = SQLProvider("sql/")


@basket_app.route('/')
@login_permission_required
def index():
    session['tickets'] = []
    return render_template('search.html')


@basket_app.route('/main', methods=['GET', 'POST'])
def process():
    print(session.get('tickets'))
    schema = ['id', 'dep', 'arr', 'date', 'price']
    current_basket = session.get('basket', [])
    tickets = session.get('tickets', [])
    if request.method == 'GET' and tickets == []:
        params = request.url.split('?')[1].split('&')
        departure = params[0].split('=')[1]
        destiny = params[1].split('=')[1]
        dep_date = params[2].split('=')[1]
        sql = provider.get('edit_item.sql', departure=departure, destiny=destiny, date=dep_date)
        session['tickets'] = work_with_db(current_app.config['DB_CONFIG'], sql, schema)
        return redirect('/basket/main')
    elif request.method == 'GET':
        return render_template('index.html', items=tickets, basket=current_basket)
    else:
        item_id = request.form.get('item_id', None)
        _SQL = provider.get("order_item.sql", item_id=item_id)
        items = work_with_db(current_app.config['DB_CONFIG'], _SQL, schema)
        if items:
            add_to_basket(items[0])
        return redirect('/basket/main')



# @basket_app.route('/insert',  methods=['GET', 'POST'])
# def insert_item():
#     # schema = ['id', 'name', 'auth', 'num', 'date', 'price']
#     if request.method == 'GET':
#         return render_template('insert_item.html')
#     else:
#         item_name = request.form.get('name')
#         author = request.form.get('author')
#         num = request.form.get('num')
#         date = request.form.get('date')
#         cost = request.form.get('cost')
#         _SQL = provider.get('insert_item.sql', item_name=item_name, author=author, num=num, date=date, cost=cost)
#         response = make_update(current_app.config['DB_CONFIG'], _SQL)
#         print(response)
#         return redirect('/basket')


@basket_app.route('/clear')
def clear_basket():
    session['basket'] = []
    session['bought'] = []
    return redirect(url_for('basket.process'))


@basket_app.route('/buy', methods=['GET', 'POST'])
def buy_items():
    for item in session['basket']:
        sql = provider.get('get_cashier.sql', login=session['login'])
        cashier = work_with_db(current_app.config['DB_CONFIG'], sql, ['cashier'])[0]['cashier']
        passenger = request.form.get('name')
        _SQL = provider.get('insert_item.sql',
                            passenger=passenger,
                            date=datetime.today().strftime('%Y-%m-%d-%H:%M:%S'),
                            cashier=cashier,
                            idT=item['id'])
        make_update(current_app.config['DB_CONFIG'], _SQL)
    return redirect('/basket/clear')
