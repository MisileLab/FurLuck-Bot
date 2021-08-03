import json
import secrets
from datetime import datetime

import discord
import requests
from bitlyshortener import Shortener
from bs4 import BeautifulSoup
from selenium import webdriver
from dislash import Option, Type, ActionRow, ButtonStyle, SelectMenu
import hashlib
import pymysql
from dotenv import dotenv_values
import pytz

tokens_pool2 = []
musicqueue = {}
musicqueueyes = {}

with open('bitlytoken.txt') as f:
    tokens_pool = f.readlines()
    print(tokens_pool)
for i in range(len(tokens_pool)):
    print(i)
    tokens_pool2.append(str(tokens_pool[i]).replace('\n', ''))
    del i
print(tokens_pool2)

mysqlconnect = open('pymysql.json', 'r').read()
mysqlconnect = json.loads(mysqlconnect)

config = dotenv_values(".env")
hypixel_api_key = config['hypixelapi']


def tz_from_utc_ms_ts(utc_ms_ts, tz_info):
    utc_datetime = datetime.utcfromtimestamp(utc_ms_ts / 1000.)
    return utc_datetime.replace(tzinfo=pytz.timezone('UTC')).astimezone(pytz.timezone(tz_info))


def unix_to_datetime(unixtime):
    return datetime.fromtimestamp(unixtime / 1000)


def todaycalculate():
    datetimetoday = datetime.today()
    return (
            str(datetimetoday.year)
            + '년 '
            + str(datetimetoday.month)
            + '월 '
            + str(datetimetoday.day)
            + '일 '
            + str(datetimetoday.hour)
            + '시 '
            + str(datetimetoday.minute)
            + '분 '
            + str(datetimetoday.second)
            + '초 '
    )


def makeformat(datetime1):
    return (
            str(datetime1.year)
            + '년 '
            + str(datetime1.month)
            + '월 '
            + str(datetime1.day)
            + '일 '
            + str(datetime1.hour)
            + '시 '
            + str(datetime1.minute)
            + '분 '
            + str(datetime1.second)
            + '초 '
    )


class Weather:
    def __init__(self, detectdict: dict):
        self.temp1 = detectdict['temp']
        self.cast1 = detectdict['cast']
        self.dust1 = detectdict['dust']
        self.dust_txt1 = detectdict['dust_txt']
        self.ultra_dust1 = detectdict['ultra_dust']
        self.ultra_dust_txt1 = detectdict['ultra_dust_txt']
        self.ozone1 = detectdict['ozone']
        self.ozonetext1 = detectdict['ozonetext']
        self.mintemp1 = detectdict['mintemp']
        self.maxtemp1 = detectdict['maxtemp']
        self.sensibletemp1 = detectdict['sensibletemp']
        self.weatherimage1 = detectdict['weatherurl']

    @property
    def temp(self):
        return self.temp1

    @property
    def cast(self):
        return self.cast1

    @property
    def dust(self):
        return self.dust1

    @property
    def dust_txt(self):
        return self.dust_txt1

    @property
    def ultra_dust(self):
        return self.ultra_dust1

    @property
    def ultra_dust_txt(self):
        return self.ultra_dust_txt1

    @property
    def ozone(self):
        return self.ozone1

    @property
    def ozonetext(self):
        return self.ozonetext1

    @property
    def mintemp(self):
        return self.mintemp1

    @property
    def maxtemp(self):
        return self.maxtemp1

    @property
    def sensibletemp(self):
        return self.sensibletemp1

    @property
    def weatherimage(self):
        return self.weatherimage1


