from flask import session


def add_to_basket(item):
    basket = session.get('basket', [])
    bought = session.get('bought', [])
    if item['id'] not in bought:
        basket.append(item)
        bought.append(item['id'])
    session['basket'] = basket
    session['bought'] = bought
