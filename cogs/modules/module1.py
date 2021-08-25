import json
import secrets
from datetime import datetime
import time
from discord.ext import commands
from dislash.interactions.slash_interaction import SlashInteraction
from . import module2 as md2
import discord
import requests
from bitlyshortener import Shortener
from bs4 import BeautifulSoup
from selenium import webdriver
from dislash import ActionRow, ButtonStyle, SelectMenu, ClickListener
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
for i, i2 in enumerate(tokens_pool):
    print(i2)
    tokens_pool2.append(str(i2).replace('\n', ''))
    del i2
print(tokens_pool2)

config = dotenv_values(".env")
hypixel_api_key = config['hypixelapi']
mysqlconnect = {
                "host": config['host'],
                "user": config['user'],
                "password": config['password'],
                "db": config['db'],
                "charset": config['charset'],
                "port": int(config['port'])
                }


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
                options = webdriver.ChromeOptions()
                options.add_argument('window-size=1920x1080')
                print('Chrome but not headless')
                browser = webdriver.Chrome('chromedriver', options=options)
        return browser

    def get_weather_data(self):
        position = self.position
        weatherurl = self.seleniumbrowser()
        req = requests.get(
            f'https://search.naver.com/search.naver?ie=utf8&query={position.replace(" ", "+")}+날씨')
        soup = BeautifulSoup(req.text, 'html.parser')
        req.close()
        try:
            soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text()
        except requests.TooManyRedirects:
            pass
        else:
            self.sort_data(soup, weatherurl)

    def seleniumbrowser(self):
        browser = self.open_browser()
        position = self.position
        browser.get(
            url=f"https://search.naver.com/search.naver?&query={position.replace(' ', '+')}+날씨")
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
        return weatherurl

    def sort_data(self, soup, weatherurl):
        result = self.soup_to_dict(soup)
        dicttemp = {"maxtemp": result["hightemp"], "lowtemp": result["lowtemp"],
                    "weatherurl": f'{self.svg_to_link(weatherurl)}.png'}
        result.update(dicttemp)
        return Weather(result)

    def soup_to_dict(self, soup):
        result = self.somanydust(soup)
        temp = self.somanytemp(soup)
        infolist = soup.find('ul', class_='info_list')
        sensibletemp = infolist.find('span', class_='sensible').find(
            'span', class_='num').text
        return {"temp": temp["temp"], "dust": result["dust"].replace("㎍/㎥", ""), "dust_txt": result["dust_txt"],
                "ultra_dust": result["ultra_dust"].replace("㎍/㎥", ""), "ultra_dust_txt": result["ultra_dust_txt"],
                "ozone": result["ozone"], "ozonetext": result["ozone_text"], "lowtemp": temp["lowtemp"],
                "hightemp": temp["hightemp"], "cast": result["cast"], "sensibletemp": sensibletemp}

    def somanydust(self, soup):
        infolist = soup.find('ul', class_='info_list')
        cast_txt = infolist.find('p', class_='cast_txt').text
        dust = self.getdust(soup)
        ultradust = self.getultradust(soup)
        ozone = self.getozone(soup)
        return {"cast": cast_txt, "dust": dust[0], "dust_txt": dust[1], "ultra_dust": ultradust[0],
                "ultra_dust_txt": ultradust[1], "ozone": ozone[0], "ozone_text": ozone[1]}

    @staticmethod
    def somanytemp(soup):
        todaytemperature = str(soup.find('p', class_='info_temperature').find('span', class_='todaytemp')).text + '도'
        tempdata = soup.find('ul', class_='info_list').find('span', class_='merge')
        lowtemperature = str(tempdata.find('span', class_='min').find('span', class_='num').text) + '도'
        hightemperature = str(tempdata.find('span', class_='max').find('span', class_='num').text) + '도'
        return {"temp": todaytemperature, "lowtemp": lowtemperature, "hightemp": hightemperature}

    @staticmethod
    def getdust(soup):
        misaemungi = soup.find('dl', class_='indicator').find_all('dd')[
            0].find('span', class_='num').text
        misaemungitext = soup.find('dl', class_='indicator').find_all('dd')[0]
        misaemungitext = remove_special_region(misaemungitext, 'span').text
        return [misaemungi, misaemungitext]

    @staticmethod
    def getultradust(soup):
        chomisaemungi = soup.find('dl', class_='indicator').find_all('dd')[
            1].find('span', class_='num').text
        chomisaemungitext = soup.find(
            'dl', class_='indicator').find_all('dd')[1]
        chomisaemungitext = remove_special_region(
            chomisaemungitext, 'span').text
        return [chomisaemungi, chomisaemungitext]

    @staticmethod
    def getozone(soup):
        ozone = soup.find('dl', class_='indicator').find_all('dd')[
            2].find('span', class_='num').text
        ozonetext = soup.find('dl', class_='indicator').find_all('dd')[2]
        ozonetext = remove_special_region(ozonetext, 'span').text
        return [ozone, ozonetext]

    @staticmethod
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
    mysql1 = connect_cursor()
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `furluckbot1`;")
    resultcursor = cursor.fetchall()
    result = cursor_to_result(resultcursor, 'id', memberid)
    if result is None:
        insertmemberdataonce(cursor=cursor, memberid=memberid)
    if not get:
        cursor.execute(
            "UPDATE furluckbot1 SET warn = %s WHERE id = %s", (amount, memberid))
    cursor.execute("SELECT * FROM `furluckbot1`;")
    resultcursor = cursor.fetchall()
    result = cursor_to_result(resultcursor, 'id', memberid)
    mysql1.close()
    return result


