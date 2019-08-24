import requests
from lxml import html
import os
import sys
sys.path.append("..")

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}

def adafruitScrape(link):
    response = requests.get(link,headers=header)
    root = html.fromstring(response.content)
    name = root.xpath('//h1[@class="products_name"]/text()')[0].strip()
    price = root.xpath('//div[@class="product-price"]/span/text()')[0].strip("$")
    info = [name,price]
    print([data for data in info])
    return info

def amazonScrape(link):
    response = requests.get(link,headers=header)
    root = html.fromstring(response.content)
    name = root.xpath('//span[@id="productTitle"]/text()')[0].strip()
    leftDecPrice = root.xpath('//span[@class="price-large"]/text()')[0].strip()
    rightDecPrice = root.xpath('//span[@class="a-size-small price-info-superscript"]/text()')[1].strip()
    price = "{}.{}".format(leftDecPrice,rightDecPrice)
    info = [name,price]
    print([data for data in info])

def scrapePartData(srcFile):
    with open(srcFile,"r") as r:
        linklist = r.readlines()
    for item in linklist:
        print(item)
        if "https://www.amazon.com/" in item:
            amazonScrape(item)
        elif "https://www.adafruit.com/" in item:
            adafruitScrape(item)

def defaultFile():
    filelist = ["data/"+item for item in os.listdir("data")]
    scrapePartData(filelist[0])
defaultFile()