import os
from pyetl_framework.lib import ETLJob

class Pipeline():
    def __init__(self, pipeline_manager, name, extractor_class, transformer_class, loader_class):
        print('pipeline.py::init() - the base class.')

        self.pipeline_manager = pipeline_manager
        self.name = name

        self._extractor_class = extractor_class
        self._transformer_class = transformer_class
        self._loader_class = loader_class

    def init_etl_job(self, extractor=False, transformer=False, loader=False, **kwargs):
        print('pipeline.py::init_etl_job() - the base class.')

        if not extractor:
            extractor=self.init_extractor()

        if not transformer:
            transformer=self.init_transformer()

        if not loader:
            loader=self.init_loader()

        return ETLJob(extractor, transformer, loader, **kwargs)

    def init_extractor(self, *args, **kwargs):
        print('pipeline.py::init_extractor() - the base class.')
        return self._extractor_class(*args, **kwargs)

    def init_transformer(self, *args, **kwargs):
        print('pipeline.py::init_transformer() - the base class.')
        return self._transformer_class(*args, **kwargs)

    def init_loader(self, *args, **kwargs):
        print('pipeline.py::init_loader() - the base class.')
        return self._loader_class(*args, **kwargs)

    def start(self, queue):
        print('pipeline.py::start() - the base class.',queue)
