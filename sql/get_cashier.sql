select idCashier
from cashier join user on (clogin=login)
where login = "$login"
