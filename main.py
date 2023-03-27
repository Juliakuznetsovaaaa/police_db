from tkinter import Button

import mysql
from mysql.connector import Error
from tkinter import *
from tkinter.messagebox import showinfo
from functools import partial



def get_select_int(select_str_format):
    return int('{}'.format(select_str_format[0]))


def get_select_str(id_str_format):
    return str('{}'.format(id_str_format[0]))


def show_section(conn, p_info1):
    p_section = p_info1.get()
    if p_section == "":
        print("insert status. All fields are required")
    else:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT `name_violation` FROM `collection of violations`"
                           f"WHERE `section`='{p_section}'")
            violation = cursor.fetchone()
            violation = get_select_str(violation)
    showinfo(title="Нарушение", message=violation)


def show_name(conn, p_info1):
    p_passport = p_info1.get()
    if p_passport == "":
        print("insert status. All fields are required")
    else:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT `full_name` FROM `people` "
                           f"WHERE `pasport_number`='{p_passport}'")
            person = cursor.fetchone()
            person = get_select_str(person)
    showinfo(title="ФИО", message=person)

def find_person_into_base(conn, p_info1, p_info2, p_info3):
    p_name=p_info1
    p_date=p_info2
    p_passport=p_info3
    with conn.cursor() as cursor:
        cursor.execute(f"""SELECT IFNULL((SELECT `id_people` FROM `people`
                                  WHERE 'full_name'='{p_name}' AND 'birth_date'='{p_date}' AND 'pasport_number'='{p_passport}' ), 'null')""")
        person=cursor.fetchone()
        person=get_select_str(person)
        if person=='null':
            showinfo(title="Извините!", message="Человек не найден! Добавьте в базу!")


def add_violation_btn_clicked(conn, p_info1, p_info2, p_info3):
    p_passport = p_info1.get()
    p_section = p_info2.get()
    p_date = p_info3.get()
    if p_passport == "":
        print("insert status. All fields are required")
    else:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT `id_people` FROM `people` "
                           f"WHERE `pasport_number`='{p_passport}'")
            person = cursor.fetchone()
            person = get_select_str(person)
            cursor.execute(f"SELECT `id_violation` FROM `collection of violations`"
                           f"WHERE `section`='{p_section}'")
            violation = cursor.fetchone()
            violation = get_select_str(violation)
            cursor.execute(f"SELECT `amount_violation` FROM `collection of violations`"
                           f"WHERE `section`='{p_section}'")
            amount = cursor.fetchone()
            amount = get_select_int(amount)
            cursor.execute(f"""SELECT IFNULL((SELECT `id_people` FROM `fine`
                           WHERE 'fine_date' BETWEEN 1999-11-01 AND 2000-11-01 AND `id_people`='{person}'), 'null')""")
            increase = cursor.fetchone()
            increase = get_select_str(increase)
            if increase != 'null':
                amount = amount * 1.1
            cursor.execute(
                "insert into fine (id_people, id_violation, fine_date, actual_amount) values ('" + person + "','" + violation + "','" + p_date + "','" + str(
                    amount) + "')")
            conn.commit()


def add_violation_btm(connection):
    window = Tk()
    window.geometry('1920x1080')
    window.title("Person registration")

    lbl1 = Label(window, text="pasport_people")
    lbl1.place(x=20, y=30)

    lbl2 = Label(window, text="section")
    lbl2.place(x=20, y=60)

    lbl3 = Label(window, text="violation_date")
    lbl3.place(x=20, y=90)

    p_name = Entry(window)
    p_name.place(x=150, y=30)

    p_violation = Entry(window)
    p_violation.place(x=150, y=60)

    p_date = Entry(window)
    p_date.place(x=150, y=90)

    add_violation_btn_clicked_wo_arg = partial(add_violation_btn_clicked, connection, p_name, p_violation,
                                               p_date, )
    btn1 = Button(window, text='Add violation into database', command=add_violation_btn_clicked_wo_arg)
    btn1.place(x=150, y=150)

    add_full_name_messagebox = partial(show_name, connection, p_name)
    btn2 = Button(window, text='Show full name', command=add_full_name_messagebox)
    btn2.place(x=300, y=30)

    add_violation_messagebox = partial(show_section, connection, p_violation)
    btn3 = Button(window, text='Show violation', command=add_violation_messagebox)
    btn3.place(x=300, y=60)


def add_person_btn_clicked(conn, p_info1, p_info2, p_info3, p_info4):
    p_name = p_info1.get()
    p_birth = p_info2.get()
    p_passport = p_info3.get()
    p_liesince = p_info4.get()
    if p_name == "":
        print("insert status. All fields are required")
    else:
        query_is_in_db = f"""SELECT IFNULL((SELECT `id_people` FROM `people`
               WHERE 'pasport_number'='{p_passport}'), 'null')"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_is_in_db)
            ((p_in_db,),) = cursor.fetchall()
            conn.commit()
        if p_in_db == 'null':
            with conn.cursor() as cursor:
                cursor.execute(
                    "insert into people (full_name, birth_date, pasport_number, driver_licence_number) values ('" + p_name + "','" + p_birth + "','" + p_passport + "','" + p_liesince + "')")
                conn.commit()


def add_person_btn(connection):
    window = Tk()
    window.geometry('1920x1080')
    window.title("Person registration")

    lbl1 = Label(window, text="person's name")
    lbl1.place(x=20, y=30)

    lbl2 = Label(window, text="Date of birth")
    lbl2.place(x=20, y=60)

    lbl3 = Label(window, text="Passport")
    lbl3.place(x=20, y=90)

    lbl4 = Label(window, text="Driving licence")
    lbl4.place(x=20, y=120)

    p_name = Entry(window)
    p_name.place(x=170, y=30)

    p_birthday = Entry(window)
    p_birthday.place(x=170, y=60)

    p_pasport = Entry(window)
    p_pasport.place(x=170, y=90)

    p_liecense = Entry(window)
    p_liecense.place(x=170, y=120)

    find_person_into_base_wo_arg = partial(find_person_into_base, connection, p_name, p_birthday, p_pasport)
    btn0=Button(window, text='Find person in database', command=find_person_into_base_wo_arg)
    btn0.place(x=20, y=150)

    add_person_btn_clicked_wo_arg = partial(add_person_btn_clicked, connection, p_name, p_birthday,
                                            p_pasport, p_liecense, )
    btn1 = Button(window, text='Add person into database', command=add_person_btn_clicked_wo_arg)
    btn1.place(x=170, y=150)


def gui(connection):
    window = Tk()
    window.geometry("1920x1080")
    window.title("police database")
    lbl1 = Label(window, text="Welcome to police database.", font=("Montserrat", 15))
    lbl1.place(x=60, y=60)

    add_person_btn_wo_arg = partial(add_person_btn, connection)
    btn1 = Button(window, text="Register new person", font=("Montserrat", 15), command=add_person_btn_wo_arg)
    btn1.place(x=60, y=120)

    add_violation_btn_clicked_wo_arg = partial(add_violation_btm, connection)
    btn2 = Button(window, text="Register new violation", font=("Montserrat", 15),
                  command=add_violation_btn_clicked_wo_arg)
    btn2.place(x=60, y=180)

    window.mainloop()


conn = mysql.connector.connect(user='root', password='898989', host='127.0.0.1', port='3306',
                               database='traffic police')
gui(conn)
