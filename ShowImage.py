from tkinter import *
import urllib.request
from io import BytesIO
from PIL import Image, ImageTk


class Recipe(object):
    title = ""
    stars = 0
    reviews = 0
    image = ""
    link = ""

    def __init__(self, title, stars, reviews, image, link):
        self.title = title
        self.stars = stars
        self.reviews = reviews
        self.image = image
        self.link = link


root = Tk()

recipes = []
recipeListRow = 2
recipeColumnRow = 0
recipeCount = 4

while recipeCount > 0:
    container = Frame(root, background="orange")

    with urllib.request.urlopen("https://images.media-allrecipes.com/userphotos/250x250/648053.jpg") as u:
        raw_data = u.read()
    im = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)

    recipes.append(Recipe("title",
                          0, 0, image,
                          ""))
    recipeCount = recipeCount - 1

for recipe in recipes:
    imgLabel = Label(master=container, image=recipe.image, bg="blue")

    imgLabel.pack()
    container.grid(row=recipeListRow, column=recipeColumnRow, padx=3, pady=3)

    recipeColumnRow = recipeColumnRow + 1
    if recipeCount % 5 == 0:
        recipeListRow = recipeListRow + 1
        recipeColumnRow = 0

root.mainloop()
