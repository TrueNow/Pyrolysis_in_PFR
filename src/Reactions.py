from math import exp


class Reactions:
    def __init__(self, filename: str):
        self.filename = filename
        self.reactions = {}

    def choose_used_components(self) -> dict:
        components = {}
        for id, reaction in self.reactions.items():
            for component in reaction.balance.keys():
                components[component] = 0
        return components

    def data_table(self):
        data = []
        for id, reaction in self.reactions.items():
            data.append([id, reaction.equation,
                         f'{reaction.A:2.3e}',
                         f'{reaction.E:.2f}'])
        return data

    def get_reaction(self, id):
        return self.reactions[id]

    def add_reaction(self, id, parameters):
        self.reactions[id] = Reaction(**parameters)


class Reaction:
    def __init__(self, id, A, E, n, balance, order):
        self.id = id
        self.A = A
        self.E = E
        self.n = n
        self.balance = balance
        self.order = order
        self.equation = ''

    def calculate(self, components, section):
        rate = self.calculate_rate(components, section)
        result = {}
        for name, coefficient in self.balance.items():
            result[name] = rate * section.time * coefficient
        return result

    def calculate_rate(self, components, section):
        rate = self.calculate_k(section)
        for component, coefficient in self.balance.items():
            if coefficient < 0:
                rate *= (components.get_component(component).calculate_concentration(section) ** (self.order[component]))
        return rate

    def calculate_k(self, section):
        R = 8.31432
        A = self.A
        E = self.E * 1000
        T = section.temperature_inlet + 273.15
        return A * exp(- E / (R * T))

    def set_equation(self, components):
        """Создает уравнение одной реакции"""
        inlet, outlet = [], []
        for name, value in self.balance.items():
            if value < 0 and abs(value) == 1:
                inlet.append(f"{components.get_component(name).formula}")
            elif value < 0 and abs(value) != 1:
                inlet.append(f"{-value:.0f}{components.get_component(name).formula}")
            elif value > 0 and abs(value) == 1:
                outlet.append(f"{components.get_component(name).formula}")
            elif value > 0 and abs(value) != 1:
                outlet.append(f"{value:.0f}{components.get_component(name).formula}")
        self.equation = ' + '.join(inlet) + ' ---> ' + ' + '.join(outlet)
