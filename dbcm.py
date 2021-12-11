from pymysql import connect
from pymysql.err import InterfaceError, OperationalError


class UseDatabase:
    def __init__(self, config: dict):
        self.config = config
    def __enter__(self):
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except InterfaceError as err:
            return err
        except OperationalError as err:
            if err.args[0] == 1049:
                print("Нет такой базы данных!")
            if err.args[0] == 1045:
                print("Неверный логин/пароль!")
            if err.args[0] == 2003:
                print("Нет такого сервера!")
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
            self.conn.close()
            self.cursor.close()
            return True
        if exc_val is not None:
            if exc_val.args[0] == 'Cursor is None':
                return True
            if exc_val.args[0] == 1064:
                print('Синтаксическая ошибка в SQL запросе')
                return True
            if exc_val.args[0] == 1146:
                print('Нет такой таблицы в БД')
                return True
            if exc_val.args[0] == 1054:
                print('Нет нужных строк в таблице')
                return True

