from selenium import webdriver
from bs4 import BeautifulSoup
import os, time

os.chdir(r'c:\users\chs\desktop\new\win')
driver = webdriver.Chrome(r'C:\Users\chs\chromedriver_win32\chromedriver.exe')
driver.get('https://wwin.com/bs/sports/#2/0/0/0/')
time.sleep(5)
""" NAREDNIH 5LINIJA KODA SU ZA SLEDECI DAN!!
link = driver.find_element_by_xpath('//*[@id="Weak342019"]/span[1]')
link.click()
time.sleep(5)
fudbal = driver.find_element_by_xpath('//*[@id="v_m_sportovi"]/tbody/tr[2]/th/div[1]/table/tbody/tr/td[1]/a')
fudbal.click()
time.sleep(5)
"""
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
time.sleep(5)
#pravimo set naziva utakmica
wwin_nazivi_liga=set()
html = driver.page_source
content = BeautifulSoup(html, 'lxml')
body = content.find('div',{'id':'ContentBody_ctl01_ucOffer_ucOdds_fullPonuda'})
lige = body.find_all('div',{'class':'liga 2'})
for liga in lige:
    naziv1 = liga.find('span',{'class':'naslov_lige'})
    if naziv1:
        naziv1 = naziv1.text[0:(len(naziv1.text)-1)]
        if naziv1 not in wwin_nazivi_liga:
            wwin_nazivi_liga.add(naziv1)
        else:
            a = naziv1
            for i in range(2,10):
                naziv1 = a
                naziv1 = naziv1 + str(i)
                if naziv1 in wwin_nazivi_liga:
                    continue
                else:
                    wwin_nazivi_liga.add(naziv1)
                    break
    with open(naziv1 + '.txt', 'w')as f:
        if liga.find('table',{'class':'parovi'}) == None:
            continue
        else:
            parovi =liga.find('table',{'class':'parovi'})
        utakmice = parovi.find_all('td',{'class':'parPar'})
        kvote = parovi.find_all('td',{'class':'tgp'})
        x = 0
        new = []
        for i in range(len(utakmice)):
            try:
                print(utakmice[i].text, kvote[x].text, kvote[x+4].text)
                new.append([utakmice[i].text, kvote[x].text, kvote[x+4].text])
            except IndexError:
                continue
            x += 6
        new = sorted(new)
        for i in range(len(new)):
            f.write(' '.join(new[i]) + '\n')
