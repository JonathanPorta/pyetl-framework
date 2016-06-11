import os

class ETLJob():
    def __init__(self, extractor, transformer, loader):
        print("ETLJob base class")

        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def execute(self):
        print('etl_Job.py::execute() - the base class.')
        print('etl_Job.py::execute() - Extracting...')
        data = self.extract()
        print('etl_Job.py::execute() - extracted: ')

        print('etl_Job.py::execute() - Transforming...')
        transformed_data = self.transform(data)
        print('etl_Job.py::execute() - transformed: ')

        print('etl_Job.py::execute() - Saving...')
        saved_data = self.load(transformed_data)
        print('etl_Job.py::execute() - saved: ')

    def extract(self, *args, **kwargs):
        print("etl_Job.py::extract() - the base class.")
        return self.extractor.execute(*args, **kwargs)

    def transform(self, *args, **kwargs):
        print("etl_Job.py::transform() - the base class.")
        return self.transformer.execute(*args, **kwargs)

    def load(self, *args, **kwargs):
        print("etl_Job.py::load() - the base class.")
        return self.loader.execute(*args, **kwargs)
