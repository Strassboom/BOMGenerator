import requests
from lxml import html
import os
import sys
sys.path.append("..")

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}

def adafruitScrape(link):
    link = link.strip()
    response = requests.get(link,headers=header)
    root = html.fromstring(response.content)
    name = root.xpath('//h1[@class="products_name"]/text()')[0].strip()
    price = root.xpath('//div[@class="product-price"]/span/text()')[0].strip("$")
    info = {"Name":name,"Price":price,"URL":link}
    info = [name,price,link]
    return info

def amazonScrape(link):
    link = link.strip()
    response = requests.get(link,headers=header)
    root = html.fromstring(response.content)
    name = root.xpath('//span[@id="productTitle"]/text()')[0].strip()
    leftDecPrice = root.xpath('//span[@class="price-large"]/text()')[0].strip()
    rightDecPrice = root.xpath('//span[@class="a-size-small price-info-superscript"]/text()')[1].strip()
    price = "{}.{}".format(leftDecPrice,rightDecPrice)
    info = {"Name":name,"Price":price,"URL":link}
    info = [name,price,link]
    return info

def scrapePartData(srcFile):
    with open(srcFile,"r") as r:
        linkList = r.readlines()
    for item in range(len(linkList)):
        if "https://www.amazon.com/" in linkList[item]:
            linkList[item] = amazonScrape(linkList[item])
        elif "https://www.adafruit.com/" in linkList[item]:
            linkList[item] = adafruitScrape(linkList[item])
    return linkList
        

def defaultFile():
    filelist = ["data/"+item for item in os.listdir("data")]
    return filelist[0]