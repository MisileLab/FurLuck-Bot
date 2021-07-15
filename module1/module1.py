import json
import secrets
from datetime import datetime
import pymysql
import requests
from bitlyshortener import Shortener
from bs4 import BeautifulSoup
from selenium import webdriver
from dislash import Option, Type, ActionRow, ButtonStyle
import hashlib

tokens_pool2 = []
musicqueue = {}
musicqueueyes = {}

with open('bitlytoken.txt') as f:
    tokens_pool = f.readlines()
    print(tokens_pool)
for i in range(len(tokens_pool)):
    print(i)
    tokens_pool2.append(str(tokens_pool[i]).replace('\n', ''))
print(tokens_pool2)

mysqlconnect = open('pymysql.json', 'r').read()
mysqlconnect = json.loads(mysqlconnect)

def todaycalculate():
    datetimetoday = datetime.today()
    today2 = str(datetimetoday.year) + '년 ' + str(datetimetoday.month) + '월 ' + str(datetimetoday.day) + '일 ' + str(datetimetoday.hour) + '시 ' + str(datetimetoday.minute) + '분 ' + str(datetimetoday.second) + '초 '
    return today2

def makeformat(datetime1):
    today2 = str(datetime1.year) + '년 ' + str(datetime1.month) + '월 ' + str(datetime1.day) + '일 ' + str(datetime1.hour) + '시 ' + str(datetime1.minute) + '분 ' + str(datetime1.second) + '초 '
    return today2

class Weather:
    def __init__(self, detectdict:dict):
        self.temp = detectdict['temp']
        self.cast = detectdict['cast']
        self.dust = detectdict['dust']
        self.dust_txt = detectdict['dust_txt']
        self.ultra_dust = detectdict['ultra_dust']
        self.ultra_dust_txt = detectdict['ultra_dust_txt']
        self.ozone = detectdict['ozone']
        self.ozonetext = detectdict['ozonetext']
        self.mintemp = detectdict['mintemp']
        self.maxtemp = detectdict['maxtemp']
        self.sensibletemp = detectdict['sensibletemp']
        self.weatherimage = detectdict['weatherurl']

    @property
    def temp(self):
        return self.temp

    @property
    def cast(self):
        return self.cast

    @property
    def dust(self):
        return self.dust

    @property
    def dust_txt(self):
        return self.dust_txt

    @property
    def ultra_dust(self):
        return self.ultra_dust

    @property
    def ultra_dust_txt(self):
        return self.ultra_dust_txt

    @property
    def ozone(self):
        return self.ozone

    @property
    def ozonetext(self):
        return self.ozonetext

    @property
    def mintemp(self):
        return self.mintemp

    @property
    def maxtemp(self):
        return self.maxtemp

    @property
    def sensibletemp(self):
        return self.sensibletemp

    @property
    def weatherimage(self):
        return self.weatherimage

    @temp.setter
    def temp(self, value):
        self._temp = value

    @weatherimage.setter
    def weatherimage(self, value):
        self._weatherimage = value

    @sensibletemp.setter
    def sensibletemp(self, value):
        self._sensibletemp = value

    @maxtemp.setter
    def maxtemp(self, value):
        self._maxtemp = value

    @mintemp.setter
    def mintemp(self, value):
        self._mintemp = value

    @ozonetext.setter
    def ozonetext(self, value):
        self._ozonetext = value

    @ozone.setter
    def ozone(self, value):
        self._ozone = value

    @ultra_dust_txt.setter
    def ultra_dust_txt(self, value):
        self._ultra_dust_txt = value

    @ultra_dust.setter
    def ultra_dust(self, value):
        self._ultra_dust = value

    @dust_txt.setter
    def dust_txt(self, value):
        self._dust_txt = value

    @dust.setter
    def dust(self, value):
        self._dust = value

    @cast.setter
    def cast(self, value):
        self._cast = value


