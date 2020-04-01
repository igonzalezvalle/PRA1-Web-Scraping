from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import requests


def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        title = bsObj.body.h2
    except AttributeError as e:
        return None
    return title

title = getTitle("https://supermercado.eroski.es/es/supermercado/SinGluten/")
if title == None:
    print("Title could not be found")
else:
    print(title)
    
html = urlopen("https://supermercado.eroski.es/es/login/delivery/?zipCode=48901")
urlpage = 'https://supermercado.eroski.es/es/supermercado/SinGluten/'
page = requests.get(urlpage).text
bsObj = BeautifulSoup(page, 'lxml')
#print(bsObj)
#Extraer el texto de la etiqueta
nameList = bsObj.findAll("div", {"class":"product-description"})

data = []
for name in nameList:
    title = name.find("h2", {"class":"product-title product-title-resp"}).get_text()
    rating = name.find("div", {"class":"ratingSubtitle"}).get_text()
    price_before = name.find("span", {"class":"price-before"}).get_text() 
    price_now = name.find("span", {"class":"price-now"}).get_text() 
    #print(name.get_text())
    #append dict to array
    data.append({"articulo" : title, "valoracion" : rating, "precio_antes": price_before, "precio_actual" : price_now})
    print(title, rating, price_before, price_now)
    
print (data)
