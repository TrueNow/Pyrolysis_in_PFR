class Components:
    def __init__(self, components: dict):
        self.__components = {}
        for name, parameters in components.items():
            self.__components[name] = Component(name, parameters)

    def get_component(self, name: str):
        return self.__components[name]

    def get_components(self):
        return self.__components


class Component:
    def __init__(self, name: str, parameters: dict):
        self.__name = name
        self.__molarMass = parameters['Молярная масса']
        self.__molFr = parameters['Мольная доля']
        self.__type = parameters['Тип']
        self.__formula = parameters['Формула']

    @property
    def molar_mass(self):
        return self.__molarMass

    @molar_mass.setter
    def molar_mass(self, value: float):
        self.__molarMass = value

    @property
    def mol_fr(self):
        return self.__molFr

    @mol_fr.setter
    def mol_fr(self, value: float):
        self.__molFr = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value

    @property
    def formula(self):
        return self.__formula

    @formula.setter
    def formula(self, value: str):
        self.__formula = value
