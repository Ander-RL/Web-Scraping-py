import mysql.connector
from Db_Operations import Db_Operations
from LinksReader import LinksReader
from Scraper import Scraper

db = Db_Operations()
scrap = Scraper()

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

        if "pccomponentes" in url:
            scrap.Scrap_pc(url)
            name_product = scrap.Get_name_product()
            price_product = scrap.Get_price_product()
            available = scrap.Get_available()

        if "steampowered" in url:
            scrap.Scrap_steam(url)
            name_product = scrap.Get_name_product()
            price_product = scrap.Get_price_product()
            available = scrap.Get_available()

        print(url)
        print(name_product)
        print(price_product)
        print(available)

        print("\n=========================================================================\n")

        # Select query to check if already in table
        link_list = db.Select_url(url)

        for link in link_list:
            db_list.append(link)

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

print("Connection to database closed.")
db.Disconnect_from_db()

# Write function that allows user to choose store to scrap.
# Create Scraper class.
# Scrap Steam.