#Cargamos las librerías necesarias
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import pandas as pd
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time

#Creamos una función para la gestión de errores

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
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


#Creamos la función de scroll infinito (cuando llamemos a esta función recorrerá todas las páginas disponibles al hacer el scroll hacia abajo
#def scroll(driver, timeout):

#    last_height = driver.execute_script("return document.body.scrollHeight")
#    # el tiempo de espera vendrá definido como uno de los valores de la función
#    Scroll_Wait = timeout

#    i=0 # contador de scroll
#    while True:
#        # execute script to scroll down the page
#        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
#        time.sleep(Scroll_Wait)
#        # Calculate new scroll height and compare with last scroll height
#        new_height = driver.execute_script("return document.body.scrollHeight")
#        i=i+1
#        print ("scroll número", i)
#        if new_height == last_height:
#            break
#        last_height = new_height
#    print ("fin del scroll")


def scroll(driver, timeout):

    for i in range (1,40):
        # execute script to scroll down the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        # sleep
        time.sleep(timeout)


#Identificamos el driver    
#driver = webdriver.Chrome("C:/chromedriver.exe") #la ruta donde tengamos el ejecutable

driver = webdriver.PhantomJS("C:/phantomjs.exe")

options = Options()
options.headless = True #No abrimos el navegador
#driver = webdriver.Firefox(firefox_options=options, executable_path = "C:/geckodriver.exe")

#Creamos una espera previa a dar un error
driver.implicitly_wait(100)
#abrimos la página
driver.get(str)

#Llamamos a la función de scroll
scroll (driver, 5)

#Parseamos el html resultante con toda la información
soup = BeautifulSoup(driver.page_source, "html.parser")

#cerramos el driver 
driver.close()


#Extraer el texto de la etiqueta que estamos buscando
nameList = soup.findAll("div", {"class":"product-description"})

#Inicializamos el diccionario de datos donde cargaremos la información
data = []
#recorremos todas las etiquetas para crear el dataset
for i, name in enumerate(nameList):
    title = name.find("h2", {"class":"product-title product-title-resp"}).text
    title = title.strip()
    product_name = title.split(',')[0] #Nos devuelve el nombre sin el peso (Filetes de lomo adobado de cerdo extrafino EROSKI)
    product_name = product_name.strip()
    # product quantity es presentación del producto
    product_quantity = title.split(' ',1)[1].split(',')[1].strip() #Nos devuelve la cantidad (bandeja 300 g)
    product_quantity = product_quantity.strip()
    #Sacar el valor nutricional. Hay que buscarlo en el texto
    #<a class="nutriscore score-c"
    nutrition = name.find("a", text="nutriscore score-")
    # Las siguientes etiquetas no se encuentran informadas en todos los casos, lo que hacemos es, 
    #en el caso de que no existan poner valos NaN y en otro caso recuperar la información
    if name.find("span", {"class":"quantity-product"})==None:
        quantity_product = "NaN"
    else:
        quantity_product = name.find("span", {"class":"quantity-product"}).text
        quantity_product = quantity_product.strip()
        
    if name.find("span", {"class":"price-product"}) == None:
        price_product = "NaN"
    else:
        price_product = name.find("span", {"class":"price-product"}).text
        price_product = price_product.strip()
        
    #Rating - número valoraciones usuarios
    rating = name.find("div", {"class":"ratingSubtitle"}).get_text()
    rating = rating.split('de')[0]
    rating = rating.strip()
    
    #Podemos incluir aquí las ofertas
    #En los precios tenemos que dejar únicamente el precio
    if name.find("span", {"class":"price-offer-before"})==None:
        price_before = "NaN"
    else:
        price_before = name.find("span", {"class":"price-offer-before"}).get_text()
        price_before = price_before.strip()
        
    price_now = name.find("span", {"class":"price-offer-now"}).get_text() 
    price_now = price_now.strip()
    #print(name.get_text())
    #append dict to array
    
    #Quitar retornos de carro (\n) y dejar solo precio y €. En la valoración dejar solo la puntuación
    data.append({"articulo" : title, "Nombre" : product_name, "Presentación" : product_quantity, "valor nutricional" : nutrition, 
                 "cantidad base" : quantity_product, "precio por cantidad base" : price_product,"valoracion" : rating, 
                 "precio_antes": price_before, "precio_actual" : price_now, "fecha": date.today()})
    print("%d|%s | %s|%s|%s|%s|%s|%s|%s|%s " %(i+1,title, product_name, product_quantity, nutrition, quantity_product, 
                                               price_product, rating, price_before, price_now))
    
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

#Como último paso trasladamos los datos a un dataframe para poder volcarlos a un csv
df=pd.DataFrame(data)
df.to_csv('AlimentosSinGluten.csv', index='FALSE', encoding='utf-8')