# noinspection PyTypeChecker
def helpingyou(memberid: int):
    mysql1 = connect_cursor()
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `furluckbot1`;")
    resultcursor = cursor.fetchall()
    result = cursor_to_result(resultcursor, 'id', memberid)
    if result is None:
        try:
            insertmemberdataonce(cursor, memberid)
        except pymysql.err.IntegrityError:
            pass
    cursor.execute("SELECT * FROM `furluckbot1`;")
    resultcursor = cursor.fetchall()
    result = cursor_to_result(resultcursor, 'id', memberid)
    mysql1.close()
    return result


def insertmemberdataonce(cursor, memberid: int):
    sql = "INSERT INTO `furluckbot1` (id, level1, warn, helpingme) VALUES (%s, 1, 0, 0)"
    cursor.execute(sql, memberid)


def insertserverdataonce(cursor, guildid: int):
    sql = "INSERT INTO `serverfurluckbot` (serverid, insaname, gongjiid, logid, recaptcha) VALUES \
    (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (guildid, 0, 0, 0, 0))


class DontHaveMoney(Exception):
    pass


class FailedDobak(Exception):
    pass


def getmoney(memberid: int):
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
        cursor_to_result(resultcursor, 'id', memberid)
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
    sub_dobak_money(result1, cursor, money, memberid)
    cursor.execute("SELECT * FROM `furluckbot1`;")
    resultcursor = cursor.fetchall()
    result1 = cursor_to_result(resultcursor, 'id', memberid)
    mysql1.close()
    return result1


def sub_dobak_money(result1, cursor, money, memberid):
    if result1 is None:
        insertmemberdataonce(cursor, memberid)
        cursor.execute("SELECT * FROM `furluckbot1`;")
        resultcursor = cursor.fetchall()
        result1 = cursor_to_result(resultcursor, 'id', memberid)
    if result1['level1'] < money:
        raise DontHaveMoney
    if secrets.SystemRandom().randint(1, 2) == 1:
        money1 = result1['level1'] - money
        cursor.execute(
            "UPDATE furluckbot1 SET level1 = %s WHERE id = %s", (money1, memberid))
        raise FailedDobak
    money1 = result1['level1'] + money
    cursor.execute(
        "UPDATE furluckbot1 SET level1 = %s WHERE id = %s", (money1, memberid))


def cursor_to_result(resultcursor, equal: str, id2):
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


def serverdata(name: str, guildid: int, modify, get: bool):
    mysql1 = connect_cursor()
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `serverfurluckbot`;")
    resultcursor = cursor.fetchall()
    result = cursor_to_result(resultcursor, 'serverid', guildid)
    if result is None:
        insertserverdataonce(cursor, guildid)
    if not get:
        executecommand = "UPDATE serverfurluckbot SET %s = %s WHERE serverid = %s"
        if name == 'recaptcha':
            executecommand = "UPDATE serverfurluckbot SET recaptcha = %s WHERE serverid = %s"
            cursor.execute(executecommand, (modify, guildid))
        else:
            cursor.execute(executecommand, (name, modify, guildid))
    cursor.execute("SELECT * FROM `serverfurluckbot`;")
    resultcursor = cursor.fetchall()
    try:
        result = cursor_to_result(resultcursor, 'serverid', guildid)
    except KeyError as e:
        if not get:
            raise KeyError(e)
    mysql1.close()
    return result


