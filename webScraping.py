from bs4 import BeautifulSoup
import requests
import tkinter
import customtkinter
import pygame
import re

pygame.init()

def startGetPrices():
    try:
        url = link.get()
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        car_advertisements = doc.find_all("a", class_="adCard_anchor__hJqwV")
        prices=[]

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

                details = f"Price: {price_text} €\n" \
                          f"Mileage: {mileage_text}\n" \
                           f"Year: {year}\n" \
                          f"Transmission: {transmission}\n\n"

                prices.append(details)
        prices_text_area.delete(1.0, tkinter.END)

        # Insert the sorted prices into the text area
        for price in prices:
            prices_text_area.insert(tkinter.END, price)

        finishLabel.configure(text="Fetching complete.", text_color="green")  # Success message

    except Exception as e:
        finishLabel.configure(text=f"Error: {e}", text_color="red")  # Display error message
 # Display error message


       # sortedPrices=sorted(prices, key=lambda x: int (x.replace(" €","").replace(" ", "")))
        #prices_text_area.delete(1.0, tkinter.END)
        #for price in sortedPrices:
         #   prices_text_area.insert(tkinter.END, price + "\n")

        #finishLabel.configure(text="Fetching complete.", text_color="green")  # Success message

    #except Exception as e:
       # finishLabel.configure(text=f"Error {e}", text_color="red")  # Error message


# SYSTEM SETTINGS
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# APP FRAME
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Tori.fi Autojen Hinnat")

# UI ELEMENTS
title = customtkinter.CTkLabel(app, text="Lisää URL osoite:")
title.pack(padx=10, pady=10)

# LINK INPUT
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()
        # url = "https://autot.tori.fi/vaihtoautot/bmw/335?korimalli=coupe"

# FINISHED GET PRICES
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# GET BUTTON
getPrices = customtkinter.CTkButton(app, text="Hae Hinnat", command=startGetPrices)
getPrices.pack(padx=10, pady=10)

# TEXT AREA FOR PRICES
prices_text_area = tkinter.Text(app, height=10, width=70)
prices_text_area.pack(padx=10, pady=10)

# RUN APP
app.mainloop()