def get_weather(position:str):
    try:
        browser = webdriver.Edge()
    except Exception as e:
        print(e)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        print("Chrome")
        browser = webdriver.Chrome('chromedriver', options=options)
    browser.get(url=f"https://search.naver.com/search.naver?&query={position.replace(' ', '+')}+날씨")
    try:
        browserfindelement = browser.find_element_by_class_name(name="ico_state").value_of_css_property("background-image")
    except Exception as e:
        print(e)
        browser.close()
        raise ValueError
    else:
        weatherurl = int(str(browserfindelement).replace('url("https://ssl.pstatic.net/sstatic/keypage/outside/scui/weather_new/img/weather_svg/icon_wt_',"").replace('.svg")', ""))
    browser.close()
    req = requests.get(f'https://search.naver.com/search.naver?ie=utf8&query={position.replace(" ", "+")}+날씨')
    soup = BeautifulSoup(req.text, 'html.parser')
    req.close()
    try:
        todaytemperature = str(soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text) + '도'
        if todaytemperature is None:
            print("1")
            raise ValueError
    except requests.TooManyRedirects:
        pass
    except ValueError:
        raise ValueError
    else:
        todaytemperature = str(soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text) + '도'
        lowtemperature = str(soup.find('ul', class_='info_list').find('span', class_='merge').find('span', class_='min').find('span',class_='num').text) + '도'
        hightemperature = str(soup.find('ul', class_='info_list').find('span', class_='merge').find('span', class_='max').find('span',class_='num').text) + '도'
        infolist = soup.find('ul', class_='info_list')
        cast_txt = infolist.find('p', class_='cast_txt').text
        misaemungi = soup.find('dl', class_='indicator').find_all('dd')[0].find('span', class_='num').text
        misaemungitext = soup.find('dl', class_='indicator').find_all('dd')[0]
        misaemungitext = remove_special_region(misaemungitext, 'span').text
        chomisaemungi = soup.find('dl', class_='indicator').find_all('dd')[1].find('span', class_='num').text
        chomisaemungitext = soup.find('dl', class_='indicator').find_all('dd')[1]
        chomisaemungitext = remove_special_region(chomisaemungitext, 'span').text
        ozone = soup.find('dl', class_='indicator').find_all('dd')[2].find('span', class_='num').text
        ozonetext = soup.find('dl', class_='indicator').find_all('dd')[2]
        ozonetext = remove_special_region(ozonetext, 'span').text
        sensibletemp = infolist.find('span', class_='sensible').find('span', class_='num').text
        weatherurl2 = [
            "https://imgur.com/VPuDpZV",
            "https://imgur.com/02sqICQ",
            "https://imgur.com/Px8uR3W",
            "https://imgur.com/hgfEduj",
            "https://imgur.com/6FEXmQK",
            "https://imgur.com/Sl1ueqT",
            "https://imgur.com/BUwOqYx",
            "https://imgur.com/CaQKTy1",
            "https://imgur.com/wWKMPU3",
            "https://imgur.com/IBJROQn",
            "https://imgur.com/IBJROQn",
            "https://imgur.com/WchO5KW",
            "https://imgur.com/VJC4wfv",
            "https://imgur.com/QP6kbP3",
            "https://imgur.com/RsT33Li",
            "https://imgur.com/p8eKpil",
            "https://imgur.com/v6zOXdI",
            "https://imgur.com/xHk7Xex",
            "https://imgur.com/t3DUaoP",
            "https://imgur.com/Sbg2Mmi",
            "https://imgur.com/TbwVn5J",
            "https://imgur.com/hxKCYPr",
            "https://imgur.com/0oHigOh",
            "https://imgur.com/4VHxJjt",
            "https://imgur.com/MAR7Rip",
            "https://imgur.com/Cxyz93G",
            "https://imgur.com/1TECcRk",
            "https://imgur.com/mOxGn6J",
            "https://imgur.com/1FJDoEj",
            "https://imgur.com/JBQz23t",
            "https://imgur.com/qW7bsxg",
            "https://imgur.com/raBRUi3",
            "https://imgur.com/QtEPCkb",
            "https://imgur.com/gSfaZ6W",
            "https://imgur.com/SOqq92z",
            "https://imgur.com/PwtZ8Qs",
            "https://imgur.com/R1hvM7E",
            "https://imgur.com/GpY3BOM",
            "https://imgur.com/XMcWPZc",
            "https://imgur.com/9Kn7KCy"
        ]
        dict1 = {
            "temp":todaytemperature,
            "cast":cast_txt,
            "dust":misaemungi.replace("㎍/㎥", ""),
            "dust_txt":misaemungitext,
            "ultra_dust":chomisaemungi.replace("㎍/㎥", ""),
            "ultra_dust_txt":chomisaemungitext,
            "ozone":ozone.replace("ppm", ""),
            "ozonetext":ozonetext,
            "mintemp":lowtemperature,
            "maxtemp":hightemperature,
            "sensibletemp":str(sensibletemp) + "도",
            "weatherurl":str(weatherurl2[weatherurl-1]) + ".png"
        }
        return Weather(dict1)

def remove_special_region(origin, tagname):
    for x in origin(tagname):
        try:
            x.decompose()
        except AttributeError:
            pass
    return origin

def shortlink(link):
    link2 = link
    if not isinstance(link, list):
        link2 = [link]
    shortener = Shortener(tokens=tokens_pool2, max_cache_size=256)
    link1 = shortener.shorten_urls(long_urls=link2)
    return link1

