from loader import db


def create_tables():
    try:
        db.execute('''create table if not exists registration 
        (id int primary key,
        name varchar(30),
        phone varchar(18),
        user_id varchar(30)
        )''', commit=True)
        db.execute('''create table if not exists item
        (id int primary key,
        kategory varchar(100),
        name varchar(100),
        info varchar(200),
        price int,
        count int,
        photo varchar(200)
        )''', commit=True)
        db.execute('''create table if not exists count_items
        (id int primary key,
        user_id integer references registration(id),
        count integer default 1
        )''', commit=True)
        db.execute('''create table if not exists korzina_item
        (id int primary key,
        item_id smallint references item(id),
        user_id smallint references registration(id),
        count smallint
        )''', commit=True)
        db.execute('''create table if not exists oformlenie
        (id int primary key,
        time varchar(10),
        date varchar(10),
        money integer,
        user_id smallint references registration(id),
        item text,
        check_zakaz boolean default false,
        location varchar(200) 
        )''', commit=True)
        db.execute('''create table if not exists promokods
        (id int primary key,
        promokod varchar(100),
        user_id  integer references registration(id),
        skidka float
        )''', commit=True)
    except Exception as err:
        print(err)


create_tables()


def insert_item(kategory, name, info, price, count, photo):
    try:
        fetchone = db.execute("select max(id) from item", fetchone=True)
        print(fetchone)
        for i in fetchone:
            if None == i:
                db.execute(f"""insert into item(id, kategory, name, info, price, count, photo) values
    (1, '{kategory}', '{name}', '{info}', {price}, {count}, '{photo}')""", commit=True)
            else:
                db.execute(f"""insert into item(id, kategory, name, info, price, count, photo) values
                    ({i+1}, '{kategory}', '{name}', '{info}', {price}, {count}, '{photo}')""", commit=True)
    except Exception as e:
        print(e)


def insert_user(name, number, user_id):
    try:
        fetchone = db.execute("select max(id) from registration", fetchone=True)
        for i in fetchone:
            if None == i:
                db.execute(f"""insert into registration(id, name, phone, user_id) values
    (1, '{name}', '{number}', '{user_id}')""", commit=True)
            else:
                db.execute(f"""insert into registration(id, name, phone, user_id) values
                    ({i + 1}, '{name}', '{number}', '{user_id}')""", commit=True)
    except Exception as e:
        print(e)


def get_user_id():
    try:
        l = []
        fetchall = db.execute('select user_id from registration', fetchall=True)
        for i in fetchall:
            for j in i:
                l.append(j)
        return l
    except Exception as e:
        print(e)


def get_item(item_name):
    try:
        return db.execute(f"select * from item where name = '{item_name}' and count != 0 ", fetchone=True)
    except Exception as e:
        print(e)


def add_my_basket(item_id, user_id, count):
    try:
        u_id = 0
        fetchone = db.execute(f"select id from registration where user_id = '{user_id}'", fetchone=True)
        for i in fetchone:
            u_id = i
        fetchall = db.execute(f"""select * from korzina_item where item_id = {item_id} and user_id = {u_id}""", fetchone=True)
        if fetchall:
            db.execute(f"""
            update korzina_item
            set count = {count}
            where item_id = {item_id} and user_id = {u_id}""", commit=True)
        else:
            max_id = db.execute('select max(id) from korzina_item', fetchone=True)
            for i in max_id:
                if None == i:
                    db.execute(f"""insert into korzina_item(id, item_id, user_id, count)
                            values (1, {item_id}, {u_id}, {count})""", commit=True)
                else:
                    db.execute(f"""insert into korzina_item(id, item_id, user_id, count)
                                                values ({i + 1}, {item_id}, {u_id}, {count})""", commit=True)
    except Exception as e:
        print(e)


def minus_count_item(item_id, count):
    try:
        db.execute(f"""update item
        set count = count - {count}
        where id = {item_id}""", commit=True)
    except Exception as err:
        print(err)


def my_basket(user_id):
    try:
        return db.execute(f"""select i.id, i.name, i.info, i.price, k_i.count, i.photo, i.count from korzina_item k_i
join item i on i.id = k_i.item_id
join registration r on r.id = k_i.user_id where r.user_id = '{user_id}'
""", fetchall=True)
    except Exception as e:
        print(e)


