from pageObjects.components.sidebar import Sidebar

class BasePage:
    def __init__(self, page):
        self.page = page
        self.sidebar = Sidebar(page)