База данных (sqlite3) с индексным деревом над всеми ID


# Ссылка на on_court.db (sqlite database dump)
# https://drive.google.com/file/d/0BzgFvyR1WEfpV3FtaDVKeWdsNlE/view?usp=sharing
# скачать, раззиповать и положить в рабочую директорию
# захерачить это в самом верху, чтобы cursor был глобальной переменной, и делать con.close() только в самом конце

import sqlite3
con = sqlite3.connect('on_court.db')
cursor = con.cursor()

cursor.execute("SELECT * FROM sqlite_master")
schema = cursor.fetchall() # можно вывести схему (правда там нет forign key-ев)

query = 'select * from games_atp where ID1_G={id_}'
query = query.format(id_=115)
cursor.execute(query).fetchone()
# » (115, 105, 1, 12, '6-2 6-1', None)

# если делали alter/create/insert into table:
# con.commit()

con.close()
