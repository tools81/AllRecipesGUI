class SearchResult(object):

    def __init__(self, title, stars, reviews, image, link, selected):
        self.title = title
        self.stars = stars
        self.reviews = reviews
        self.image = image
        self.link = link
        self.selected = selected

    def select(self):
        self.selected = True

    def click(self):
        self.selected = True
        self.title = "Selected"