class WeatherBrowser:
    def __init__(self, position: str):
        self.position = position

    # noinspection PyBroadException
    @staticmethod
    def open_browser():
        try:
            browser = webdriver.Edge()
        except Exception:
            try:
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('window-size=1920x1080')
                options.add_argument("disable-gpu")
                print("Chrome")
                browser = webdriver.Chrome('chromedriver', options=options)
            except Exception:
                try:
                    options = webdriver.ChromeOptions()
                    options.add_argument('window-size=1920x1080')
                    print('Chrome but not headless')
                    browser = webdriver.Chrome('chromedriver', options=options)
                except Exception as e:
                    raise e
        return browser

    def get_weather_data(self):
        browser = self.open_browser()
        position = self.position
        browser.get(url=f"https://search.naver.com/search.naver?&query={position.replace(' ', '+')}+날씨")
        try:
            browserfindelement = browser.find_element_by_class_name(name="ico_state").value_of_css_property(
                "background-image")
        except Exception as e:
            browser.close()
            raise e
        else:
            weatherurl = int(str(browserfindelement).replace(
                'url("https://ssl.pstatic.net/sstatic/keypage/outside/scui/weather_new/img/weather_svg/icon_wt_',
                "").replace('.svg")', ""))
        browser.close()
        req = requests.get(f'https://search.naver.com/search.naver?ie=utf8&query={position.replace(" ", "+")}+날씨')
        soup = BeautifulSoup(req.text, 'html.parser')
        req.close()
        try:
            todaytemperature = str(
                soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text) + '도'
            if todaytemperature is None:
                raise ValueError
        except requests.TooManyRedirects:
            pass
        except ValueError:
            raise ValueError
        else:
            self.sort_data(soup, weatherurl)

    def sort_data(self, soup, weatherurl):
        result = self.somanydust(soup)
        todaytemperature = result["temp"]
        lowtemperature = result["mintemp"]
        hightemperature = result["hightemp"]
        cast_txt = result["cast"]
        misaemungi = result["dust"]
        misaemungitext = result["dust_txt"]
        chomisaemungi = result["ultra_dust"]
        chomisaemungitext = result["ultra_dust_txt"]
        ozone = result["ozone"]
        ozonetext = result["ozonetext"]
        sensibletemp = result["sensibletemp"]
        dict1 = self.data_to_dict(temp=todaytemperature, mintemp=lowtemperature, maxtemp=hightemperature, cast=cast_txt,
                                  dust=misaemungi, dust_txt=misaemungitext, ultra_dust=chomisaemungi, ultra_dust_txt=chomisaemungitext,
                                  ozone=ozone, ozonetext=ozonetext, sensibletemp=sensibletemp, weatherurl=weatherurl)
        return Weather(dict1)

    @staticmethod
    def somanydust(soup):
        todaytemperature = str(soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text) + '도'
        lowtemperature = str(
            soup.find('ul', class_='info_list').find('span', class_='merge').find('span', class_='min').find('span',
                                                                                                             class_='num').text) + '도'
        hightemperature = str(
            soup.find('ul', class_='info_list').find('span', class_='merge').find('span', class_='max').find('span',
                                                                                                             class_='num').text) + '도'
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
        return {"temp":todaytemperature,"dust":misaemungi,"dust_txt":misaemungitext,
                "ultra_dust":chomisaemungi,"ultra_dust_txt":chomisaemungitext, "ozone":ozone, "ozonetext":ozonetext,
                "lowtemp":lowtemperature, "hightemp":hightemperature,"cast":cast_txt, "sensibletemp":sensibletemp}

    @staticmethod
    def data_to_dict(temp, cast, dust, dust_txt, ultra_dust, ultra_dust_txt, ozone, ozonetext, mintemp, maxtemp, sensibletemp, weatherurl):
        return {
            "temp": temp,
            "cast": cast,
            "dust": dust.replace("㎍/㎥", ""),
            "dust_txt": dust_txt,
            "ultra_dust": ultra_dust.replace("㎍/㎥", ""),
            "ultra_dust_txt": ultra_dust_txt,
            "ozone": ozone.replace("ppm", ""),
            "ozonetext": ozonetext,
            "mintemp": mintemp,
            "maxtemp": maxtemp,
            "sensibletemp": str(sensibletemp) + "도",
            "weatherurl": f"{str(svg_to_link(weatherurl))}.png"
        }


