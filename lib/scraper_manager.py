import os, re

class ScraperManager():
    # getter
    def get_scrapers(self):
        return self._scrapers

    def __init__(self, App):
        self.App = App
        self._scrapers = {}
        self._jobs = {}
        self.scrapers_dir = App.config['SCRAPERS_DIR']
        self.scrapers_pkg = App.config['SCRAPERS_PKG']

        self.jobs_dir = App.config['JOBS_DIR']
        self.jobs_pkg = App.config['JOBS_PKG']

    # TODO: Perhaps we should check _scrapers first?
    def init_scraper(self, name):
        print("init scrapper by name: '{}'".format(name))
        # magic load the default job for this scraper type
        job_metadata = self.__lookup_class_by_class_name(name, self.jobs_pkg)
        job_class = self.__load_class(job_metadata)

        scraper_metadata = self.__lookup_class_by_class_name(name, self.scrapers_pkg)
        scraper_class = self.__load_class(scraper_metadata)
        return scraper_class(self, scraper_metadata['name'], job_class)

    def load(self):
        self._scrapers = self.__load_classes(self.scrapers_dir, self.scrapers_pkg)
        self._jobs = self.__load_classes(self.jobs_dir, self.jobs_pkg)

    # accesses file system - best to do this on inital application load.
    def __load_classes(self, directory, package_name):
        print('__load_classes from directory: {}'.format(directory))
        classes = {}
        for subdir, dirs, files in os.walk(directory):
            for filename in files:
                # Make sure we have a .py file and not a "hidden" .py file such as __init__.py
                if filename.endswith('.py') and not filename.startswith('_'):
                    class_metadata = self.__lookup_class_by_file_name(filename, package_name)
                    classes[class_metadata['name']] = class_metadata
        return classes

    # assumes that that scrapers follow the name convention: ScraperClass is in a file named scraper_class.py in the directory scrapers.
    def __lookup_class_by_class_name(self, class_name, package_name):
        print("lookup class by class name: '{}'".format(class_name))
        pieces = re.findall('[A-Z][a-z]*', class_name)
        pieces = map(lambda s: s.lower(), pieces)
        module_name = '_'.join(pieces)
        file_name = '{}.py'.format(module_name)
        return {
            'file_name': file_name,
            'import_string': '{}.{}'.format(package_name, module_name),
            'module_name': module_name,
            'class_name': class_name,
            'name': class_name
        }

    # assumes that that scrapers follow the name convention: ScraperClass is in a file named scraper_class.py in the directory scrapers.
    def __lookup_class_by_file_name(self, file_name, package_name):
        print("lookup class by file name: '{}'".format(file_name))
        module_name = file_name.replace('.py', '')
        pieces = module_name.split('_')
        pieces = map(lambda s: s.title(), pieces)
        class_name = ''.join(pieces)
        return {
            'file_name': file_name,
            'import_string': '{}.{}'.format(package_name, module_name),
            'module_name': module_name,
            'class_name': class_name,
            'name': class_name
        }

    def __load_class(self, metadata):
        # TODO: Either do this with the load_scrapers() call or refactor to use array to check for validity and handle error.
        parent_module = __import__(metadata['import_string'])
        child_module = getattr(parent_module, metadata['module_name'])
        _class = getattr(child_module, metadata['class_name'])

        return _class
