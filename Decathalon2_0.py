import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *
from tkinter import filedialog, ttk
from tkinter.scrolledtext import ScrolledText

def scrape_and_save(query):
    result_text.config(state=NORMAL)
    result_text.delete(1.0, END)

    # Initialize an empty dictionary
    data_dict = {"Name": [], "Description": [], "Rating": [], "Curr_Price": [], "Actual_Price": [], "Link": []}

    page = requests.get(f"https://www.decathlon.in/search?query={query}").text
    soup = BeautifulSoup(page, "html.parser")

    data_all = soup.find_all("li", class_="ais-InfiniteHits-item")

    for data in data_all:
        name = data.find("div", class_="font-semibold text-grey-900 lg:text-16 cn-481").text.strip()
        description = data.find("p", class_="capitalize text-14 lg:text-14 whitespace-nowrap overflow-ellipsis overflow-hidden mt-1").text.strip()
        rating = data.find("span", class_="ml-1 font-semibold text-blue-500 text-12 lg:text-14").text.strip()
        price = data.find("span", class_="text-12 lg:text-16 font-semibold").text.replace("₹", "").strip()
        discount = data.find("span", class_="").text.replace("₹", "").strip()
        link = data.find("a", class_="").get("href")

        # Update the dictionary with new key-value pairs
        data_dict["Name"].append(name)
        data_dict["Description"].append(description)
        data_dict["Rating"].append(rating)
        data_dict["Curr_Price"].append(price)
        data_dict["Actual_Price"].append(discount)
        data_dict["Link"].append("https://www.decathlon.in" + link)

    # Save the data to a CSV file
    file_path = filedialog.asksaveasfilename(defaultextension=('csv', '*.csv'))
    if file_path:
        df = pd.DataFrame(data_dict)
        df.to_csv(file_path, index=False)
        result_text.insert(END, f"Data saved to: {file_path}\n")
    else:
        result_text.insert(END, "Operation canceled by user.\n")

    result_text.config(state=DISABLED)

# Create a more interactive GUI
root = Tk()
root.title("Decathlon Scraper")
root.geometry("600x400")

style = ttk.Style()
style.theme_use("clam")

frame = Frame(root)
frame.pack(pady=20)

label = Label(frame, text="Enter Product Query:")
label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

entry = Entry(frame, width=30)
entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

scrape_button = Button(frame, text="Scrape and Save", command=lambda: scrape_and_save(entry.get()))
scrape_button.grid(row=1, column=0, columnspan=2, pady=10)

result_frame = Frame(root)
result_frame.pack()

result_label = Label(result_frame, text="Scraping Results:")
result_label.pack(pady=10)

result_text = ScrolledText(result_frame, height=8, width=70, state=DISABLED)
result_text.pack(pady=10)

quit_button = Button(root, text="Quit", command=root.destroy)
quit_button.pack(pady=20)

root.mainloop()
