from bs4 import BeautifulSoup
import requests
import tkinter
from tkinter import ttk
import customtkinter
import pygame
import re

pygame.init()

def constructUrl():
    base_url = "https://autot.tori.fi/vaihtoautot/"
    merkki = merkki_var.get()
    malli = malli_var.get()
    korimalli = korimalli_var.get()
    kayttovoima = kayttovoima_var.get()
    vaihteisto = vaihteisto_var.get()

    url = f"{base_url}{merkki}/{malli}?korimalli={korimalli}&kayttovoima={kayttovoima}&vaihteisto={vaihteisto}"
    print(url)

    return url

def startGetPrices():
    try:
        # GET AND PARSE THE HTML
        url = constructUrl()
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        car_advertisements = doc.find_all("a", class_="adCard_anchor__hJqwV")

        if not car_advertisements:
            # NO CARS, DISPLAY MESSAGE
            prices_text_area.delete(1.0, tkinter.END)
            prices_text_area.insert(tkinter.END, "Hakuehdoilla ei löytynyt autoja")
            finishLabel.configure(text="No cars found.", text_color="red")
            return

        # MAKE ARRAY FOR THE DESIRED INFO
        prices=[]

        #GO THROUGH THE FETCHED MATERIAL
        for ad in car_advertisements:
            price_element = ad.find("p", class_="m:mb-4 typography_shared__SK_V2 typography_m-headingS__ozYY8 typography_subtitle2__nF6ow")
            details_element = ad.find("p", class_="hidden m:block float-left text-gray-dark typography_shared__SK_V2 typography_m-body1__5__iP typography_body2__fCRbo")

            if price_element and "€" in price_element.get_text() and details_element:
                price_text=price_element.get_text().strip()

                svg_parent = details_element.find("svg").find_parent()
                mileage_text = svg_parent.get_text().strip()
                km_index= mileage_text.find("km")
                if km_index != -1:
                    mileage_text=mileage_text[:km_index + 2]

                year_match = re.search(r"(\d{4})", details_element.get_text())
                transmission_match = re.search(r"(Automaatti|Manuaali)", details_element.get_text())

                year = year_match.group(1) if year_match else "N/A"
                transmission = transmission_match.group(1) if transmission_match else "N/A"
                
                #SORT WANTED DATA NICELY
                details = f"Price: {price_text} €\n" \
                          f"Mileage: {mileage_text}\n" \
                           f"Year: {year}\n" \
                          f"Transmission: {transmission}\n\n"
                
                #ADD SORTED DATA (DETAILS) INTO THE ARRAY (PRICES)
                prices.append(details)
        prices_text_area.delete(1.0, tkinter.END)
        
        # INSERTING PRICES ON TEXTAREA
        for price in prices:
            prices_text_area.insert(tkinter.END, price)

        finishLabel.configure(text="Fetching complete.", text_color="green")  # SUCCESS!

    except Exception as e:
        finishLabel.configure(text=f"Error: {e}", text_color="red")  # DISPLAY ERROR
 


# SYSTEM SETTINGS
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# APP FRAME
app = customtkinter.CTk()
app.geometry("720x980")
app.title("Tori.fi Autojen Hinnat")

# UI ELEMENTS
title = customtkinter.CTkLabel(app, text="Hae autojen tiedot Tori.fi, lisäämällä hakuehdot")
title.pack(padx=10, pady=10)

# FINISHED GET PRICES
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# SEARCH PARAMETER VALUABLES
merkki_var = tkinter.StringVar()
malli_var =tkinter.StringVar()
korimalli_var = tkinter.StringVar()
kayttovoima_var = tkinter.StringVar()
vaihteisto_var = tkinter.StringVar()

