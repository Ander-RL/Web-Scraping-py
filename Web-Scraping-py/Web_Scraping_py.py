from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import json

url = "https://www.pccomponentes.com/amd-ryzen-5-5600x-37ghz"

# Open the URL as Browser, not as python urllib to avoid Forbidden errors
page = urllib.request.Request(url,headers={'User-Agent': 'Chrome'}) 
html = urllib.request.urlopen(page).read()

soup = BeautifulSoup(html, features="lxml") # lxml helps to interpret the html

tag_sections = soup.find_all("div", class_="precioMain h1")
for section in tag_sections:
    print(section)

print("\nPrecio:",tag_sections[0].text)

print("\n=========================================================================\n")

tag_comprar = soup.find("button", class_="btn js-article-buy btn-primary btn-lg buy GTM-addToCart buy-button")
print(tag_comprar.text)

lista_comprar = (tag_comprar.text).split()
if "Comprar" in lista_comprar: print("Disponible")