# noinspection PyTypeChecker
def warn(memberid:int, amount:int, get:bool):
    mysql1 = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"], db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"], autocommit=True)
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM `furluckbot1`;"
    cursor.execute(sql)
    resultcursor = cursor.fetchall()
    result = None
    for i1 in resultcursor:
        resultid = i1['id']
        if resultid == memberid:
            result = i1
            break
    if result is None:
        insertmemberdataonce(cursor=cursor, memberid=memberid)
    if get is True:
        pass
    elif get is False:
        sql = "UPDATE furluckbot1 SET warn = %s WHERE id = %s"
        cursor.execute(sql, (amount, memberid))
    sql = "SELECT * FROM `furluckbot1`;"
    cursor.execute(sql)
    resultcursor = cursor.fetchall()
    result = None
    for i1 in resultcursor:
        resultid = i1['id']
        if resultid == memberid:
            result = i1
            break
    mysql1.close()
    return result

# noinspection PyTypeChecker
def helpingyou(memberid:int):
    mysql1 = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"], db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"], autocommit=True)
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM `furluckbot1`;"
    cursor.execute(sql)
    resultcursor = cursor.fetchall()
    result = None
    for i1 in resultcursor:
        resultid = i1['id']
        if resultid == memberid:
            result = i1
            break
    if result is None:
        insertmemberdataonce(cursor, memberid)
    sql = "SELECT * FROM `furluckbot1`;"
    cursor.execute(sql)
    resultcursor = cursor.fetchall()
    result = None
    for i1 in resultcursor:
        resultid = i1['id']
        if resultid == memberid:
            result = i1
            break
    mysql1.close()
    return result

def insertmemberdataonce(cursor, memberid:int):
    sql = "INSERT INTO `furluckbot1` (id, level1, warn, helpingme) VALUES (%s, 1, 0, 0)"
    cursor.execute(sql, memberid)

def insertserverdataonce(cursor, guildid:int):
    sql = "INSERT INTO `serverfurluckbot` (serverid, insaname, gongjiid, logid) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (guildid, 0, 0, 0))

class DontHaveMoney(Exception):
    pass

class FailedDobak(Exception):
    pass

def getmoney(memberid:int):
    mysql1 = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"],db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"],autocommit=True)
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `furluckbot1`;")
    resultcursor = cursor.fetchall()
    result1 = None
    for i1 in resultcursor:
        resultid = i1['id']
        if resultid == memberid:
            result1 = i1
            break
    if result1 is None:
        insertmemberdataonce(cursor, memberid)
        sql = "SELECT * FROM `furluckbot1`;"
        cursor.execute(sql)
        resultcursor = cursor.fetchall()
        for i1 in resultcursor:
            resultid = i1['id']
            if resultid == memberid:
                result1 = i1
                break
    mysql1.close()
    return result1['level1']

def dobakmoney(memberid:int, money:int):
    mysql1 = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"],db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"],autocommit=True)
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `furluckbot1`;")
    resultcursor = cursor.fetchall()
    result1 = None
    for i1 in resultcursor:
        resultid = i1['id']
        if resultid == memberid:
            result1 = i1
            break
    if result1 is None:
        insertmemberdataonce(cursor, memberid)
        sql = "SELECT * FROM `furluckbot1`;"
        cursor.execute(sql)
        resultcursor = cursor.fetchall()
        for i1 in resultcursor:
            resultid = i1['id']
            if resultid == memberid:
                result1 = i1
                break
    if result1['level1'] < money:
        raise DontHaveMoney
    random1 = secrets.SystemRandom().randint(1, 2)
    if random1 == 1:
        money1 = result1['level1'] - money
        sql = "UPDATE furluckbot1 SET level1 = %s WHERE id = %s"
        cursor.execute(sql, (money1, memberid))
        raise FailedDobak
    money1 = result1['level1'] + money
    sql = "UPDATE furluckbot1 SET level1 = %s WHERE id = %s"
    cursor.execute(sql, (money1, memberid))
    sql = "SELECT * FROM `furluckbot1`;"
    cursor.execute(sql)
    resultcursor = cursor.fetchall()
    for i1 in resultcursor:
        resultid = i1['id']
        if resultid == memberid:
            result1 = i1
            break
    mysql1.close()
    return result1

def miningmoney(memberid:int):
    mysql1 = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"],db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"],autocommit=True)
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM `furluckbot1`;"
    cursor.execute(sql)
    resultcursor = cursor.fetchall()
    result1 = None
    for i1 in resultcursor:
        resultid = i1['id']
        if resultid == memberid:
            result1 = i1
            break
    if result1 is None:
        insertmemberdataonce(cursor, memberid)
        sql = "SELECT * FROM `furluckbot1`;"
        cursor.execute(sql)
        resultcursor = cursor.fetchall()
        for i1 in resultcursor:
            resultid = i1['id']
            if resultid == memberid:
                result1 = i1
                break
    sql = "UPDATE furluckbot1 SET level1 = %s WHERE id = %s"
    cursor.execute(sql, (result1['level1'] + 3000, memberid))
    for i1 in resultcursor:
        resultid = i1['id']
        if resultid == memberid:
            result1 = i1
            break
    mysql1.close()
    return result1