def svg_to_link(weatherurl):
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
    return weatherurl2[weatherurl - 1]


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
    return shortener.shorten_urls(long_urls=link2)


# noinspection PyTypeChecker
def warn(memberid: int, amount: int, get: bool):
    mysql1 = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"],
                             db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"],
                             autocommit=True)
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
    if not get:
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
def helpingyou(memberid: int):
    mysql1 = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"],
                             db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"],
                             autocommit=True)
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
        try:
            insertmemberdataonce(cursor, memberid)
        except pymysql.err.IntegrityError:
            pass
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


def insertmemberdataonce(cursor, memberid: int):
    sql = "INSERT INTO `furluckbot1` (id, level1, warn, helpingme) VALUES (%s, 1, 0, 0)"
    cursor.execute(sql, memberid)


def insertserverdataonce(cursor, guildid: int):
    sql = "INSERT INTO `serverfurluckbot` (serverid, insaname, gongjiid, logid) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (guildid, 0, 0, 0))


class DontHaveMoney(Exception):
    pass


class FailedDobak(Exception):
    pass


def getmoney(memberid: int):
    mysql1 = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"],
                             db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"],
                             autocommit=True)
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


def connect_cursor():
    return pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"],
                           db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"],
                           autocommit=True)


def dobakmoney(memberid: int, money: int):
    mysql1 = connect_cursor()
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `furluckbot1`;")
    resultcursor = cursor.fetchall()
    result1 = cursor_to_result(resultcursor, 'id', memberid)
    if result1 is None:
        insertmemberdataonce(cursor, memberid)
        sql = "SELECT * FROM `furluckbot1`;"
        cursor.execute(sql)
        resultcursor = cursor.fetchall()
        result1 = cursor_to_result(resultcursor, 'id', memberid)
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
    result1 = cursor_to_result(resultcursor, 'id', memberid)
    mysql1.close()
    return result1


def cursor_to_result(resultcursor, equal:str, id2):
    result1 = None
    for i1 in resultcursor:
        resultid = i1[equal]
        if resultid == id2:
            result1 = i1
            break
    return result1


def miningmoney(memberid: int):
    mysql1 = connect_cursor()
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM `furluckbot1`;"
    cursor.execute(sql)
    resultcursor = cursor.fetchall()
    result1 = cursor_to_result(resultcursor, 'id', memberid)
    if result1 is None:
        insertmemberdataonce(cursor, memberid)
        sql = "SELECT * FROM `furluckbot1`;"
        cursor.execute(sql)
        resultcursor = cursor.fetchall()
        result1 = cursor_to_result(resultcursor, 'id', memberid)
    sql = "UPDATE furluckbot1 SET level1 = %s WHERE id = %s"
    cursor.execute(sql, (result1['level1'] + 3000, memberid))
    result1 = cursor_to_result(resultcursor, 'id', memberid)
    mysql1.close()
    return result1


def serverdata(mode: str, guildid: int, channelid: int, get: bool):
    mysql1 = connect_cursor()
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `serverfurluckbot`;")
    resultcursor = cursor.fetchall()
    result = None
    cursor_to_result(resultcursor, 'serverid', guildid)
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
        cursor_to_result(resultcursor, 'serverid', guildid)
    except KeyError as e:
        if not get:
            raise KeyError(e)
    mysql1.close()
    return result


def noticeusingbot(guildid: int, channelid: int, get: bool):
    mysql1 = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"],
                             db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"],
                             autocommit=True)
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
    if not get:
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

    def make_option(self, name: str, description: str, required: bool, type: Type):
        option = Option(name=name, description=description, required=required, type=type)
        self.option.append(option)
        return self.option

    @property
    def options(self):
        return self.option


class NewActionRow:
    def __init__(self):
        self.component = ActionRow()

    def add_button(self, style: ButtonStyle, name: str, custom_id: str):
        self.component.add_button(style=style, label=name, custom_id=custom_id)

    @property
    def components(self):
        return [self.component]


