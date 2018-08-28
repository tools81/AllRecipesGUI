import tkinter as tk
from bs4 import BeautifulSoup
import urllib
import urllib.request
from io import BytesIO
from PIL import Image, ImageTk
from collections import defaultdict
from SearchResult import SearchResult

root = tk.Tk()
root.title("All Recipes GUI")
# root.geometry("1280x768")

results = []
result_containers = defaultdict(list)
sortChoice = "re"
image_size = 150, 150


def search(event):
    url_result = urllib.request.urlopen(
        "https://www.allrecipes.com/search/results/?wt={0}&sort={1}"
            .format(search_input.get().replace(' ', "%20"), sortChoice))
    url_bytes = url_result.read()
    url_string = url_bytes.decode("utf8")
    url_result.close()

    soup = BeautifulSoup(url_string, 'html.parser')
    display(soup)


def display(soup):
    result_list_row = 2
    display_row = 0
    result_list_column = 0
    result_count = 0
    for result in soup.find_all("article", class_='fixed-recipe-card'):
        with urllib.request.urlopen(result.find("img", class_='fixed-recipe-card__img')
                                            .attrs['data-original-src']) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        image = ImageTk.PhotoImage(im.resize(image_size))

        results.append(SearchResult(result.find("span", class_='fixed-recipe-card__title-link').string,
                                    result.find("span", class_='stars').attrs['data-ratingstars'],
                                    result.find("span", class_='fixed-recipe-card__reviews').contents[0].attrs[
                                        'number'],
                                    image,
                                    result.find("a", {'data-internal-referrer-link': 'hub recipe'}).attrs['href'],
                       False))

    for result in results:
        if len(result.title) > 21:
            result.title = result.title[:21] + "..."

        container = tk.Frame(root, width=150)

        if result.selected:
            container.background = "green"

        tk.Message(master=container, text=result.title, bg="blue", fg="white", width=150).pack(fill=tk.BOTH)
        tk.Label(master=container, image=result.image, bg="orange").pack()
        tk.Label(master=container, text=result.stars).pack()
        tk.Label(master=container, text=result.reviews).pack()
        result_containers[display_row].append(
            container.grid(row=result_list_row, column=result_list_column, padx=3, pady=3))

        result_list_column = result_list_column + 1
        result_count = result_count + 1
        if result_count % 5 == 0:
            result_list_row = result_list_row + 1
            display_row = display_row + 1
            result_list_column = 0

    # tk.Frame(result_containers[0][3]).config(bg="red")


root.bind('<Return>', search)
title = tk.Label(root, text="Search All Recipes", font=("Meiryo", 24))
search_input = tk.Entry(root, font=("Meiryo", 36))
search_button = tk.Button(root, text="Search", fg="white", bg="green", font=("Meiryo", 22))
search_button.bind("<Button-1>", search)

title.grid(row=0, columnspan=10)
search_input.grid(row=1, columnspan=4)
search_button.grid(row=1, column=4)
search_input.focus_set()

root.mainloop()
