#Cargamos las librerías necesarias
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError

#Creamos una función para la gestión de errores

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


#Identificamos la url que vamos a rastrear
str = "https://supermercado.eroski.es/es/supermercado/SinGluten/"


title = getTitle(str)
if title == None:
    print("Title could not be found")
else:
    print(title)
#podríamos meter en el else toda la lógica
    
#html = urlopen("https://supermercado.eroski.es/es/login/delivery/?zipCode=48901")
#urlpage = 'https://supermercado.eroski.es/es/supermercado/SinGluten/'

#Esto de abajo lo tendremos que meter en una función

page = requests.get(str).text #recuperamos la información correspondiente a la respuesta de la petición

#Parseamos el html
soup = BeautifulSoup(page, "html.parser")

#bsObj = BeautifulSoup(page, 'lxml')
#print(bsObj)

#Extraer el texto de la etiqueta
nameList = soup.findAll("div", {"class":"product-description"})

data = []
for name in nameList:
    title = name.find("h2", {"class":"product-title product-title-resp"}).text
    product_name = title.split(',')[0] #Nos devuelve el nombre sin el peso (Filetes de lomo adobado de cerdo extrafino EROSKI)
    product_quantity = title.split(' ',1)[1].split(',')[1].strip() #Nos devuelve la cantidad (bandeja 300 g)
    #Sacar el valor nutricional
    #quantity_product = name.find("span", {"class":"quantity-product"}).text
    #price_product = name.find("span", {"class":"price-product"}).text
    #Rating - número valoraciones usuarios
    rating = name.find("div", {"class":"ratingSubtitle"}).get_text()
    price_before = name.find("span", {"class":"price-before"}).get_text() 
    price_now = name.find("span", {"class":"price-now"}).get_text() 
    #print(name.get_text())
    #append dict to array
    data.append({"articulo" : title, "Nombre" : product_name, "Camtidad" : product_quantity, "valoracion" : rating, 
                 "precio_antes": price_before, "precio_actual" : price_now})
    print(title, rating, price_before, price_now)
    
print (data)    

#ProductInfo = soup.find("h2", {"class": "product-title product-title-resp"}).text
#print(ProductInfo) 

#<a href="/es/productdetail/14085807-filetes-de-lomo-adobado-de-cerdo-extrafino-eroski-bandeja-300-g/">Filetes de lomo adobado de cerdo extrafino EROSKI, bandeja 300 g</a>

#<h2 class="product-title product-title-resp">
#				<a href="/es/productdetail/20110177-carne-picada-de-ternera-eusko-label-seleqtia-bandeja-500-g/">
#					Filetes de lomo adobado de cerdo extrafino EROSKI, bandeja 300 g
#				</a>
#			</h2>

#Filetes de lomo adobado de cerdo extrafino EROSKI, bandeja 300 g
#
#

#ProductName = ProductInfo.split(',')[0]  #Nos devuelve el nombre sin el peso (Filetes de lomo adobado de cerdo extrafino EROSKI)
#ProductQuantity = ProductInfo.split(' ',1)[1].split(',')[1].strip() #Nos devuelve la cantidad (bandeja 300 g)
