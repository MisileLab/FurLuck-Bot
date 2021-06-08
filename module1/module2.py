from dislash import Type, Option

def getoption(arglist:list):
    a = []
    name = 'itsaname'
    description = None
    required = True
    itsnottypefunction = Type.STRING
    for i in arglist:
        for key, value in i.items():
            if key == 'name':
                name = value
            elif key == 'description':
                description = value
            elif key == 'required':
                required = value
            elif key == 'type':
                itsnottypefunction = value
        a.append(Option(
            name=name,
            description=description,
            required=required,
            type=itsnottypefunction
        ))
    return a

class NewOptionList:
    def __init__(self):
        self.option = []

    def make_option(self, name, description, required:bool, type):
        option = Option(name=name, description=description, required=required, type=type)
        self.option.append(option)
        return self.option

    @property
    def getoption(self, getnumber:int=0):
        return self.option[getnumber]