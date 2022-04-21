from DATA.components.read_components import read_components_from_xlsx


class Components:
    def __init__(self, components):
        all_components = read_components_from_xlsx()
        self._components = {}
        for name, parameters in all_components.items():
            if name in components:
                self._components[name] = Component(name, parameters)

    def get_mol_fr(self):
        mol_fr = 0
        for component in self._components.values():
            mol_fr += component.mol_fr
        return mol_fr

    def set_mol_fr(self):
        mol_fr = 0
        for component in self._components.values():
            mol_fr += component.ratio
        if mol_fr != 0:
            for component in self._components.values():
                component.mol_fr = component.ratio / mol_fr

    def get_mol_flow(self):
        molar_flow = 0
        for component in self._components.values():
            molar_flow += component.mol
        return molar_flow

    def set_mol_flow(self, molar_flow=0):
        for component in self._components.values():
            component.mol = component.mol_fr * molar_flow

    def get_mass_flow(self):
        mass_flow = 0
        for component in self._components.values():
            mass_flow += component.mol * component.molar_mass
        return mass_flow

    def set_mass_flow(self):
        for component in self._components.values():
            component.mass = component.mol * component.molar_mass

    def get_mass_fr(self):
        mass_fr = 0
        for component in self._components.values():
            mass_fr += component.mass_fr
        return mass_fr

    def set_mass_fr(self):
        mass_flow = self.get_mass_flow()
        for component in self._components.values():
            if mass_flow != 0:
                component.mass_fr = component.mass / mass_flow

    def calculate_components(self, molar_flow=10):
        """Расчет компонентоного состава"""
        self.set_mol_fr()
        self.set_mol_flow(molar_flow)
        self.set_mass_flow()
        self.set_mass_fr()

    def get_component(self, name: str):
        return self._components[name]

    def get_components(self):
        return self._components


class Component:
    def __init__(self, name: str, parameters: dict):
        self._name = str(name)
        self._molarMass = parameters['Молярная масса']
        self._ratio = parameters['Мольная доля']
        self._molFr = 0.0
        self._mol = 0.0
        self._mass = 0.0
        self._massFr = 0.0
        self._type = bool(parameters['Молекула'])
        self._formula = str(parameters['Формула'])

    def calc_concentration(self, section):
        R = 8.31432
        T = section.temp_in + 273.15
        P = section.press_in
        return self.mol_fr * P / (R * T)

    @property
    def molar_mass(self):
        return self._molarMass

    @property
    def ratio(self):
        return self._ratio

    @ratio.setter
    def ratio(self, value: float):
        try:
            if float(value) > 0:
                self._ratio = float(value)
        except ValueError:
            self._ratio = 0

    @property
    def mol_fr(self):
        return self._molFr

    @mol_fr.setter
    def mol_fr(self, value):
        self._molFr = value

    @property
    def mol(self):
        return self._mol

    @mol.setter
    def mol(self, value):
        self._mol = value

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        self._mass = value

    @property
    def mass_fr(self):
        return self._massFr

    @mass_fr.setter
    def mass_fr(self, value: float):
        self._massFr = value

    @property
    def type(self):
        return self._type

    @property
    def formula(self):
        return self._formula
