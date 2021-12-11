from dbcm import UseDatabase



def work_with_db(dbconfig, _SQL, scheme):
    result = []
    with UseDatabase(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Cursor is None')
        cursor.execute(_SQL)
        result = []
        for line in cursor.fetchall():
            result.append(dict(zip(scheme, line)))
    return result

def make_update(dbconfig, sql):
    with UseDatabase(dbconfig) as cursor:
        a = cursor.execute(sql)
    return a
