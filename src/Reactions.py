from math import exp


class Reactions:
    def __init__(self, reactions, filename):
        self.filename = filename
        self._reactions = {}
        for id, reaction in reactions.items():
            self._reactions[id] = Reaction(reaction)

    def choose_used_components(self):
        components = {}
        for id, reaction in self.get_reactions().items():
            for component in reaction.balance.keys():
                components[component] = 0
        return components

    def get_reaction(self, id):
        return self._reactions[id]

    def get_reactions(self):
        return self._reactions


class Reaction:
    def __init__(self, parameters: dict):
        self._A = parameters['A']
        self._E = parameters['E']
        self._n = parameters['n']
        self._balance = {}
        divider = parameters['Divider']
        for name, value in parameters['Components'].items():
            self._balance[name] = value / divider
        self._order = parameters['Order']
        self._equation = parameters['equation']

    def calculate(self, components, section):
        rate = self.calculate_rate(components, section)
        result = {}
        for name, coefficient in self._balance.items():
            result[name] = rate * section.tay * coefficient
        return result

    def calculate_rate(self, components, section):
        rate = self.calculate_k(section)
        for component, coefficient in self._balance.items():
            if coefficient < 0:
                rate *= (components.get_component(component).calc_concentration(section) ** (self._order[component]))
        return rate

    def calculate_k(self, section):
        R = 8.31432
        A = self.A
        E = self.E * 1000
        T = section.temp_in + 273.15
        return A * exp(- E / (R * T))

    @property
    def A(self):
        return self._A

    @property
    def E(self):
        return self._E

    @property
    def n(self):
        return self._n

    @property
    def equation(self):
        return self._equation

    @property
    def balance(self):
        return self._balance

    def set_equation(self, components):
        """Создает уравнение одной реакции"""
        inlet, outlet = [], []
        for name, value in self.balance.items():
            if value < 0:
                inlet.append(f"{-value}{components.get_component(name).formula}")
            else:
                outlet.append(f"{value}{components.get_component(name).formula}")
        self._equation = ' + '.join(inlet) + ' ---> ' + ' + '.join(outlet)
