import requests
from bs4 import BeautifulSoup

str = "https://supermercado.eroski.es/es/supermercado/SinGluten/"

#Esto de abajo lo tendremos que meter en una función

page = requests.get(str).text #recuperamos la información correspondiente a la respuesta de la petición

#Parseamos el html
soup = BeautifulSoup(page, "html.parser")

ProductInfo = soup.find("h2", {"class": "product-title product-title-resp"}).text
print(ProductInfo) 

#<a href="/es/productdetail/14085807-filetes-de-lomo-adobado-de-cerdo-extrafino-eroski-bandeja-300-g/">Filetes de lomo adobado de cerdo extrafino EROSKI, bandeja 300 g</a>

#<h2 class="product-title product-title-resp">
#				<a href="/es/productdetail/20110177-carne-picada-de-ternera-eusko-label-seleqtia-bandeja-500-g/">
#					Filetes de lomo adobado de cerdo extrafino EROSKI, bandeja 300 g
#				</a>
#			</h2>

#Filetes de lomo adobado de cerdo extrafino EROSKI, bandeja 300 g
#
#

ProductName = ProductInfo.split(',')[0]  #Nos devuelve el nombre sin el peso (Filetes de lomo adobado de cerdo extrafino EROSKI)
ProductQuantity = ProductInfo.split(' ',1)[1].split(',')[1].strip() #Nos devuelve la cantidad (bandeja 300 g)
