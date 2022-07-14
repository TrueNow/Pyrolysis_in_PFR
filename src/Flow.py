RATIO = 'ratio'
MOL, MASS, VOL = 'mol', 'mass', 'volume'
CONC = 'concentration'


class Component:
    def __init__(self, name: str, molar_mass: float, molecular: float, formula: str):
        """This class defines the component and its properties"""
        self._name = name
        self._molar_mass = molar_mass
        self._molecular = bool(molecular)
        self._formula = formula
        self._fractions = {
            'ratio': 0.0,
            'mol': 0.0,
            'mass': 0.0,
        }
        self._flows = {
            'mol': 0.0,
            'mass': 0.0,
        }
        self._concentration = 0.0

    def __repr__(self):
        return f'{self._name}'

    def is_molecular(self) -> bool:
        return self._molecular

    # -------------------------------------CALCULATE-------------------------------------
    def calculate_mol(self, molar_flow=None) -> float:
        if molar_flow is None:
            return self.mass / self.molar_mass
        return self.mol_fraction * molar_flow

    def calculate_mass(self, mass_flow=None) -> float:
        if mass_flow is None:
            return self.mol * self.molar_mass
        return self.mass_fraction * mass_flow

    def calculate_concentration(self, temperature: float | int, pressure: float | int):
        """Calculate concentration of component in the mixture in section"""
        R = 8.31432  # кДж / (кмоль * К)
        T = temperature + 273.15  # К
        P = pressure  # кПа
        return self.mol_fraction * P / (R * T)

    # -------------------------------------CONSTANT PROPERTIES-------------------------------------
    @property
    def name(self) -> str:
        return self._name

    @property
    def molar_mass(self) -> float:
        return self._molar_mass

    @property
    def fractions(self) -> dict:
        return self._fractions

    @property
    def flows(self) -> dict:
        return self._flows

    @property
    def formula(self) -> str:
        return self._formula

    # -------------------------------------CHANGEABLE PROPERTIES-------------------------------------
    @property
    def ratio(self):
        return self._fractions[RATIO]

    @ratio.setter
    def ratio(self, value: float):
        self._fractions[RATIO] = value

    @property
    def mol_fraction(self):
        return self._fractions[MOL]

    @mol_fraction.setter
    def mol_fraction(self, value: float):
        self._fractions[MOL] = value

    @property
    def mass_fraction(self):
        return self._fractions[MASS]

    @mass_fraction.setter
    def mass_fraction(self, value: float):
        self._fractions[MASS] = value

    @property
    def concentration(self) -> float:
        return self._concentration

    @concentration.setter
    def concentration(self, value: float):
        self._concentration = value

    @property
    def mol(self):
        return self._flows[MOL]

    @mol.setter
    def mol(self, value: float):
        self._flows[MOL] = value

    @property
    def mass(self):
        return self._flows[MASS]

    @mass.setter
    def mass(self, value: float):
        self._flows[MASS] = value


class Components:
    def __init__(self):
        self._components = {}

    def __str__(self):
        return f'{" ".join(self._components)}'

    def get_components(self):
        """Get dict of used components in Flow._components"""
        return self._components.values()

    def get_component(self, name: str) -> Component:
        """Get object Component with name = name"""
        return self._components[name]

    def add_component(self, name: str, properties: dict) -> None:
        self._components[name] = Component(name, **properties)


class Flow:
    """This class has all components as objects of class Component"""
    def __init__(self, components: Components):
        self.composition = components

    def get_composition(self):
        return self.composition.get_components()

    def get_component(self, name: str) -> Component:
        """Get object Component with name = name"""
        return self.composition.get_component(name)

    def summary_fractions(self, parameter: str) -> float:
        """Get parameter's sum from all components. Parameter must be equal 'ratio', 'mol', 'mass', 'volume'."""
        return sum(component.fractions[parameter] for component in self.get_composition())

    def summary_flows(self, parameter: str) -> float:
        """Get parameter's sum from all components. Parameter must be equal 'mol', 'mass', 'volume'."""
        return sum(component.flows[parameter] for component in self.get_composition())

    def summary_concentration(self):
        return sum(component.concentration for component in self.get_composition())

    # -------------------------------------SETTERS-------------------------------------
    def set_fraction(self, parameter):
        ratio_summary = self.summary_fractions(RATIO)
        if ratio_summary:
            for component in self.get_composition():
                if component.ratio:
                    component.fractions[parameter] = component.ratio / ratio_summary
        if parameter == MASS:
            self.from_mass_fr_to_mol_fr()

    def from_mass_fr_to_mol_fr(self):
        for component in self.get_composition():
            component.mass = component.calculate_mass(100)
            component.mol = component.calculate_mol()
        self.calculate_mol_fr()

    def calculate_mol_fr(self):
        sum_mol = self.summary_flows(MOL)
        for component in self.get_composition():
            component.mol_fraction = component.mol / sum_mol

    @staticmethod
    def calculate_volume(molar_flow, temperature, pressure) -> float:
        R = 8.31432  # кДж / (кмоль * К)
        M = molar_flow  # кмоль / с
        T = temperature + 273.15  # К
        P = pressure  # кПа
        return M * R * T / P

    def update_composition(self, value_flow: float, type_flow: str) -> None:
        """Updating the composition of components"""
        if type_flow == MOL:
            for component in self.get_composition():
                component.mol = component.calculate_mol(value_flow)
                component.mass = component.calculate_mass()
            sum_mass = self.summary_flows(MASS)
            if sum_mass:
                for component in self.get_composition():
                    component.mass_fraction = component.mass / sum_mass

    def data_composition(self) -> list:
        composition_list = [['Кол-во, кмоль/с', 'Мол. доля', 'Масс. доля', 'Масса, кг/с']]
        last_row = [0, 0, 0, 0]
        for component in self.get_composition():
            composition_list.append([component.mol, component.mol_fraction, component.mass_fraction, component.mass])
            last_row[0] += component.mol
            last_row[1] += component.mol_fraction
            last_row[2] += component.mass_fraction
            last_row[3] += component.mass
        composition_list.append(last_row)
        return composition_list

    def data_composition_mass_fraction(self) -> list:
        composition_list = [[]]
        for component in self.get_composition():
            composition_list.append([component.mass_fraction])
        return composition_list
