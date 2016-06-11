import os

class Extractor():
    def __init__(self, *args, **kwargs):
        print("Extractor::init() - the base class.")

    def execute(self, *args, **kwargs):
        print("Extractor::execute() - the base class.")
