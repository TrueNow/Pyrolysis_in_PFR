from math import exp


class Reaction:
    def __init__(self, id, A: float | int, E: float | int, components_reaction: list[str, float | int, float | int]):
        self.id: any = id
        self.A = A
        self.E = E
        self.components_reaction = components_reaction  # [[name, coef, order], ...]
        self.equation: str = ''

    def __repr__(self) -> str:
        return f'{self.id} {self.equation}'

    def calculate_rate(self, flow, temperature: float) -> float:
        rate = self.calculate_k(temperature)
        for component_name, _, order in self.components_reaction:
            if order:
                component = flow.get_component(component_name)
                rate *= (component.concentration ** order)
        return rate

    def calculate_k(self, temperature) -> float:
        R = 8.31432
        A = self.A
        E = self.E * 1000
        T = temperature + 273.15
        return A * exp(- E / (R * T))

    def set_equation(self, components) -> None:
        """Создает уравнение одной реакции"""
        inlet, outlet = [], []
        for component_name, stoich, _ in self.components_reaction:
            component = components.get_component(component_name)
            if stoich < 0 and abs(stoich) == 1:
                inlet.append(f"{component.formula}")
            elif stoich < 0 and abs(stoich) != 1:
                inlet.append(f"{-stoich:.0f}{component.formula}")
            elif stoich > 0 and abs(stoich) == 1:
                outlet.append(f"{component.formula}")
            elif stoich > 0 and abs(stoich) != 1:
                outlet.append(f"{stoich:.0f}{component.formula}")
        self.equation = ' + '.join(inlet) + ' ---> ' + ' + '.join(outlet)


class Reactions:
    def __init__(self, filename: str):
        self.filename: str = filename
        self._reactions: dict = {}

    def __str__(self) -> str:
        return f'{[reaction for reaction in self.get_reactions()]}'

    def choose_used_components(self) -> list:
        components = []
        for reaction in self.get_reactions():
            for component_name, _, _ in reaction.components_reaction:
                if component_name in components:
                    pass
                else:
                    components.append(component_name)
        return components

    def get_reactions(self):
        return self._reactions.values()

    # def get_reaction(self, id) -> Reaction:
    #     return self._reactions[id]

    def add_reaction(self, id, parameters) -> None:
        self._reactions[id] = Reaction(id, **parameters)
