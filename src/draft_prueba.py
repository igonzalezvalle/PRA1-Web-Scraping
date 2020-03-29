from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError


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
html2 = urlopen("https://supermercado.eroski.es/es/supermercado/SinGluten/")
bsObj = BeautifulSoup(html2)
#print(bsObj)
#Extraer el texto de la etiqueta
nameList = bsObj.findAll("div", {"class":"product-description"})
for name in nameList:
    print(name.get_text())
