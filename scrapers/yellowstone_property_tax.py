from lib import Scraper as Scraper

class YellowstonePropertyTax(Scraper):
    def __init__(self, scraper_manager, name):
        super().__init__(scraper_manager, name)
        print("YellowstonePropertyTax::init()")
        self.scraper_manager = scraper_manager
        self.name = name

    def start(self):
        super().start()
        print("YellowstonePropertyTax::start()")
