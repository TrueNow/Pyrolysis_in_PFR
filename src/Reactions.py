from math import exp


class Reactions:
    def __init__(self, reactions=None):
        self.__reactions = {}
        for id, reaction in reactions.items():
            self.__reactions[id] = Reaction(reaction)

    def choose_used_components(self):
        components = {}
        for id, reaction in self.get_reactions().items():
            for component in reaction.balance.keys():
                components[component] = 0
        return components

    def get_reaction(self, id):
        return self.__reactions[id]

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

    @property
    def E(self):
        return self.__E

    @property
    def n(self):
        return self.__n

    @property
    def equation(self):
        return self.__equation

    @property
    def balance(self):
        return self.__balance

    def create_equation_reactions(self, reaction, components):
        """Создает уравнение одной реакции"""
        inlet, outlet = [], []
        for name, value in reaction.__balance.items():
            if value < 0:
                inlet.append(f"{-value}{components.get_component(name).formula}")
            else:
                outlet.append(f"{value}{components.get_component(name).formula}")
        self.__equation = ' + '.join(inlet) + ' ---> ' + ' + '.join(outlet)
