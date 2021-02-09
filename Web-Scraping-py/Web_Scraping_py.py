from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import json
from LinksReader import LinksReader

link_reader = LinksReader()
link_list = link_reader.get_link_list()
print(link_list)
print("\n=========================================================================\n")

for link in link_list:
    url = link
    print(url)
    # Open the URL as Browser, not as python urllib to avoid Forbidden errors
    page = urllib.request.Request(url,headers={'User-Agent': 'Chrome'}) 
    html = urllib.request.urlopen(page).read()

    soup = BeautifulSoup(html, features="lxml") # lxml helps to interpret the html

    tag_sections = soup.find_all("div", class_="precioMain h1")
    for section in tag_sections:
        print(section)

    print("\nPrecio:",tag_sections[0].text)

    disponible = False

    try:
        #tag_comprar = soup.find("button", class_="btn js-article-buy btn-primary btn-lg buy GTM-addToCart buy-button")
        tag_comprar = soup.find_all("button", type="button")

        for element in tag_comprar:
            if "Comprar" in element.text:
                disponible = True
            if "Avísame" in element.text:
                disponible = False

        if disponible:
           print("Disponible")

        if not disponible:
           print("No disponible")

    except Exception as e:
            print(e)

    print("\n=========================================================================\n")