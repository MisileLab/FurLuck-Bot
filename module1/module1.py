from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
from bitlyshortener import Shortener
import requests
import json
import pymysql

count = 0
tokens_pool2 = []

with open('bitlytoken.txt') as f:
    tokens_pool = f.readlines()
    print(tokens_pool)
for i in range(len(tokens_pool)):
    print(i)
    tokens_pool2.append(str(tokens_pool[count]).replace('\n', ''))
    count = count + 1
print(tokens_pool2)

mysqlconnect = open('pymysql.json', 'r').read()
mysqlconnect = json.loads(mysqlconnect)

def todaycalculate():
    datetimetoday = datetime.today()
    today2 = str(datetimetoday.year) + '년 ' + str(datetimetoday.month) + '월 ' + str(datetimetoday.day) + '일 ' + str(datetimetoday.hour) + '시 ' + str(datetimetoday.minute) + '분 ' + str(datetimetoday.second) + '초 '
    return today2

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
        list1 = {
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
        return list1

def remove_special_region(origin, tagname):
    for x in origin(tagname):
        try:
            x.decompose()
        except AttributeError:
            pass
    return origin

def shortlink(link):
    shortener = Shortener(tokens=tokens_pool2, max_cache_size=256)
    link1 = shortener.shorten_urls(long_urls=link)
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
        result = i1
        resultid = i1['id']
        if resultid == memberid:
            break
    if result is None:
        sql = "INSERT INTO `furluckbot1` (id, level1, warn) VALUES (%i, 1, 0)" % memberid
        cursor.execute(sql)
    if get is True:
        pass
    elif get is False:
        sql = "UPDATE furluckbot1 SET warn = %i WHERE id = %i" % (amount, memberid)
        cursor.execute(sql)
    sql = "SELECT * FROM `furluckbot1`;"
    cursor.execute(sql)
    resultcursor = cursor.fetchall()
    result = None
    for i1 in resultcursor:
        result = i1
        resultid = i1['id']
        if resultid == memberid:
            break
    mysql1.close()
    return result

# noinspection PyTypeChecker
def sayhellotoyourmember(guildid:int, channelid:int, get:bool):
    mysql1 = pymysql.connect(user=mysqlconnect["user"], passwd=mysqlconnect["password"], host=mysqlconnect["host"], db=mysqlconnect["db"], charset=mysqlconnect["charset"], port=mysqlconnect["port"], autocommit=True)
    cursor = mysql1.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM `serverfurluckbot`;"
    cursor.execute(sql)
    resultcursor = cursor.fetchall()
    result = None
    for i1 in resultcursor:
        result = i1
        resultid = i1['serverid']
        if resultid == guildid:
            break
    if result is None:
        sql = "INSERT INTO `serverfurluckbot` (serverid, insaname) VALUES (%i, %i)" % (guildid, channelid)
        cursor.execute(sql)
    if get is True:
        pass
    elif get is False:
        sql = "UPDATE serverfurluckbot SET insaname = %i WHERE serverid = %i" % (channelid, guildid)
        cursor.execute(sql)
    sql = "SELECT * FROM `serverfurluckbot`;"
    cursor.execute(sql)
    resultcursor = cursor.fetchall()
    result = None
    try:
        for i1 in resultcursor:
            result = i1
            resultid = i1['serverid']
            if resultid == guildid:
                break
    except KeyError as e:
        if get is True:
            pass
        elif get is False:
            raise KeyError(e)
    mysql1.close()
    return result