def noticeusingbot(guildid: int, channelid: int, get: bool):
    mysql1 = connect_cursor()
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `serverfurluckbot`;")
    resultcursor = cursor.fetchall()
    result1 = cursor_to_result(resultcursor, 'id', guildid)
    if result1 is None:
        insertserverdataonce(cursor, guildid)
    if not get:
        cursor.execute(
            "UPDATE serverfurluckbot SET gongjiid = %s WHERE serverid = %s", (channelid, guildid))
    cursor.execute("SELECT * FROM `serverfurluckbot`;")
    resultcursor = cursor.fetchall()
    mysql1.close()
    return resultcursor


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
        self.voteid = hashlib.sha3_512(
            str(secrets.SystemRandom().randint(1, 10000000)).encode('utf-8')).hexdigest()
        self.mysql = connect_cursor()
        self.cursor = self.mysql.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute("SELECT * FROM `votes`")
        resultcursor = self.cursor.fetchall()
        self.set_key(resultcursor)
        self.cursor.execute("INSERT INTO `votes` (voteid, result1, bot) VALUES (%s, %s, %s)",
                            (self.voteid, 1233, self.voteid))

    def add_vote(self, opinion: bool, interid: int):
        if opinion:
            self.cursor.execute(
                "INSERT INTO `votes` (voteid, bot, result1) VALUES (%s, %s, %s) ON DUPLICATE KEY \
                UPDATE bot=%s, result1=%s",
                (self.voteid, self.voteid + str(interid), 0, self.voteid + str(interid), 0))
        else:
            self.cursor.execute(
                "INSERT INTO `votes` (voteid, bot, result1) VALUES (%s, %s, %s) ON DUPLICATE KEY \
                UPDATE bot=%s, result1=%s",
                (self.voteid, self.voteid + str(interid), 1, self.voteid + str(interid), 1))

    def set_key(self, resultcursor):
        for i1 in resultcursor:
            resultid = i1['voteid']
            if resultid == self.voteid:
                self.voteid = hashlib.sha3_512(
                    str(secrets.SystemRandom().randint(1, 10000000)).encode('utf-8')).hexdigest()

    def close(self):  # sourcery no-metrics
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
        regular = True

        for i2 in self.rankrecord.keys():
            dictlol = self.detectdict[i2]
            ranks = self.ranks(dictlol)
            vip = ranks["vip"]
            vip_plus = ranks["vip_plus"]
            mvp = ranks["mvp"]
            mvp_plus = ranks["mvp_plus"]
            self.rankrecord[i2] = HypixelRank(
                regular, vip, vip_plus, mvp, mvp_plus)

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

    def ranks(self, dictlol: dict):
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
        return {"vip": vip, "vip_plus": vip_plus, "mvp": mvp, "mvp_plus": mvp_plus}

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
        response = requests.get(
            f"https://api.mojang.com/users/profiles/minecraft/{playername}")
        if response.status_code == 204:
            raise UsernameNotValid("username is not valid:", playername)
        self.playername = playername

    def get_response(self, get: str):
        params = {'key': hypixel_api_key, 'name': self.playername}
        if get.find("/") == -1:
            get = "/" + get
        response = requests.get(f"https://api.hypixel.net{get}", params)
        if response.status_code != 200 and json.loads(response.content)["cause"] == "You have already looked up this \
                                                                                     name recently":
            raise YouAlreadylookedupthisnamerecently("yes it's error")
        if response.status_code == 429:
            raise KeyLimit("Key Limit Exceed")
        return json.loads(response.content)

    def get_information(self):
        response = self.get_response("/player")
        if response is False:
            return False
        return Information(response['player'])

    def get_rankhistory(self):
        response = self.get_response("/player")
        if response is False:
            return False
        return HypixelRankHistory(response["player"]["monthlycrates"]).rankhistory

    def get_online(self, response: Information = None):
        if response is None:
            response = self.get_information()
        if response is False:
            return None
        return bool(response.lastlogin > response.lastlogout)


def rankhistorycomponents(response):
    components = SelectMenu(
        custom_id="rankhistory", placeholder="보고 싶은 날짜를 골라주세요.", max_values=len(response))
    for key in response.keys():
        components.add_option(label=key, value=key,
                              description=f"{key} 날짜의 기록을 보여줍니다.")
    return components


def rankhistoryembed(labels, response, name):
    embed = discord.Embed(name=f"{name}의 랭크 기록")
    for i2 in labels:
        value: HypixelRank = response[i2]
        if value.mvp_plus:
            value1 = "일반, VIP, VIP+, MVP, MVP+"
        elif value.mvp:
            value1 = "일반, VIP, VIP+, MVP"
        elif value.vip_plus:
            value1 = "일반, VIP, VIP+"
        elif value.vip:
            value1 = "일반, VIP"
        else:
            value1 = "일반"
        embed.add_field(name=i2, value=value1)
    return embed


