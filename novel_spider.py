from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
import os
from os import path
from bs4 import BeautifulSoup
import requests


Chromedriver_path = path.join(path.dirname(__file__), 'chromedriver.exe')
novel_folder = path.join(path.dirname(__file__), '88dus各种网文合集')
folder = os.path.exists(novel_folder)
browser = webdriver.Chrome(Chromedriver_path)
wait = Wait(browser, 10)

if not folder:
    os.makedirs(novel_folder)
    filedir_path = novel_folder
else:
    filedir_path = novel_folder

bookurl = []
booknames = []


class Downloadworker(Thread):
    def __init__(self, i):
        Thread.__init__(self)
        self.i = i

    def run(self):
        count = 1
        current_url = bookurls[self.i]
        while True:
            try:
                page1 = requests.get(current_url)
                page1.encoding = ('GBK')
                html = page1.text
                soup = BeautifulSoup(html, 'lxml')
                content = soup.select('body div.novel div.yd_text2')
                contentr = content[0].text.replace('^_^', '')
                filename = path.join(filedir_path, booknames[self.i] + '.txt')
                if os.path.exists(filename):
                    with open(filename, 'a', encoding='UTF-8') as f:
                        f.write(contentr)
                else:
                    with open(filename, 'w', encoding='UTF-8') as f:
                        f.write(contentr)
                next_page = soup.select('body div.novel div.pereview a')[-1]['href']
                count += 1
                if next_page == 'index.html':
                    print(booknames[self.i] + '爬取完毕')
                    break
                next_url = bookurl[self.i] + next_page
                current_url = next_url
            except Exception as hg:
                print(booknames[self.i] + '爬取失败')
                print(str(hg))
                break


for page in range(1, 149):
    catalog = requests.get(f'https://www.88dus.com/top/fullflag/{page}/')
    catalog.encoding = ('GBK')
    html = catalog.text
    soup = BeautifulSoup(html, 'lxml')
    book_list = soup.body.find('div', class_="booklist")
    booklist1 = book_list.ul.find_all('li')
    for i in range(len(booklist1)):
        try:
            url = booklist1[i].span.a["href"]
            bookurl.append('https://www.88dus.com' + url)
            bookname = booklist1[i].span.a.b.string
            booknames.append(bookname)
        except Exception as e:
            print(e)
loop_count = 0
loop_range = len(bookurl) // 10
loop_end = loop_range
for loop in range(9):
    bookurls = []
    for i in range(loop_count, loop_end):
        browser.get(bookurl[i])
        print(f'绕过动态加载 记录{booknames[i]}爬取地址...')
        mulu = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "body div.mulu ul li a")
            )
        )
        mulu = browser.find_elements_by_css_selector("body div.mulu ul li a")
        current_url = mulu[0].get_attribute("href")
        bookurls.append(current_url)
    loop_count += loop_range
    loop_end += loop_range

    print(bookurls)

    Thread_list = []
    for i in range(len(bookurls)):
        if __name__ == '__main__':
            th = Downloadworker(i)
            th.start()
            Thread_list.append(th)
    for i in Thread_list:
        i.join()