from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.common.exceptions import TimeoutException
import re
from bs4 import BeautifulSoup
#千万不要用XPATH去选择，它会固定选择具体的一项，用CSS去选比较好。

brower = webdriver.Chrome()
url = 'https://www.taobao.com'
brower.get(url)
wait = WebDriverWait(brower,10)

def get_nextpage(page):
    try:
        input = wait.until(Ec.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))
        botton = wait.until(Ec.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page)
        botton.click()
        wait.until(Ec.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page)))
        get_product()
    except TimeoutException:
        get_nextpage(page)

def get_pagenum(keyword):
    try:
        input = wait.until(Ec.presence_of_element_located((By.ID,'q')))
        input.send_keys(keyword)
        botton = wait.until(Ec.presence_of_element_located((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        botton.click()
        page = brower.find_element(By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total').text
        page = re.compile('(\d+)').search(page).group(1)
        get_product()
        return int(page)
    except TimeoutException:
        get_pagenum()

def get_product():
    html = brower.page_source
    doc = BeautifulSoup(html,'lxml')
    items = doc.findAll("div",attrs={"class":re.compile(r"item J_MouserOnverRe.*?")})
    for item in items:
        product = {
            'imag':items[0].find('img')['data-src'],
            'price': item.find('strong').get_text(),
            'deal': item.find(class_= 'deal-cnt').get_text(),
            'title': item.find(class_="row row-2 title").get_text(),
            'shop': item.find(class_="row row-3 g-clearfix").get_text(),
            'location': item.find(class_="location").get_text()
        }
        print(product)

def main():
    keyword = str(input("请输入搜索的关键词："))
    pageNum = get_pagenum(keyword)
    for i in range(2,pageNum+1):
        get_nextpage(i)
if __name__=='__main__':
    main()
