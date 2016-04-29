from lib import ScrapeJob as ScrapeJob

class YellowstonePropertyTax(ScrapeJob):
    def __init__(self, url):
        # self.url = url
        super.__init__(self, url)
        print("YellowstoneOrion ScrapeJob")
        print("url should be: ",url," it is:", self.url)

    def execute(self):
        super().execute()
        print("YellowstonePropertyTax::execute()")

    def retrieve(self, url):
        # Get the raw data from the webpage
        print("retrieve")

    def parse(self, data):
        # BeautifulSoup Here!
        print("parse")

    def save(self, results):
        # put the results somewhere
        print("save")