# CREATE A DROPDOWN FOR MERKIT
merkit = [
    " ","alfa-romeo", "fiat", "ford", "honda", "hyundai", "jaguar", "jeep", "kia", "lamborghini", 
    "land-rover", "lexus", "audi", "maserati", "mazda", "mercedes-benz", "mini", "mitsubishi", 
    "nissan", "opel", "peugeot", "pontiac", "porsche", "bmw", "renault", "rover", "saab", "seat", 
    "skoda", "smart", "ssangyong", "subaru", "suzuki", "toyota", "cadillac", "volkswagen", "volvo", 
    "lada", "dacia", "austin", "aston-martin", "hummer", "infiniti", "isuzu", "iveco", "chevrolet", 
    "lancia", "lincoln", "lotus", "mclaren", "tesla", "daewoo", "daihatsu", "bentley", "wartburg", 
    "ds", "chrysler", "rolls-royce", "buick", "cupra", "dkw", "gaz", "gmc", "hudson", "moskvitsh", 
    "neckar", "morris", "citroen", "oldsmobile", "trabant", "truckmasters", "talbot", "vauxhall", 
    "plymouth", "caterham", "daimler", "fiat-abarth", "dodge", "man", "maxus", "polestar", "byd", 
    "hongqi", "nio", "xpeng", "voyah", "jac", "seres", "ferrari", "chery", "lynk-&-co", "dfsk"
]
merkit= sorted(merkit)

merkki_label= customtkinter.CTkLabel(app, text="Valitse merkki: ")
merkki_label.pack(padx=10, pady=5)
merkki_dropdown = ttk.Combobox(app, values=merkit, textvariable=merkki_var)
merkki_dropdown.pack(padx=10, pady=5)
merkki_dropdown.set(merkit[0])  

# CREATE ENTRY FOR MALLI
malli_label= customtkinter.CTkLabel(app, text="Kirjoita malli: ")
malli_label.pack(padx=10, pady=5)

malli_entry =customtkinter.CTkEntry(app, textvariable=malli_var)
malli_entry.pack(padx=10, pady=5)

# CREATE A DROPDOWN FOR KORIMALLI
korimallit = [
    " ","avoauto", "avolava", "coupe", "farmari", "erikoisauto", "maasturi", 
    "viistopera", "porraspera", "tila-auto", "lyhyt-malli", "puolipitka-malli", 
    "pitka-malli", "minibussi", "muut"
]

korimalli_label= customtkinter.CTkLabel(app, text="Valitse korimalli: ")
korimalli_label.pack(padx=10, pady=5)
korimalli_dropdown = ttk.Combobox(app, values=korimallit, textvariable=korimalli_var)
korimalli_dropdown.pack(padx=10, pady=5)
korimalli_dropdown.set(korimallit[0]) 


# CREATE A DROPDOWN FOR KAYTTOVOIMA
kayttovoimat = [
    " ","bensiini", "diesel", "hybridi", "kaasu", "sahko", "e85---flexifuel"
]

kayttovoima_label= customtkinter.CTkLabel(app, text="Valitse käyttövoima: ")
kayttovoima_label.pack(padx=10, pady=5)
kayttovoima_dropdown = ttk.Combobox(app, values=kayttovoimat, textvariable=kayttovoima_var)
kayttovoima_dropdown.pack(padx=10, pady=5)
kayttovoima_dropdown.set(kayttovoimat[0]) 

# CREATE RADIOBUTTONS FOR TRANSMISSION
transmission_label=customtkinter.CTkLabel(app, text="Vaihteisto: ")
transmission_label.pack(padx=10, pady=5)
transmission_frame = tkinter.Frame(app)
transmission_frame.pack(padx=10, pady=5)
auto_radio=tkinter.Radiobutton(transmission_frame, text="Automaatti", variable=vaihteisto_var, value="automaatti")
manual_radio=tkinter.Radiobutton(transmission_frame, text="Manuaali", variable=vaihteisto_var, value="manuaali")
auto_radio.pack(side="left", padx=10)
manual_radio.pack(side="left", padx=10)


# GET BUTTON
getPrices = customtkinter.CTkButton(app, text="Hae", command=startGetPrices)
getPrices.pack(padx=10, pady=10)

# TEXT AREA FOR PRICES
prices_text_area = tkinter.Text(app, height=10, width=70)
prices_text_area.pack(padx=10, pady=10)


# RUN APP
app.mainloop()

