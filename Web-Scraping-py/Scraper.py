from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error

class Scraper:

    def __init__(self):
        self.name_product = "name_product"
        self.price_product = "0"
        self.available = "Available"

    # This code is for products of store.steampowered.com
    def Scrap_steam(self, url):
        try:
            # Open the URL as Browser, not as python urllib to avoid Forbidden errors
            page = urllib.request.Request(url,headers={'User-Agent': 'Chrome'}) 
            html = urllib.request.urlopen(page).read()

            soup = BeautifulSoup(html, features="lxml") # lxml helps to interpret the html

            tag_item_name = soup.find("div", class_="apphub_AppName")
            self.name_product = tag_item_name.text

            game_area_tag = soup.find("div", class_="game_area_purchase_game")

            if "PROMOTION" in game_area_tag.text:
                price_tag = soup.find(attrs={"class": "discount_final_price"})
                self.price_product = price_tag.text.replace("€", " E").strip()

            else:
                price_tag = soup.find(attrs={"class": "game_purchase_price price"})
                self.price_product = price_tag.text.replace("€", " E").strip()

        except Exception as e:
            print(e)


    # This code is for products of www.pccomponentes.com
    def Scrap_pc(self, url):
        try:
            # Open the URL as Browser, not as python urllib to avoid Forbidden errors
            page = urllib.request.Request(url,headers={'User-Agent': 'Chrome'}) 
            html = urllib.request.urlopen(page).read()

            soup = BeautifulSoup(html, features="lxml") # lxml helps to interpret the html

            tag_sections = soup.find_all("div", class_="precioMain h1")
            tag_item_name = soup.find("div", class_="articulo")

            self.name_product = tag_item_name.text

            self.price_product = tag_sections[0].text
            self.price_product = self.price_product.replace("€", " E")

            self.available = False

            tag_buy = soup.find_all("button", type="button")

            for element in tag_buy:
                if "Comprar" in element.text:
                    self.available = "Available"
                if "Avísame" in element.text:
                    self.available = "Not available"

        except Exception as e:
            print(e)


    def Get_price_product(self):
        return self.price_product

    def Get_name_product(self):
        return self.name_product

    def Get_available(self):
        return self.available