def oformlenie(time, date, user_id, money, item, latitude, longitude):
    try:
        u_id = 0
        fetchone = db.execute(f"""select id from registration where user_id = '{user_id}'""", fetchone=True)
        for i in fetchone:
            u_id = i
        max_id = db.execute('select max(id) from oformlenie', fetchone=True)
        for i in max_id:
            if None == i:
                db.execute(f"""insert into oformlenie (id, time, date, money, user_id, item, latitude, longitude)
                   values (1, '{time}', '{date}', {money}, {u_id}, '{item}', {latitude}, {longitude});""", commit=True)
            else:
                db.execute(f"""insert into oformlenie (id, time, date, money, user_id, item, latitude, longitude)
    values ({i + 1}, '{time}', '{date}', {money}, {u_id}, '{item}', {latitude}, {longitude});""", commit=True)

    except Exception as e:
        print(e)


def delete_item(user_id):
    try:
        fetchall = db.execute(f"""select k_i.id from korzina_item k_i
join registration r on r.id = k_i.user_id
where r.user_id = '{user_id}'""", fetchall=True)
        for i in fetchall:
            for j in i:
                db.execute(f"""delete from korzina_item
where id = {j}
""", commit=True)
    except Exception as e:
        print(e)


def delete_korzina_item(item_id, count):
    try:
        if count <= 0:
            db.execute(f"delete from korzina_item where item_id = {item_id}", commit=True)
        db.execute('delete from item where count = 0', commit=True)
    except Exception as err:
        print(err)


def count_item(user_id):
    count = int()
    u_id = int()
    try:
        fetchone1 = db.execute(f"""select id from registration where user_id = '{user_id}'""", fetchone=True)
        for i in fetchone1:
            u_id = i
        fetchone2 = db.execute(f"""select count from count_items where user_id = {u_id}""", fetchone=True)
        for i in fetchone2:
            count = i
        return count
    except Exception as err:
        print(err)


def update_plus_count(user_id):
    try:
        u_id = int()
        fetchone = db.execute(f"select id from registration where user_id = '{user_id}'", fetchone=True)
        for i in fetchone:
            u_id = i
        db.execute(f"""update count_items
set count = count + 1
where user_id = {u_id}""", commit=True)
    except Exception as err:
        print(err)


def update_minus_count(user_id):
    try:
        u_id = int()
        fetchone = db.execute(f"select id from registration where user_id = '{user_id}'", fetchone=True)
        for i in fetchone:
            u_id = i
        db.execute(f"""update count_items
        set count = count - 1
        where user_id = {u_id}""", commit=True)
    except Exception as err:
        print(err)


def update_count(user_id):
    u_id = int()
    try:
        fetchone = db.execute(f"""select id from registration where user_id = '{user_id}'""", fetchone=True)
        for i in fetchone:
            u_id = i
        db.execute(f"""update count_items
set count = 1
where user_id = {u_id}""", commit=True)

    except Exception as err:
        print(err)


def get_oformleniya():
    try:
        item = []
        fetchone = db.execute("""select
oformlenie.id, oformlenie.time, oformlenie.date, oformlenie.money, r.user_id, oformlenie.item, oformlenie.latitude, oformlenie.longitude from oformlenie
join registration r on r.id = oformlenie.user_id order by oformlenie.id desc""", fetchone=True)
        for i in fetchone:
            item.append(i)
        return item
    except Exception as err:
        print(err)


def get_id_count():
    try:
        user_id = []
        fetchall = db.execute("""select user_id from count_items""", fetchall=True)
        for i in fetchall:
            for j in i:
                user_id.append(j)
        return user_id
    except Exception as err:
        print(err)


def create_count_id(user_id):
    try:
        list = []
        u_id = int()
        fetchone = db.execute(f"""select id from registration where user_id = '{user_id}'""", fetchone=True)
        for i in fetchone:
            u_id = i
        fetchall = db.execute("select user_id from count_items", fetchall=True)
        for i in fetchall:
            for j in i:
                list.append(j)
        if u_id in list:
            pass
        else:
            max_id = db.execute('select max(id) from count_items', fetchone=True)
            for i in max_id:
                if None == i:
                    db.execute(f"""insert into count_items(id, user_id) 
        values (1, {u_id})""", commit=True)
                else:
                    db.execute(f"""insert into count_items(id, user_id) 
                            values ({i + 1}, {u_id})""", commit=True)

    except Exception as err:
        print(err)


