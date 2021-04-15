from datetime import datetime

def todaycalculate():
    datetimetoday = datetime.today()
    today2 = str(datetimetoday.year) + '년 ' + str(datetimetoday.month) + '월 ' + str(datetimetoday.day) + '일 ' + str(datetimetoday.hour) + '시 ' + str(datetimetoday.minute) + '분 ' + str(datetimetoday.second) + '초 '
    return today2