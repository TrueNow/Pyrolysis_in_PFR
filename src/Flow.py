RATIO = 'ratio'
MOL, MASS, VOL = 'mol', 'mass', 'volume'
MOL_FR, MASS_FR, VOL_FR = 'mol_fraction', 'mass_fraction', 'vol_fraction'
CONC = 'concentration'


class Component:
    def __init__(self, name: str, molar_mass: float, molecular: float, formula: str):
        """This class defines the component and its properties"""
        self._name = name
        self._molar_mass = molar_mass
        self._fractions = {
            'ratio': 0.0,
            'mol_fraction': 0.0,
            'mass_fraction': 0.0,
            'vol_fraction': 0.0,
            'mol': 0.0,
            'mass': 0.0,
            'volume': 0.0,
            'concentration': 0.0,
        }
        self._molecular = bool(molecular)
        self._formula = formula

    def __str__(self):
        return f'{self._name} {self._formula}\n' \
               f'Mol_fr:  {self._fractions[MOL_FR]:.4f}    Mol:  {self._fractions[MOL]:.1f}\n' \
               f'Mass_fr: {self._fractions[MASS_FR]:.4f}    Mass: {self._fractions[MASS]:.1f}\n' \
               f'Vol_fr:  {self._fractions[VOL_FR]:.4f}    Vol:  {self._fractions[VOL]:.1f}\n' \
               f'{"-" * 50}'

    def is_molecular(self) -> bool:
        return self._molecular

    # -------------------------------------CALCULATE-------------------------------------
    def calculate_concentration(self, pressure=101.325, temperature=25) -> None:
        """Calculate concentration of component in the mixture in section"""
        R = 8.31432
        self._fractions[CONC] = self.mol_fraction * pressure / (R * (temperature + 273.15))

    def calculate_volume(self, pressure=101.325, temperature=25) -> None:
        R = 8.31432
        self._fractions[VOL] = self.mol * pressure / (R * (temperature + 273.15))

    # -------------------------------------CONSTANT PROPERTIES-------------------------------------
    @property
    def name(self) -> str:
        return self._name

    @property
    def fractions(self) -> dict:
        return self._fractions

    @property
    def molar_mass(self) -> float:
        return self._molar_mass

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
        return self._fractions[MOL_FR]

    @mol_fraction.setter
    def mol_fraction(self, value: float):
        self._fractions[MOL_FR] = value

    @property
    def mass_fraction(self):
        return self._fractions[MASS_FR]

    @mass_fraction.setter
    def mass_fraction(self, value: float):
        self._fractions[MASS_FR] = value

    @property
    def vol_fraction(self):
        return self._fractions[VOL_FR]

    @vol_fraction.setter
    def vol_fraction(self, value: float):
        self._fractions[VOL_FR] = value

    @property
    def mol(self):
        return self._fractions[MOL]

    @mol.setter
    def mol(self, value: float):
        self._fractions[MOL] = value

    @property
    def mass(self):
        return self._fractions[MASS]

    @mass.setter
    def mass(self, value: float):
        self._fractions[MASS] = value

    @property
    def volume(self):
        return self._fractions[VOL]

    @volume.setter
    def volume(self, value: float):
        self._fractions[VOL] = value

    @property
    def concentration(self):
        return self._fractions[CONC]

    @concentration.setter
    def concentration(self, value: float):
        self._fractions[CONC] = value


class Flow:
    """This class has all components as objects of class Component"""

    def __init__(self):
        self._components = {}

    def __str__(self):
        return f'{" ".join(self._components.values())}'

    def get_components(self) -> dict:
        """Get dict of used components in Flow._components"""
        return self._components

    def get_component(self, name: str) -> Component:
        """Get object Component with name = name"""
        return self._components[name]

    def add_component(self, name: str, properties: dict):
        self._components[name] = Component(name, **properties)

    def summary_parameter(self, parameter: str) -> float:
        """
        Get parameter's sum from all components.
        Parameter must be equal 'ratio', 'mol_fraction', 'mass_fraction',
        'vol_fraction', 'mol', 'mass', 'volume', 'concentration'.
        """
        return sum(component.fractions[parameter] for component in self._components.values())

    # -------------------------------------SETTERS-------------------------------------
    def set_fraction(self, parameter):
        ratio_summary = self.summary_parameter(RATIO)

        if ratio_summary:
            for component in self._components.values():
                component.fractions[parameter] = component.ratio / ratio_summary

        if parameter == MOL_FR:
            self.from_mol_to_vol_and_mass()
        elif parameter == MASS_FR:
            self.from_mass_to_vol_and_mol()
        elif parameter == VOL_FR:
            self.from_vol_to_mol_and_mass()

    def from_mol_to_vol_and_mass(self):
        for component in self._components.values():
            component.vol_fraction = component.mol_fraction
            component.mass = component.mol_fraction / component.molar_mass
        mass = sum(component.mass for component in self._components.values())
        for component in self._components.values():
            component.mass_fraction = component.mass / mass
            component.mass = 0

    def from_mass_to_vol_and_mol(self):
        for component in self._components.values():
            component.mol = component.mass_fraction * component.molar_mass
        mol = sum(component.mol for component in self._components.values())
        for component in self._components.values():
            component.mol_fraction = component.mol / mol
            component.vol_fraction = component.mol_fraction
            component.mol = 0

    def from_vol_to_mol_and_mass(self):
        for component in self._components.values():
            component.mol_fraction = component.vol_fraction
            component.mass = component.vol_fraction / component.molar_mass
        mass = sum(component.mass for component in self._components.values())
        for component in self._components.values():
            component.mass_fraction = component.mass / mass
            component.mass = 0

    def update_composition(self, molar_flow: float = None,
                           mass_flow: float = None, volume_flow: float = None) -> None:
        """Updating the composition of components"""
        if molar_flow is not None:
            self.set_from_molar_flow(molar_flow)
        elif mass_flow is not None:
            self.set_from_mass_flow(mass_flow)
        elif volume_flow is not None:
            self.set_from_volume_flow(volume_flow)

    def set_from_molar_flow(self, flow):
        for component in self._components.values():
            component.mol = component.mol_fraction * flow
            component.mass = component.mol * component.molar_mass
            component.calculate_volume()
            component.calculate_concentration()

    def set_from_mass_flow(self, flow):
        for component in self._components.values():
            component.mass = component.mass_fraction * flow
            component.mol = component.mass / component.molar_mass
            component.calculate_volume()
            component.calculate_concentration()

    def set_from_volume_flow(self, flow):
        for component in self._components.values():
            component.volume = component.vol_fraction * flow
            component.mol = component.volume / 22.4
            component.mass = component.mol * component.molar_mass
            component.calculate_concentration()
