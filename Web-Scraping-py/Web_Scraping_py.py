from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import json
import mysql.connector
from Db_Operations import Db_Operations
from LinksReader import LinksReader

db = Db_Operations()

try:
    # Connection to DB
    db.Connect_to_db()

    link_reader = LinksReader()
    link_list = link_reader.get_link_list()
    print("\n=========================================================================\n")

    # This code is for products of www.pccomponentes.com
    db_list = list()

    for link in link_list:
        url = link.strip()
        print(url)
        # Open the URL as Browser, not as python urllib to avoid Forbidden errors
        page = urllib.request.Request(url,headers={'User-Agent': 'Chrome'}) 
        html = urllib.request.urlopen(page).read()

        soup = BeautifulSoup(html, features="lxml") # lxml helps to interpret the html

        tag_sections = soup.find_all("div", class_="precioMain h1")
        tag_item_name = soup.find("div", class_="articulo")

        name_product = tag_item_name.text
        print(tag_item_name.text)

        price_product = tag_sections[0].text
        price_product = price_product.replace("€", " E")
        print("\nPrecio:",tag_sections[0].text)

        available = False

        try:
            tag_buy = soup.find_all("button", type="button")

            for element in tag_buy:
                if "Comprar" in element.text:
                    available = True
                if "Avísame" in element.text:
                    available = False

            if available:
                available = "Available"
                print("Available")

            if not available:
                available = "Not available"
                print("Not available")

            # Select query to check if already in table
            link_list = db.Select_url(url)

            for link in link_list:
                db_list.append(link) # Each element in the cursor is a list

            if url not in db_list:
                # Insert query to product table
                db.Insert_product(name_product, url)

                # Select query to get inserted product id into foreign key
                foreign_key = db.Select_fk(url)
                                
                # Insert query to history table
                db.Insert_history(foreign_key, name_product, price_product, available)

            else:
                # Select query to get inserted product id into foreign key
                foreign_key = db.Select_fk(url)

                # Insert query to history table
                db.Insert_history(foreign_key, name_product, price_product, available)

        except Exception as e:
            print(e)

        print("\n=========================================================================\n")

    print("Connection to database closed.")
    db.Disconnect_from_db()

except Exception as e:
    print(e)

# Write function that allows user to choose store to scrap.
# Create Scraper class.
# Scrap Steam.