async def except_error_information(inter: SlashInteraction, name):
    response = None
    response2 = None
    try:
        response: Information = HypixelAPI(playername=name).get_information()
        response2: bool or None = HypixelAPI(
            playername=name).get_online(response)
    except UsernameNotValid:
        await inter.edit("유저의 이름이 알맞지 않습니다.")
    except YouAlreadylookedupthisnamerecently:
        await inter.edit("이 플레이어를 최근에 누군가 검색했습니다.")
    except KeyLimit:
        await inter.edit("1분에 120번 이상 API를 사용했습니다. 잠시만 기다려주세요.")
    except Exception as e:
        await inter.edit("클라이언트 안에서 알 수 없는 에러가 났습니다.")
        raise e
    return Responses(response, response2)


class Responses:
    def __init__(self, response, response2):
        self.response1 = response
        self.response21 = response2

    @property
    def responses1(self):
        yield self.response1
        yield self.response21


async def except_error_history(inter: SlashInteraction, name: str):
    response = None
    try:
        response: Information = HypixelAPI(playername=name).get_rankhistory()
    except UsernameNotValid:
        await inter.edit("유저의 이름이 알맞지 않습니다.")
    except YouAlreadylookedupthisnamerecently:
        await inter.edit("이 플레이어를 최근에 누군가 검색했습니다.")
    except KeyLimit:
        await inter.edit("1분에 120번 이상 API를 사용했습니다. 잠시만 기다려주세요.")
    except Exception as e:
        await inter.edit("클라이언트 안에서 알 수 없는 에러가 났습니다.")
        raise e
    else:
        if response is False:
            await inter.edit("서버 안에서 알 수 없는 에러가 났습니다.")
            return False
    return response


def create_player_embed(name, response, response2):
    responseonline = None
    if response2:
        responseonline = "온라인"
    elif response2 is not True:
        responseonline = "오프라인"
    embed = discord.Embed(title="플레이어 정보", description=f"플레이어 이름 : {name}")
    embed.add_field(name="부여 받은 랭크", value=response.rank)
    embed.add_field(name="돈으로 산 랭크", value=str(
        response.packagerank).replace('PLUS', '+').replace('_', ''))
    embed.add_field(name="처음 로그인한 일자", value=str(response.firstlogin))
    embed.add_field(name="마지막으로 로그인한 일자", value=str(response.lastlogin))
    embed.add_field(name="마지막으로 로그아웃한 일자", value=str(response.lastlogout))
    embed.add_field(name="현재 온라인 여부", value=str(responseonline))


def get_helping_rank(helpingyouandme, id2):
    helpingrank = None
    if id2 == 338902243476635650:
        helpingrank = "나를 만들어 준 너"
    elif helpingyouandme == 0:
        helpingrank = "이용을 해주는 너"
    elif 0 < helpingyouandme < 100:
        helpingrank = "조금이라도 도와주는 너"
    return helpingrank


def get_message_edit_embed(before, after):
    embed1 = discord.Embed(name="메시지가 변경되었어요!")
    embed1.add_field(name="변경되기 전 메시지의 콘텐츠",
                     value=before.content, inline=False)
    embed1.add_field(name="변경된 후 메시지의 콘텐츠", value=after.content, inline=False)
    embed1.add_field(name="메시지를 변경한 사람",
                     value=f"<@{after.author.id}>", inline=False)
    embed1.set_footer(text=todaycalculate())


async def vote_listener(on_click: ClickListener, votelol, embed, inter):
    # noinspection PyShadowingNames
    @on_click.matching_id('accept')
    async def _accept(inter):
        votelol.add_vote(True, inter.author.id)
        await inter.reply(content="투표가 완료되었습니다!", ephemeral=True)

    # noinspection PyShadowingNames
    @on_click.matching_id('deny')
    async def _deny(inter):
        votelol.add_vote(False, inter.author.id)
        await inter.reply(content="투표가 완료되었습니다!", ephemeral=True)

    # noinspection PyShadowingNames
    @on_click.timeout
    async def _timeout():
        result = votelol.close()
        trueopinion = result['true']
        falseopinion = result['false']
        embed.add_field(name="O", value=trueopinion)
        embed.add_field(name="X", value=falseopinion)
        await inter.edit(embed=embed, components=[])


