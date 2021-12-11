from flask import Blueprint, current_app, render_template, request
from sql import work_with_db
from sql_provider import SQLProvider
from access import login_permission_required

provider = SQLProvider("sql/")
request_app = Blueprint('requests', __name__, template_folder='templates')


@request_app.route('/')
@login_permission_required
def menu():
    return render_template('requests_menu.html')


@request_app.route('/books', methods=['GET', 'POST'])
def book_list():
    schema = ['Passenger_Name', 'Date_of_sale', 'Departure_airport', 'Arrival_airport', 'Departure_Time_And_Date', 'Cost']
    context = {
        'tickets':[]
    }
    if request.method == 'POST':
        date = request.form.get('date', None)
        _SQL = provider.get("sold_that_day.sql", date=date)
        table = work_with_db(current_app.config['DB_CONFIG'], _SQL, schema)
        for elem in table:
            context['tickets'].append(elem)
    return render_template('book_list.html', **context)


@request_app.route('/orders', methods=['GET', 'POST'])
def order_list():
    schema = ['Passenger_Name', 'Date_of_sale', 'Departure_airport', 'Arrival_airport', 'Departure_Time_And_Date', 'Cost']
    context = {
        'orders': []
    }
    if request.method == 'POST':
        name = request.form.get('name', None)
        try:
            _SQL = provider.get("get_tickets.sql", Passenger_Name=name)
            table = work_with_db(current_app.config['DB_CONFIG'], _SQL, schema)
        except:
            return "Wrong input"
        for elem in table:
            context['orders'].append(elem)
    return render_template('order_list.html', **context)