class Vote:
    def __init__(self):
        self.voteid = hashlib.sha512(str(secrets.SystemRandom().randint(1, 10000000)).encode('utf-8')).hexdigest()
        self.mysql = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"],
                                     host=mysqlconnect["host"], db=mysqlconnect["db"], charset=mysqlconnect["charset"],
                                     port=mysqlconnect["port"], autocommit=True)
        self.cursor = self.mysql.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute("SELECT * FROM `votes`")
        resultcursor = self.cursor.fetchall()
        for i1 in resultcursor:
            resultid = i1['voteid']
            if resultid == self.voteid:
                self.voteid = hashlib.sha512(
                    str(secrets.SystemRandom().randint(1, 10000000)).encode('utf-8')).hexdigest()
        self.cursor.execute("INSERT INTO `votes` (voteid, result1, bot) VALUES (%s, %s, %s)",
                            (self.voteid, 1233, self.voteid))

    def add_vote(self, opinion: bool, interid: int):
        if opinion:
            self.cursor.execute(
                "INSERT INTO `votes` (voteid, bot, result1) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE bot=%s, result1=%s",
                (self.voteid, self.voteid + str(interid), 0, self.voteid + str(interid), 0))
        else:
            self.cursor.execute(
                "INSERT INTO `votes` (voteid, bot, result1) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE bot=%s, result1=%s",
                (self.voteid, self.voteid + str(interid), 1, self.voteid + str(interid), 1))

    def close(self):
        self.cursor.execute('SELECT * FROM `votes` WHERE voteid = %s', self.voteid)
        resultcursor = self.cursor.fetchall()
        trueopinion = 0
        falseopinion = 0
        for i1 in resultcursor:
            resultid = i1['result1']
            voteid = i1['voteid']
            bot = i1['bot']
            if bot != self.voteid and voteid == self.voteid:
                if resultid == 0:
                    trueopinion += 1
                elif resultid == 1:
                    falseopinion += 1
        self.cursor.execute("DELETE FROM `votes` WHERE voteid = %s", self.voteid)
        self.cursor.close()
        return {"true": trueopinion, "false": falseopinion}


class Information:
    def __init__(self, dict1: dict):
        try:
            self.rank1 = dict1['rank']
        except KeyError:
            self.rank1 = 'None'
        self.packagerank1 = dict1['newPackageRank']
        self.name1 = dict1['displayname']
        self.firstlogin1 = makeformat(unix_to_datetime(dict1['firstLogin']))
        self.lastlogin1 = makeformat(unix_to_datetime(dict1['lastLogin']))
        self.lastlogout1 = makeformat(unix_to_datetime(dict1['lastLogout']))

    @property
    def rank(self):
        return self.rank1

    @property
    def packagerank(self):
        return self.packagerank1

    @property
    def name(self):
        return self.name1

    @property
    def firstlogin(self):
        return self.firstlogin1

    @property
    def lastlogin(self):
        return self.lastlogin1

    @property
    def lastlogout(self):
        return self.lastlogout1


class UsernameNotValid(Exception):
    pass


class HypixelRankHistory:
    def __init__(self, detectdict: dict):
        self.detectdict = detectdict
        self.lol()

        for i2 in self.rankrecord.keys():
            dictlol = self.detectdict[i2]
            try:
                dictlol["REGULAR"]
            except KeyError:
                regular = False
            else:
                regular = True
            try:
                dictlol["VIP"]
            except KeyError:
                vip = False
            else:
                vip = True
            try:
                dictlol["VIP_PLUS"]
            except KeyError:
                vip_plus = False
            else:
                vip_plus = True
            try:
                dictlol["MVP"]
            except KeyError:
                mvp = False
            else:
                mvp = True
            try:
                dictlol["MVP_PLUS"]
            except KeyError:
                mvp_plus = False
            else:
                mvp_plus = True
            self.rankrecord[i2] = HypixelRank(regular, vip, vip_plus, mvp, mvp_plus)

    # noinspection PyShadowingNames
    def lol(self, a: dict = None):
        if a is None:
            a = self.detectdict
        if len(a) > 25:
            a = dict(reversed(a.items()))
            a.popitem()
            a = dict(reversed(a.items()))
        if len(a) <= 25:
            # noinspection PyAttributeOutsideInit
            self.rankrecord = a
            return a
        self.lol(a)

    @property
    def rankhistory(self):
        return self.rankrecord


