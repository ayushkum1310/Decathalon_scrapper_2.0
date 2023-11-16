import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *
from tkinter import Tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename,asksaveasfilename


root=Tk()
root.geometry("700x300")
root.config(bg="#87BDD8")

def Search():
    file=asksaveasfilename(defaultextension=('csv', '*.csv',"*xlsx"))
    b=value.get("1.0","end-1c")
    page = requests.get(f"https://www.decathlon.in/search?query={b}").text
    a=f"https://www.decathlon.in/search?query={b}"

# Initialize an empty dictionary
    data_dict = {"Name": [], "Description": [], "Rating": [], "Curr_Price": [], "Actual_Price": [], "Link": []}

    
    soup = BeautifulSoup(page, "html.parser")

    data_all = soup.find_all("li", class_="ais-InfiniteHits-item")

    for data in data_all:
        name = data.find("div", class_="font-semibold text-grey-900 lg:text-16 cn-481").text.strip()
        description = data.find("p", class_="capitalize text-14 lg:text-14 whitespace-nowrap overflow-ellipsis overflow-hidden mt-1").text.strip()
        rating = data.find("span", class_="ml-1 font-semibold text-blue-500 text-12 lg:text-14").text.strip()
        price = data.find("span", class_="text-12 lg:text-16 font-semibold").text.replace("₹","").strip()
        discount = data.find("span", class_="").text.replace("₹","").strip()
        link = data.find("a", class_="").get("href")

        # Update the dictionary with new key-value pairs
        data_dict["Name"].append(name)
        data_dict["Description"].append(description)
        data_dict["Rating"].append(rating)
        data_dict["Curr_Price"].append(price)
        data_dict["Actual_Price"].append(discount)
        data_dict["Link"].append("https://www.decathlon.in"+link)

    # Print the dictionary
    df=pd.DataFrame(data_dict)
    df.to_csv(file,index=False)
def quit_app():
    root.destroy()


value=Text(root, height=2, width=40)
value.place(x=200,y=20)
# val=Text(root, height=2, width=40)
# val.place(x=200,y=75)


hi=Label(root,text="Product Name:",bg="#87BDD8",font=("ariel 17 bold"), width=12)
hi.place(x=20,y=20)
# hi2=Label(root,text="File Name:",bg="#87BDD8",font=("ariel 17 bold"), width=8)
# hi2.place(x=45,y=75)
hi3=Label(root,text="Note:Enter '%20' insteed of space",bg="#87BDD8",font=("ariel 17 bold"), width=50)
hi3.place(x=10,y=270)

comment= Button(root, height=3, width=10, text="Generate File",fg='Red', command=lambda: Search())

#command=get_input() will wait for the key to press and displays the entered text
comment.place(x=300,y=200)
# qui.place(10,200)
quit_button = Button(root, height=3, width=10, text="Quit", fg='Black', command=quit_app)
quit_button.place(x=500, y=200)
root.mainloop()
