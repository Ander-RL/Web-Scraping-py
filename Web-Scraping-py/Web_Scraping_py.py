from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import json
import mysql.connector
from LinksReader import LinksReader
from datetime import datetime

# Data to connecto to DB
HOST = "localhost"
DATABASE = "web_scraper"
USER = "root"
PASSWORD = "root"

# Todays date
today = datetime.today().strftime("%Y-%m-%d")

try:
    # Connection to DB
    print("Connecting to database...")
    conn = mysql.connector.connect(host = HOST, user = USER, password = PASSWORD, database = DATABASE)
    my_cursor = conn.cursor()
    my_cursor.execute("SET GLOBAL time_zone = '+02:00'")
    
    print("Connection succesful!")

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
            select_query = f"SELECT url_product FROM product WHERE url_product = \"{url}\""
            my_cursor.execute(select_query)

            for link in my_cursor:
                db_list.append(link[0]) # Each element in the cursor is a list

            if url not in db_list:
                # Insert query to product table
                insert_query = f"INSERT INTO product VALUES (0, \"{name_product}\", \"{url}\")"
                my_cursor.execute(insert_query)
                conn.commit()

                # Select query to get inserted product id into foreign key
                select_query = f"SELECT id_product FROM product WHERE url_product = \"{url}\""
                my_cursor.execute(select_query)
                for e in my_cursor:
                    foreign_key = e[0]
                    print(e[0])
                                
                # Insert query to history table
                insert_query = f"INSERT INTO history VALUES (0, {foreign_key}, \"{name_product}\", \"{price_product}\", \"{available}\", \"{today}\")"
                my_cursor.execute(insert_query)
                conn.commit()


            else:
                # Select query to get inserted product id into foreign key
                select_query = f"SELECT id_product FROM product WHERE url_product = \"{url}\""
                my_cursor.execute(select_query)
                for e in my_cursor:
                    foreign_key = e[0]
                    print(e[0])
                
                # Insert query to history table
                insert_query = f"INSERT INTO history VALUES (0, {foreign_key}, \"{name_product}\", \"{price_product}\", \"{available}\", \"{today}\")"
                my_cursor.execute(insert_query)
                conn.commit()

        except Exception as e:
                print(e)

        print("\n=========================================================================\n")

    print("Connection to database closed.")
    conn.close()

except Exception as e:
    print(e)

# Insert codes for database connection into a function.
# Insert each query lines into a function for each store.
# Write function that allows user to choose store to scrap.