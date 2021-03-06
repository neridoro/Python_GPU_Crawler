from selenium import webdriver
import telegram_send
import time

def start_page(chrome):
    url = 'https://www.newegg.com/global/il-en/'
    chrome.get(url)
    k = chrome.find_element_by_id("app").find_element_by_partial_link_text("RTX30")
    return k.get_attribute('href')

def email(item):
    telegram_send.send(messages=item)

def refresh(chrome, url):
    chrome.get(url)
    info = chrome.find_elements_by_class_name('item-info')
    price = chrome.find_elements_by_class_name('price-current')
    href = chrome.find_elements_by_class_name('item-img')
    x=0
    for x in range(0,len(info)):
        text=info[x].text
        niceprice=str(price[x].text).split("₪")[1].replace(",","").split(" ")[0]
        if "OUT OF STOCK" not in (text):
            if "3060 Ti" in text:
                email(["3060 Ti",price[x].text,href[x].get_attribute('href')])
            if "3060" in text and float(niceprice)<3000:
                email(["3060",price[x].text,href[x].get_attribute('href')])
            if "3070" in text and float(niceprice)<4000:
                email(["3070",price[x].text,href[x].get_attribute('href')])
            if "3080" in text and float(niceprice)<5000:
                email(["3080",price[x].text,href[x].get_attribute('href')])

driver = webdriver.Chrome()
while(True):
    try:

        alert=refresh(driver,'https://www.newegg.com/global/il-en/p/pl?d=rtx&N=101613484&PageSize=60')
        time.sleep(6)
    except Exception as e: print(e)