def item_count(item_id):
    try:
        fetchone = db.execute(f"""select count from item where id = {item_id}""", fetchone=True)
        for i in fetchone:
            return i
    except Exception as err:
        print(err)


def get_kategory():
    try:
        list = []
        fetchall = db.execute(f'select distinct kategory from item', fetchall=True)
        for i in fetchall:
            for j in i:
                list.append(j)
        return list
    except Exception as err:
        print(err)


def get_info_user(user_id):
    try:
        list = []
        fetchone = db.execute(f"select * from registration where user_id = '{user_id}'", fetchone=True)
        for i in fetchone:
            list.append(i)
        return list
    except Exception as err:
        print(err)


def add_promokod(promokod, user_id, skidka):
    try:
        u_id = int()
        fetchone = db.execute(f"select id from registration where user_id = '{user_id}'", fetchone=True)
        for i in fetchone:
            u_id = i
        max_id = db.execute('select max(id) from promokods', fetchone=True)
        for i in max_id:
            if None == i:
                db.execute(
                    f"insert into promokods(id, promokod, user_id, skidka) values (1,'{promokod}', {u_id}, {skidka})",
                    commit=True)
            else:
                db.execute(
                    f"insert into promokods(id, promokod, user_id, skidka) values ({i + 1},'{promokod}', {u_id}, {skidka})",
                    commit=True)
    except Exception as err:
        print(err)


def get_promokod(user_id):
    try:
        list = []
        fetchall = db.execute(
            f"select p.promokod, p.skidka from promokods p join registration r on r.id = p.user_id where r.user_id = '{user_id}'",
            fetchall=True)
        for i in fetchall:
            l = [i[0], i[1]]
            list.append(l)
        return list
    except Exception as err:
        print(err)


def delete_promokod(promo, user_id):
    try:
        u_id = int()
        fetchone = db.execute(f"select id from registration where user_id = '{user_id}'", fetchone=True)
        for i in fetchone:
            u_id = i
        db.execute(f"""delete from promokods where user_id = {u_id} and promokod = '{promo}'""", commit=True)
    except Exception as err:
        print(err)


def change_name(name, user_id):
    try:
        u_id = int()
        fetchone = db.execute(f"select id from registration where user_id = '{user_id}'", fetchone=True)
        for i in fetchone:
            u_id = i
        db.execute(f"update registration set name = '{name}' where id = {u_id}", commit=True)
    except Exception as err:
        print(err)


def change_number(number, user_id):
    try:
        u_id = int()
        fetchone = db.execute(f"select id from registration where user_id = '{user_id}'", fetchone=True)
        for i in fetchone:
            u_id = i
        db.execute(f"update registration set phone = '{number}' where id = {u_id}", commit=True)
    except Exception as err:
        print(err)


def get_id(user_id):
    try:
        fetchone = db.execute(f"select id from registration where user_id = '{user_id}'", fetchone=True)
        for i in fetchone:
            return i
    except Exception as err:
        print(err)


def clear_korzina(user_id, id):
    try:
        db.execute(f"""delete from korzina_item
where item_id = {id} and user_id = {get_id(user_id)}""", commit=True)
    except Exception as err:
        print(err)


def get_count_korzina_item(user_id, id):
    try:
        fetchone = db.execute(f"select count from korzina_item where user_id = {get_id(user_id)} and item_id = {id}",
                              fetchone=True)
        for i in fetchone:
            return i
    except Exception as err:
        print(err)


def increase(user_id, id):
    try:
        db.execute(f"""update korzina_item
set count = count - 1
where user_id = {get_id(user_id)} and item_id = {id}""", commit=True)
    except Exception as err:
        print(err)


def decrease(user_id, id):
    try:
        db.execute(f"""update korzina_item
set count = count + 1
where user_id = {get_id(user_id)} and item_id = {id}""", commit=True)
    except Exception as err:
        print(err)


def get_korzina():
    try:
        list = []
        fetchall = db.execute(
            '''select k_i.id, k_i.item_id, r.user_id, k_i.count from korzina_item k_i join registration r where r.id = k_i.user_id''',
            fetchall=True)
        for i in fetchall:
            list.append([i[0], i[1], i[2], i[3]])
        return list
    except Exception as err:
        print(err)
