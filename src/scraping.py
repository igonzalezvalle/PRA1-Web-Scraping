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
    except HTTPError:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        title = bsObj.body.h2
    except AttributeError:
        return None
    return title


#Identificamos la url que vamos a rastrear
str = "https://supermercado.eroski.es/es/supermercado/SinGluten/"

# Comprobamos el acceso y sacamos el itulo de la página por pantalla
title = getTitle(str)
if title == None:
    print("Title could not be found")
else:
    print(title)
#podríamos meter en el else toda la lógica


#Creamos la función de scroll infinito (cuando llamemos a esta función recorrerá todas las páginas disponibles al hacer el scroll hacia abajo
def scroll(driver, timeout):

    last_height = driver.execute_script("return document.body.scrollHeight")
    # el tiempo de espera vendrá definido como uno de los valores de la función
    Scroll_Wait = timeout

    i=0 # contador de scroll
    while True:
        # execute script to scroll down the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(Scroll_Wait)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        i=i+1
        print ("scroll número", i)
        if new_height == last_height:
            break
        last_height = new_height
    print ("fin del scroll")


#Por si por tiempo de espera no funcionase el While, podemos forzar la lectura total con un bloque for.
#def scroll(driver, timeout):

#    for i in range (1,40):
#        # execute script to scroll down the page
#        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        # sleep
#        time.sleep(timeout)

#Utilizamos las opciones de Chrome para abrir el navegador en segundo plano
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")

driver = webdriver.Chrome("C:/chromedriver.exe", chrome_options=chrome_options) #la ruta donde tengamos el ejecutable

#Creamos una espera previa en el caso de que nos devuelva algún error dar un error
driver.implicitly_wait(100)
#abrimos la página
driver.get(str)

#Llamamos a la función de scroll con una espera entre scroll hacia abajo de 7 sg
scroll (driver, 13)

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
    #Sacar el valor nutricional. Hay que buscarlo en el texto
    #<a class="nutriscore score-c" que está un nivel por encima de donde estamos ahora
    nutrition = name.find("div", {"class":"description-text"}).parent.parent
    if nutrition.find("a", {"class":"nutriscore"})==None:
        nutrition_score = "NaN"
    else:
        nutrition = nutrition.find("a", {"class":"nutriscore"})
        nutrition_score = nutrition.get("class")[1]
   
    #Sacamos la información del producto (nombre y presentación)
    title = name.find("h2", {"class":"product-title product-title-resp"}).text
    title = title.strip()
    product_name = title.split(',')[0] #Nos devuelve el nombre sin el peso (Filetes de lomo adobado de cerdo extrafino EROSKI)
    product_name = product_name.strip()
    # product quantity es presentación del producto
    product_quantity = title.split(' ',1)[1].split(',')[1].strip() #Nos devuelve la cantidad (bandeja 300 g)
    product_quantity = product_quantity.strip()

    # Las siguientes etiquetas no se encuentran informadas en todos los casos, lo que hacemos es, 
    #en el caso de que no existan poner valos NaN y en otro caso recuperar la información
    if name.find("span", {"class":"quantity-product"})==None:
        quantity_product = "NaN"
    else:
        quantity_product = name.find("span", {"class":"quantity-product"}).text
        quantity_product = quantity_product.split(' ')[1].strip()
        
    if name.find("span", {"class":"price-product"}) == None:
        price_product = "NaN"
    else:
        price_product = name.find("span", {"class":"price-product"}).text
        price_product = price_product.split(' ')[0].replace(",",".").strip()
        
    #Rating_stats - número valoraciones usuarios
    rating_stats = name.find("div", {"class":"ratingTitle"}).span.text
    rating_stats = rating_stats.replace ("(","").replace(")","")

    #Rating - Valoración del producto
    rating = name.find("div", {"class":"ratingSubtitle"}).get_text()
    rating = rating.split('de')[0]
    rating = rating.replace(",",".").strip()
    #Porcentaje de valoración de los clientes.


    #Podemos incluir aquí las ofertas
    #En los precios tenemos que dejar únicamente el precio
    if name.find("span", {"class":"price-offer-before"})==None:
        price_before = "NaN"
    else:
        price_before = name.find("span", {"class":"price-offer-before"}).get_text()
        price_before = price_before.replace(",",".").strip()
        
    price_now = name.find("span", {"class":"price-offer-now"}).get_text() 
    price_now = price_now.replace(",",".").strip()
    #print(name.get_text())

    #append dict to array
    data.append({"Id": i, "Artículo" : title, "Nombre" : product_name, "Presentación" : product_quantity, "Valor_Nutricional" : nutrition_score, 
                 "Cantidad_Base" : quantity_product, "Precio_Unidad_Base" : price_product,"Número_Valoraciones" : rating_stats, 
                 "Valoración": rating, "Precio_Anterior": price_before, "Precio_Actual" : price_now, "Fecha_Extracción": date.today()})
    
#print (data)    


#Como último paso trasladamos los datos a un dataframe para poder volcarlos a un csv
df=pd.DataFrame(data)
df.to_csv('AlimentosSinGluten.csv', index=False, encoding='utf-8')
