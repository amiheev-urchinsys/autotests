from pageObjects.components.popups import Popups
from pageObjects.components.sidebar import Sidebar

class BasePage:
    def __init__(self, page):
        self.page = page
        self.sidebar = Sidebar(page)
        self.popups = Popups(page)