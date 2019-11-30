import urllib.request, urllib.parse
import os
from pathlib import Path
from datetime import datetime

url = 'https://openreview.net/forum?id=BkggGREKvS'

response = urllib.request.urlopen(url)
webcontent = response.read().decode("utf-8")

save_path = Path("openreview_files")
os.makedirs(save_path, exist_ok=True)

with open(save_path / f'iclr_submission_forum_{datetime.now().strftime("%d-%m-%Y-%Hh:%Mm:%Ss")}_v1', 'w+') as f:
    f.write(webcontent)



# from bs4 import BeautifulSoup
# from selenium import webdriver
#
# url = "https://openreview.net/forum?id=BkggGREKvS"
# browser = webdriver.PhantomJS()
# browser.get(url)
# html = browser.page_source
# soup = BeautifulSoup(html, 'lxml')
# a = soup.find('section', 'wrapper')
# print()