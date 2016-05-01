from lib import Scraper as Scraper

class YellowstonePropertyTax(Scraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("YellowstonePropertyTax::init()")
        # self.scraper_manager = scraper_manager
        # self.name = name

    def start(self, queue):
        super().start(queue)
        print("YellowstonePropertyTax::start()", queue)
