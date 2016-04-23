import os

class ScraperManager():
    def __init__(self, App):
        self.App = App
        self._scrapers = []
        self.scrapers_dir = App.config['SCRAPERS_DIR']

    def load_scraper(self, name):
        print("Looking up scrapper by name: '{}'".format(name))
        module_name = "scrapers.{}".format(name)
        scraper = self.__load_module(module_name)
        return scraper(self, name)

    def list_scrapers(self):
        print('list_scrapers')
        for subdir, dirs, files in os.walk(self.scrapers_dir):
            for filename in files:
                # Make sure we have a .py file and not a 'hidden' .py file such as __init__.py
                if filename.endswith('.py') and not filename.startswith('_'):
                    scraper = self.__sanitize_scraper_name(filename)
                    self._scrapers.append(scraper)
        return self._scrapers

    def __sanitize_scraper_name(self, name):
        name = name.replace('.py', '')
        pieces = name.split('_')
        pieces = map(lambda s: s.title(), pieces)
        return ''.join(pieces)

    def __load_module(self, name):
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod
