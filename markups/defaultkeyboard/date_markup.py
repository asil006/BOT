import datetime

from aiogram.types import ReplyKeyboardMarkup

day = datetime.datetime.now().day
month = datetime.datetime.now().month
year = datetime.datetime.now().year


def date():
    dates = {1: 31,
             2: 28,
             3: 31,
             4: 30,
             5: 31,
             6: 30,
             7: 31,
             8: 31,
             9: 30,
             10: 31,
             11: 30,
             12: 31}

    if year == 2024 or year == 2028 or year == 2032:
        dates = {1: 31,
                 2: 29,
                 3: 31,
                 4: 30,
                 5: 31,
                 6: 30,
                 7: 31,
                 8: 31,
                 9: 30,
                 10: 31,
                 11: 30,
                 12: 31}
    return dates


date1 = str(year) + '-' + str(month) + '-' + str(day)
date2 = str(year) + '-' + str(month) + '-' + str(day + 1)
date3 = str(year) + '-' + str(month) + '-' + str(day + 2)
for i, j in date().items():
    if i == month and day + 2 > j == day + 1:
        if month == 12:
            date3 = str(year + 1) + '-' + str(1) + '-' + str(1)
        else:
            date3 = str(year) + '-' + str(i + 1) + '-' + str(1)
    if i == month and day == j:
        if month == 12:
            date2 = str(year + 1) + '-' + str(1) + '-' + str(1)
            date3 = str(year + 1) + '-' + str(1) + '-' + str(2)
        else:
            date2 = str(year) + '-' + str(i + 1) + '-' + str(1)
            date3 = str(year) + '-' + str(i + 1) + '-' + str(2)
    if datetime.datetime.now().hour > 20:
        day = datetime.datetime.now().day + 1
        date1 = str(year) + '-' + str(month) + '-' + str(day)
        date2 = str(year) + '-' + str(month) + '-' + str(day + 1)
        date3 = str(year) + '-' + str(month) + '-' + str(day + 2)
        if i == month and day + 2 > j == day + 1:
            if month == 12:
                date3 = str(year + 1) + '-' + str(1) + '-' + str(1)
            else:
                date3 = str(year) + '-' + str(i + 1) + '-' + str(1)
        if i == month and day == j:
            if month == 12:
                date2 = str(year + 1) + '-' + str(1) + '-' + str(1)
                date3 = str(year + 1) + '-' + str(1) + '-' + str(2)
            else:
                date2 = str(year) + '-' + str(i + 1) + '-' + str(1)
                date3 = str(year) + '-' + str(i + 1) + '-' + str(2)



date_list = [date1, date2, date3]
date_markup = ReplyKeyboardMarkup(resize_keyboard=True)
date_markup.row(date1, date2, date3)
date_markup.add('🔚 Главный меню')
