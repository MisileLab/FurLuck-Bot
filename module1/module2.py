from dislash import Option

class NewOptionList:
    def __init__(self):
        self.option = []

    def make_option(self, name, description, required:bool, type):
        option = Option(name=name, description=description, required=required, type=type)
        self.option.append(option)
        return self.option