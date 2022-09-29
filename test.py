from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
from dfk_bot import *

world_floor = 55
anti_spam = []

def not_spam(id):
    global anti_spam
    if(id in anti_spam):
        return False
    else:
        anti_spam.append(id)
        return True

def display_hero_setup(hero_data):
    id = hero_data[0]
    cost = hero_data[1]
    description = cost + "J"
    main = hero_data[2]
    sub = hero_data[3]
    header = id + '-' + main + '/' + sub
    split_sub = sub.split('/')[1]
    sub = split_sub.split('(')[0]
    job = hero_data[4].split('/')[0]
    job_percent = hero_data[5]
    job = job + "-" + job_percent
    rarity = hero_data[8]
    if(rarity == 'C'):
        rarity = "Common"
    if(rarity == 'U'):
        rarity = "Uncommon"
    if(rarity == 'R'):
        rarity = "Rare"
    if(rarity == 'L'):
        rarity = "Legendary"
    if(rarity == 'M'):
        rarity = "Mythic"
    level = hero_data[9]
    gen = hero_data[10]
    summons = hero_data[11]
    stat_boost1 = hero_data[12]
    stat_boost2 = hero_data[13]
    boosts = stat_boost1 + '/' + stat_boost2
    transaction_started = hero_data[16]

    display_data = [header, description, job, rarity, boosts, level, gen, summons]

    if(not_spam(id)):
        return display_data
    



def analyze_hero(hero_data):
    global world_floor

    id = hero_data[0]
    cost = hero_data[1]
    main = hero_data[2]
    sub = hero_data[3]
    split_sub = sub.split('/')[1]
    sub = split_sub.split('(')[0]
    job = hero_data[4].split('/')[0]
    job_percent = hero_data[5]
    rarity = hero_data[8]
    if(rarity == 'C'):
        rarity = "Common"
    if(rarity == 'U'):
        rarity = "Uncommon"
    if(rarity == 'R'):
        rarity = "Rare"
    if(rarity == 'L'):
        rarity = "Legendary"
    if(rarity == 'M'):
        rarity = "Mythic"
    level = hero_data[9]
    gen = hero_data[10]
    summons = hero_data[11]
    stat_boost1 = hero_data[12]
    stat_boost2 = hero_data[13]
    transaction_started = hero_data[16]

    if(float(cost) < world_floor):
        hero_data.append("FLOOR LISTING")
        display_hero_setup(hero_data)



def testif():
    return "testing"
    

#gets data 
def make_data():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    url = 'https://dfktavern.com/saleAuction-alert'

    wd = webdriver.Chrome('chromedriver', options=options)
    wd.get(url)
    time.sleep(5)
    try:
        html = wd.page_source

        df = pd.read_html(html)
        df_string = str(df)
        df_list = df_string.splitlines()
        df_list.pop(0)
        for hero in df_list:
            hero_data = hero.split()
            hero_data.pop(0)
            if(hero_data[0] != 'HeroID'):
                analyze_hero(hero_data)
        wd.close()
    except: 
        print("error")

