from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import asyncio


world_floor = 47
anti_spam = []

def set_world_floor(value):
    global world_floor
    world_floor = value


def not_spam(id):
    global anti_spam
    if(id in anti_spam):
        return False
    else:
        anti_spam.append(id)
        return True

def analyze_hero(df_list):
    hero_list = []
    for hero in df_list:
        hero_data = hero.split()
        hero_data.pop(0)
        if(hero_data[0] != 'HeroID'):
            id = hero_data[0]
            if(not_spam(id)):
                cost = hero_data[1]
                description = cost + "J"
                main = hero_data[2]
                sub = hero_data[3]
                prof_value = sub.split('/')[0]
                prof_value = prof_value.replace("(","").replace(")","")
                split_sub = sub.split('/')[1]
                sub = split_sub.split('(')[0]
                header = id + '-' + main + '/' + sub
                job = hero_data[4].split('/')[0]
                job_percent = hero_data[5]
                job = job + "-" + job_percent
                rarity = hero_data[8]
                if(rarity == 'C'):
                    rarity = "Common"
                if(rarity == 'UN'):
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
                display_data = [header, description, job, rarity, boosts, level, gen, summons, prof_value]
                if(float(cost) < world_floor):
                    display_data.append("Under floor")
                    hero_list.append(display_data)
                    pass
                if(float(cost) < 55 and '★' in boosts and prof_value >= 100):
                    display_data.append("Potentially Underpriced")
                    hero_list.append(display_data)
                    pass

                if(main == "thief" and sub == "thief" and cost < 78):
                    display_data.append("thief/thief fisher floor")
                    hero_list.append(display_data)
                    pass

    return hero_list

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
    time.sleep(15)
    try:
        html = wd.page_source
        wd.close()
        wd.quit()
        df = pd.read_html(html)
        df_string = str(df)
        df_list = df_string.splitlines()
        df_list.pop(0)
        wd.close()
        for hero in df_list:
            hero_data = hero.split()
            hero_data.pop(0)
            if(hero_data[0] != 'HeroID'):
                return analyze_hero(df_list)
    except: 
        return 'E'


