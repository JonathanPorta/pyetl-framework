import os

class Loader():
    def __init__(self, *args, **kwargs):
        print("Loader::init() - the base class.")

    def execute(self, *args, **kwargs):
        print("Loader::execute() - the base class.")
