import os, re, sys
from os import path
from importlib.machinery import SourceFileLoader

class PipelineManager():
    # getter
    def get_pipelines(self):
        return self._pipelines

    def __init__(self, App):
        self.App = App
        self._pipelines = {}
        self._extractors = {}
        self._transformers = {}
        self._loaders = {}

        self.base_dir = App.config['BASE_DIR']
        # Ensure we load anything we need from the package using this framework
        sys.path.append(os.path.dirname(path.join(self.base_dir, '*')))

        self.pipelines_dir = App.config['PIPELINES_DIR']
        self.pipelines_pkg = App.config['PIPELINES_PKG']

        self.extractors_dir = App.config['EXTRACTORS_DIR']
        self.extractors_pkg = App.config['EXTRACTORS_PKG']

        self.transformers_dir = App.config['TRANSFORMERS_DIR']
        self.transformers_pkg = App.config['TRANSFORMERS_PKG']

        self.loaders_dir = App.config['LOADERS_DIR']
        self.loaders_pkg = App.config['LOADERS_PKG']

    # TODO: Perhaps we should check _pipelines first?
    def init_pipeline(self, name):
        print("init pipeline by name: '{}'".format(name))
        # magic load the default extractor, transformer, and loader for this pipeline
        extractor_metadata = self.__lookup_class_by_class_name(name, self.extractors_pkg, self.extractors_dir)
        extractor_class = self.__load_class(extractor_metadata)

        transformer_metadata = self.__lookup_class_by_class_name(name, self.transformers_pkg, self.transformers_dir)
        transformer_class = self.__load_class(transformer_metadata)

        loader_metadata = self.__lookup_class_by_class_name(name, self.loaders_pkg, self.loaders_dir)
        loader_class = self.__load_class(loader_metadata)

        # instantiate the pipeline and return an instance
        pipeline_metadata = self.__lookup_class_by_class_name(name, self.pipelines_pkg, self.pipelines_dir)
        pipeline_class = self.__load_class(pipeline_metadata)
        return pipeline_class(self, pipeline_metadata['name'], extractor_class, transformer_class, loader_class)

    def load(self):
        self._pipelines = self.__load_classes(self.pipelines_dir, self.pipelines_pkg)

        self._extractors = self.__load_classes(self.extractors_dir, self.extractors_pkg)
        self._transformers = self.__load_classes(self.transformers_dir, self.transformers_pkg)
        self._loaders = self.__load_classes(self.loaders_dir, self.loaders_pkg)

    # accesses file system - best to do this on inital application load.
    def __load_classes(self, directory, package_name):
        print('__load_classes from directory: {}'.format(directory))
        classes = {}
        for subdir, dirs, files in os.walk(directory):
            for filename in files:
                # Make sure we have a .py file and not a "hidden" .py file such as __init__.py
                if filename.endswith('.py') and not filename.startswith('_'):
                    class_metadata = self.__lookup_class_by_file_name(filename, package_name, directory)
                    classes[class_metadata['name']] = class_metadata
        return classes

    # assumes that that pipelines, extractors, transformers, and loaders follow
    # the name convention: PipelineClassName is in a file named pipeline_class_name.py
    # in the directory pipelines.
    def __lookup_class_by_class_name(self, class_name, package_name, directory):
        print("lookup class by class name: '{}'".format(class_name))
        pieces = re.findall('[A-Z][a-z]*', class_name)
        pieces = map(lambda s: s.lower(), pieces)
        module_name = '_'.join(pieces)
        file_name = '{}.py'.format(module_name)
        return {
            'file_name': file_name,
            'import_path': path.join(directory, file_name),
            'module_name': "{}.{}".format(package_name, module_name),
            'class_name': class_name,
            'name': class_name,
            'directory': directory
        }

    # assumes that that pipelines, extractors, transformers, and loaders follow
    # the name convention: PipelineClassName is in a file named pipeline_class_name.py
    # in the directory pipelines.
    def __lookup_class_by_file_name(self, file_name, package_name, directory):
        print("lookup class by file name: '{}'".format(file_name))
        module_name = file_name.replace('.py', '')
        pieces = module_name.split('_')
        pieces = map(lambda s: s.title(), pieces)
        class_name = ''.join(pieces)
        return {
            'file_name': file_name,
            'import_path': path.join(directory, file_name),
            'module_name': "{}.{}".format(package_name, module_name),
            'class_name': class_name,
            'name': class_name,
            'directory': directory
        }

    def __load_class(self, metadata):
        # TODO: Either do this with the load_pipelines() call or refactor to use array to check for validity and handle error.
        # parent_module = __import__(metadata['import_path'])
        # child_module = getattr(parent_module, metadata['module_name'])
        print(metadata)
        print('-----------------------------------------------')
        _module = SourceFileLoader(metadata['module_name'], metadata['import_path']).load_module()
        print(_module)
        _class = getattr(_module, metadata['class_name'])
        return _class
