import mysql.connector
from datetime import datetime

class Db_Operations:

    conn = None
    my_cursor = None

    def __init__(self):
        self.HOST = "localhost"
        self.DATABASE = "web_scraper"
        self.USER = "root"
        self.PASSWORD = "root"
        self.today = datetime.today().strftime("%Y-%m-%d")

    # Connection to database
    def Connect_to_db(self):
        try:
            print("\n=========================================================================\n")
            print("Connecting to database...")
            self.conn = mysql.connector.connect(host = self.HOST, user = self.USER, password = self.PASSWORD, database = self.DATABASE)
            self.my_cursor = self.conn.cursor(buffered=True)
            self.my_cursor.execute("SET GLOBAL time_zone = '+02:00'")
            print("Connected to database succesfully!")
            print("\n=========================================================================\n")
        except Exception as e:
            print(e)

    def Disconnect_from_db(self):
        self.conn.close()

    # Insert query to product table
    def Insert_product(self, name_product, url):
        insert_query = f"INSERT INTO product VALUES (0, \"{name_product}\", \"{url}\")"
        self.my_cursor.execute(insert_query)
        self.conn.commit()

    # Insert query to history table
    def Insert_history(self, foreign_key, name_product, price_product, available):
        my_cursor = self.conn.cursor()
        insert_query = f"INSERT INTO history VALUES (0, {foreign_key}, \"{name_product}\", \"{price_product}\", \"{available}\", \"{self.today}\")"
        my_cursor.execute(insert_query)
        self.conn.commit()
        my_cursor.close()

    # Select query to check if already in table
    def Select_url(self, url):
        select_query = f"SELECT url_product FROM product WHERE url_product = \"{url}\""
        self.my_cursor.execute(select_query)
        link_list = list()
        for link in self.my_cursor:
            link_list.append(link[0])
        return link_list

    # Select query to get inserted product id into foreign key
    def Select_fk(self, url):
        my_cursor = self.conn.cursor()
        select_query = f"SELECT id_product FROM product WHERE url_product = \"{url}\""
        my_cursor.execute(select_query)
        for e in my_cursor:
            foreign_key = e[0]
        my_cursor.close()
        return foreign_key
    
