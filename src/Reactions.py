from math import exp
from DATA.reactions.read_reactions import read_reactions_from_xlsx


class Reactions:
    def __init__(self, reactions=None):
        if reactions is None:
            reactions = read_reactions_from_xlsx()
        self.__reactions = {}
        for id, parameters in reactions.items():
            self.__reactions[id] = Reaction(parameters)

    def get_reaction(self, name):
        return self.__reactions[name]

    def get_reactions(self):
        return self.__reactions


class Reaction:
    def __init__(self, parameters: dict):
        self.__A = parameters['A']
        self.__E = parameters['E']
        self.__n = parameters['n']
        self.__balance = {}
        divider = parameters['Divider']
        for name, value in parameters['Components'].items():
            self.__balance[name] = value / divider
        self.__order = parameters['Order']
        self.__equation = parameters['equation']

    def calculate(self, model, temp, tay):
        rate = self.calculate_rate(model, temp)
        result = {}
        for name, coefficient in self.__balance.items():
            result[name] = rate * tay * coefficient
        return result

    def calculate_rate(self, model, temp):
        rate = self.calculate_k(temp)
        for component, coefficient in self.__balance.items():
            if coefficient < 0:
                rate *= (model.get_section().calc_component_concentration(model, component) ** (self.__order[component]))
        return rate

    def calculate_k(self, temp):
        R = 8.31432
        A = self.A
        E = self.E * 1000
        T = temp + 273.15
        return A * exp(- E / (R * T))

    @property
    def A(self):
        return self.__A

    @A.setter
    def A(self, value: float):
        self.__A = value

    @property
    def E(self):
        return self.__E

    @E.setter
    def E(self, value: float):
        self.__E = value

    @property
    def n(self):
        return self.__n

    @n.setter
    def n(self, value: float):
        self.__n = value
