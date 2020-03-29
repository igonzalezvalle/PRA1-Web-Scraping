import requests
from bs4 import BeautifulSoup

str = "https://supermercado.eroski.es/es/supermercado/SinGluten/"

#Esto de abajo lo tendremos que meter en una función

page = requests.get(str) #recuperamos la información correspondiente a la respuesta de la petición
#page es un objeto. Sus atributos son:
# - page.status_code: código HTTP devuelto por el servidor
# - page.content: contenido en bruto de la respuesta del servidor

soup = BeautifulSoup(page.content)