def get_warn_message(reason, memberid, authorid, warndata):
    if reason is None:
        return f"<@{memberid}>님은 <@{authorid}>에 의해서 주의를 받았어요! 현재 주의 개수는 {warndata['warn']}개에요!"
    return f"<@{memberid}>님은 {reason}이라는 이유로 <@{authorid}>에 의해서 주의를 받았어요! 현재 주의 개수는 {warndata['warn']}개에요!"


def get_unwarn_message(reason, memberid, authorid, warndata):
    if reason is None:
        return f"<@{memberid}>님은 <@{authorid}>에 의해서 주의가 없어졌어요! 현재 주의 개수는 {warndata['warn']}개에요!"
    return f"<@{memberid}>님은 {reason}이라는 이유로 <@{authorid}>에 의해서 주의가 없어졌어요! 현재 주의 개수는 {warndata['warn']}개에요!"


def make_embed_bot_information(inter: SlashInteraction, cpuinfo1, ping, client: commands.Bot):
    embed1 = md2.cpuandram(inter, cpuinfo1)
    embed1.add_field(name="파이썬 버전", value=cpuinfo1["python_version"])
    embed1.add_field(name="봇 핑(ms)", value=str(ping))
    embed1.add_field(name="API 핑(ms)", value=str(round(client.latency * 1000)))
    return embed1


async def get_guilds(guildid, client: commands.Bot, inter):
    try:
        guildid = int(guildid)
        guild: discord.Guild = client.get_guild(guildid)
        if guild is None:
            raise AttributeError
    except (AttributeError, discord.errors.HTTPException, ValueError):
        await inter.edit(content="그 서버는 잘못된 서버거나 제가 참여하지 않은 서버인 것 같아요!")
    else:
        return guild


def make_guildinfo_embed(guild, inter):
    embed1 = discord.Embed(name="서버의 정보", description=f"{guild.name}의 정보에요!")
    embed1.add_field(name="길드의 부스트 티어", value=guild.premium_tier)
    embed1.add_field(name="길드의 부스트 개수",
                     value=f"{guild.premium_subscription_count}개")
    embed1.add_field(name="길드 멤버 수(봇 포함)", value=f"{len(guild.members)}명")
    embed1.add_field(name="실제 길드 멤버 수",
                     value=f"{len([m for m in guild.members if not m.bot])}명")
    embed1.set_thumbnail(url=guild.icon_url)
    embed1.set_author(name=inter.author.name, icon_url=inter.author.avatar_url)
    embed1.set_footer(text=todaycalculate())
    return embed1


async def mute_command(role1: discord.Role or None, inter: SlashInteraction, member=discord.Member, reason=str or None):
    if role1 is None:
        perms1 = discord.Permissions(
            add_reactions=False, create_instant_invite=False, send_messages=False, speak=False)
        role1 = await inter.guild.create_role(name="뮤트", permissions=perms1)
    await member.add_roles(role1, reason=reason)
    if reason is None:
        await inter.reply(f"<@{inter.author.id}>님이 <@{member.id}>님을 뮤트하였습니다!")
    else:
        await inter.reply(f"<@{inter.author.id}>님이 {reason}이라는 이유로 <@{member.id}>님을 뮤트하였습니다!")


def auth(memberid: int, recentcontentmsg: str):
    mysql1 = connect_cursor()
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `auth`;")
    resultcursor = cursor.fetchall()
    result = cursor_to_result(resultcursor, 'id', memberid)
    cursor.close()
    return result is not None and recentcontentmsg == result["key"]


async def auth_recaptcha(member: discord.Member, getchannel: tuple):
    successauth = None
    channel: discord.DMChannel = await member.create_dm()
    msgcontent = f"이 링크에서 인증해서 key를 채팅에 쳐주세요! https://book.chizstudio.com/?id={member.id}"
    msgcontent2 = " (이 링크는 10분동안만 가능합니다. 10분이 지날 시 나갔다 들어오면 다시 하실 수 있습니다."
    await channel.send(content=(msgcontent + msgcontent2))
    rollin: discord.Role = member.guild.get_role(getchannel["recaptcha"])
    for _i in range(600):
        async for msg2 in channel.history(limit=1):
            if auth(member.id, msg2.content) is True:
                await member.add_roles(rollin)
                await channel.send("인증이 완료되었습니다!")
                successauth = True
        time.sleep(1)
        if successauth:
            break
    if successauth is None:
        await channel.send("인증 시간이 만료되었습니다. 재입장을 추천드립니다.")