class HypixelRank:
    def __init__(self, regular: bool, vip: bool, vip_plus: bool, mvp: bool, mvp_plus: bool):
        self.regular1 = regular
        self.vip1 = vip
        self.vip_plus1 = vip_plus
        self.mvp1 = mvp
        self.mvp_plus1 = mvp_plus

    @property
    def regular(self):
        return self.regular1

    @property
    def vip(self):
        return self.vip1

    @property
    def vip_plus(self):
        return self.vip_plus1

    @property
    def mvp(self):
        return self.mvp1

    @property
    def mvp_plus(self):
        return self.mvp_plus1


class YouAlreadylookedupthisnamerecently(Exception):
    pass


class KeyLimit(Exception):
    pass


class HypixelAPI:
    def __init__(self, playername: str):
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{playername}")
        if response.status_code == 204:
            raise UsernameNotValid("username is not valid:", playername)
        self.playername = playername

    def get_response(self, get: str):
        params = {'key': hypixel_api_key, 'name': self.playername}
        if get.find("/") == -1:
            get = "/" + get
        response = requests.get(f"https://api.hypixel.net{get}", params)
        if response.status_code != 200 and json.loads(response.content)["cause"] == "You have already looked up this name recently":
            raise YouAlreadylookedupthisnamerecently("yes it's error")
        if response.status_code == 429:
            raise KeyLimit("Key Limit Exceed")
        return json.loads(response.content)

    def get_information(self):
        try:
            response = self.get_response("/player")
        except Exception as e:
            raise e
        else:
            if response is False:
                return False
            return Information(response['player'])

    def get_rankhistory(self):
        try:
            response = self.get_response("/player")
        except Exception as e:
            raise e
        else:
            if response is False:
                return False
            return HypixelRankHistory(response["player"]["monthlycrates"]).rankhistory

    def get_online(self, response: Information = None):
        try:
            if response is None:
                response = self.get_information()
        except Exception as e:
            raise e
        else:
            if response is False:
                return None
            return bool(response.lastlogin > response.lastlogout)


def booltostr(arg: bool):
    if arg:
        return "없음"
    return "있음"

def weathercomponents(response):
    components = SelectMenu(custom_id="rankhistory", placeholder="보고 싶은 날짜를 골라주세요.", max_values=len(response))
    for key in response.keys():
        components.add_option(label=key, value=key, description=f"{key} 날짜의 기록을 보여줍니다.")

def weatherembed(labels, response, name):
    embed = discord.Embed(name=f"{name}의 랭크 기록")
    for i2 in labels:
        value = response[i2]
        value1 = f"deafult={booltostr(value.regular)}, vip={booltostr(value.vip)}, vip+={booltostr(value.vip_plus)}" \
                 f", mvp={booltostr(value.mvp)}, mvp+={booltostr(value.mvp_plus)}"
        embed.add_field(name=i2, value=value1)

def except_error(inter, name):
    response = None
    response2 = None
    try:
        response: Information = HypixelAPI(playername=name).get_information()
        response2: bool or None = HypixelAPI(playername=name).get_online(response)
    except UsernameNotValid:
        await inter.reply("유저의 이름이 알맞지 않습니다.")
    except YouAlreadylookedupthisnamerecently:
        await inter.reply("이 플레이어를 최근에 누군가 검색했습니다.")
    except KeyLimit:
        await inter.reply("1분에 120번 이상 API를 사용했습니다. 잠시만 기다려주세요.")
    except Exception as e:
        await inter.reply("클라이언트 안에서 알 수 없는 에러가 났습니다.")
        raise e
    return [response, response2]