def serverdata(mode:str, guildid:int, channelid:int, get:bool):
    mysql1 = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"], db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"], autocommit=True)
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `serverfurluckbot`;")
    resultcursor = cursor.fetchall()
    result = None
    for i1 in resultcursor:
        resultid = i1['serverid']
        if resultid == guildid:
            result = i1
            break
    if result is None:
        insertserverdataonce(cursor, guildid)
    if get is False:
        if mode != "logid":
            sql = "UPDATE serverfurluckbot SET %s = %s WHERE serverid = %s"
            cursor.execute(sql, (mode, channelid, guildid))
        else:
            sql = "UPDATE serverfurluckbot SET logid = %s WHERE serverid = %s"
            cursor.execute(sql, (channelid, guildid))
    sql = "SELECT * FROM `serverfurluckbot`;"
    cursor.execute(sql)
    resultcursor = cursor.fetchall()
    result = None
    try:
        for i1 in resultcursor:
            resultid = i1['serverid']
            if resultid == guildid:
                result = i1
                break
    except KeyError as e:
        if get is True:
            pass
        elif get is False:
            raise KeyError(e)
    mysql1.close()
    return result

def noticeusingbot(guildid:int, channelid:int, get:bool):
    mysql1 = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"], db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"], autocommit=True)
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `serverfurluckbot`;")
    resultcursor = cursor.fetchall()
    result1 = None
    for i1 in resultcursor:
        resultid = i1['serverid']
        if resultid == guildid:
            result1 = i1
            break
    if result1 is None:
        insertserverdataonce(cursor, guildid)
    if get is False:
        sql = "UPDATE serverfurluckbot SET gongjiid = %s WHERE serverid = %s"
        cursor.execute(sql, (channelid, guildid))
    sql = "SELECT * FROM `serverfurluckbot`;"
    cursor.execute(sql)
    resultcursor = cursor.fetchall()
    mysql1.close()
    return resultcursor

class NewOptionList:
    def __init__(self):
        self.option = []

    def make_option(self, name:str, description:str, required:bool, type:Type):
        option = Option(name=name, description=description, required=required, type=type)
        self.option.append(option)
        return self.option

    @property
    def options(self):
        return self.option

class NewActionRow:
    def __init__(self):
        self.component = ActionRow()

    def add_button(self, style:ButtonStyle, name:str, custom_id:str):
        self.component.add_button(style=style, label=name, custom_id=custom_id)

    @property
    def components(self):
        return [self.component]

class Vote:
    def __init__(self):
        self.voteid = hashlib.sha512(str(secrets.SystemRandom().randint(1, 10000000)).encode('utf-8')).hexdigest()
        self.mysql = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"],db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"],autocommit=True)
        self.cursor = self.mysql.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute("SELECT * FROM `votes`")
        resultcursor = self.cursor.fetchall()
        for i1 in resultcursor:
            print(i1)
            resultid = i1['voteid']
            if resultid == self.voteid:
                self.voteid = hashlib.sha512(str(secrets.SystemRandom().randint(1, 10000000)).encode('utf-8')).hexdigest()
        self.cursor.execute("INSERT INTO `votes` (voteid, result1, bot) VALUES (%s, %s, %s)", (self.voteid, 1233, self.voteid))

    def add_vote(self, opinion:bool, interid:int):
        if opinion is True:
            self.cursor.execute("INSERT INTO `votes` (voteid, bot, result1) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `votes` VALUES voteid=%s, bot=%s, result1=%s", (self.voteid, interid, 0, self.voteid, interid, 0))
        elif opinion is False:
            self.cursor.execute("INSERT INTO `votes` (voteid, bot, result1) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `votes` VALUES voteid=%s, bot=%s, result1=%s", (self.voteid, interid, 1, self.voteid, interid, 1))

    def close(self):
        self.cursor.execute("SELECT * FROM `votes` WHERE voteid = (voteid) VALUES (%s)", self.voteid)
        resultcursor = self.cursor.fetchall()
        trueopinion = 0
        falseopinion = 0
        for i1 in resultcursor:
            resultid = i1['result1']
            bot = i1['bot']
            if bot != self.voteid and resultid == 0:
                trueopinion = trueopinion + 1
            elif bot != self.voteid and resultid == 1:
                falseopinion = falseopinion + 1
        self.cursor.execute("DELETE FROM `votes` WHERE voteid = (%s)", self.voteid)
        return {"true":trueopinion, "false":falseopinion}

