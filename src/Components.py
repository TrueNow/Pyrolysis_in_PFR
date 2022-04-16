from DATA.components.read_components import read_components_from_xlsx


class Components:
    def __init__(self, components):
        all_components = read_components_from_xlsx()
        self.__components = {}
        for name, parameters in all_components.items():
            if name in components:
                self.__components[name] = Component(name, parameters)

    def get_component(self, name: str):
        return self.__components[name]

    def get_components(self):
        return self.__components


class Component:
    def __init__(self, name: str, parameters: dict):
        self.__name = str(name)
        self.__molarMass = parameters['Молярная масса']
        self.__molFr = float(parameters['Мольная доля'])
        self.__massFr = 0.0
        self.__type = bool(parameters['Молекула'])
        self.__formula = str(parameters['Формула'])

    @property
    def molar_mass(self):
        return self.__molarMass

    @property
    def mol_fr(self):
        return self.__molFr

    @mol_fr.setter
    def mol_fr(self, value: float):
        self.__molFr = value

    @property
    def mass_fr(self):
        return self.__massFr

    @mass_fr.setter
    def mass_fr(self, value: float):
        self.__massFr = value

    @property
    def type(self):
        return self.__type

    @property
    def formula(self):
        return self.__formula
