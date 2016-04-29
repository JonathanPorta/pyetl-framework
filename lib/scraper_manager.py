import os, re

class ScraperManager():
    # getter
    def get_scrapers(self):
        return self._scrapers

    def __init__(self, App):
        self.App = App
        self._scrapers = {}
        self.scrapers_dir = App.config['SCRAPERS_DIR']
        self.scrapers_pkg = App.config['SCRAPERS_PKG']

    # TODO: Perhaps we should check _scrapers first?
    def init_scraper(self, name):
        print("init scrapper by name: '{}'".format(name))
        scraper_metadata = self.__lookup_scraper_by_class_name(name)
        scraper_class = self.__load_scraper(scraper_metadata)
        return scraper_class(self, scraper_metadata['name'])

    # accesses file system - best to do this on inital application load.
    def load_scrapers(self):
        print('load_scrapers from directory: {}'.format(self.scrapers_dir))
        for subdir, dirs, files in os.walk(self.scrapers_dir):
            for filename in files:
                # Make sure we have a .py file and not a "hidden" .py file such as __init__.py
                if filename.endswith('.py') and not filename.startswith('_'):
                    scraper_metadata = self.__lookup_scraper_by_file_name(filename)
                    self._scrapers[scraper_metadata['name']] = scraper_metadata

    # assumes that that scrapers follow the name convention: ScraperClass is in a file named scraper_class.py in the directory scrapers.
    def __lookup_scraper_by_class_name(self, class_name):
        print("lookup scraper by class name: '{}'".format(class_name))
        pieces = re.findall('[A-Z][a-z]*', class_name)
        pieces = map(lambda s: s.lower(), pieces)
        module_name = '_'.join(pieces)
        file_name = '{}.py'.format(module_name)
        return {
            'file_name': file_name,
            'import_string': '{}.{}'.format(self.scrapers_pkg, module_name),
            'module_name': module_name,
            'class_name': class_name,
            'name': class_name
        }

    # assumes that that scrapers follow the name convention: ScraperClass is in a file named scraper_class.py in the directory scrapers.
    def __lookup_scraper_by_file_name(self, file_name):
        print("lookup scraper by file name: '{}'".format(file_name))
        module_name = file_name.replace('.py', '')
        pieces = module_name.split('_')
        pieces = map(lambda s: s.title(), pieces)
        class_name = ''.join(pieces)
        return {
            'file_name': file_name,
            'import_string': '{}.{}'.format(self.scrapers_pkg, module_name),
            'module_name': module_name,
            'class_name': class_name,
            'name': class_name
        }

    def __load_scraper(self, scraper_metadata):
        # TODO: Either do this with the load_scrapers() call or refactor to use array to check for validity and handle error.
        parent_module = __import__(scraper_metadata['import_string'])
        child_module = getattr(parent_module, scraper_metadata['module_name'])
        scraper_class = getattr(child_module, scraper_metadata['class_name'])
        return scraper_class
