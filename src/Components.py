class Component:
    def __init__(self, name: str, molar_mass, molecular, formula):
        """This class defines the component and its properties"""
        self.name = name
        self.molar_mass = molar_mass
        self.ratio = 0.0
        self.mol_fraction = 0.0
        self.mol = 0.0
        self.mass = 0.0
        self.mass_fraction = 0.0
        self.molecular = bool(molecular)
        self.formula = formula
        self.concentration = 0.0
        self.iter = -1

    def calculate_concentration(self, section):
        """Calculate concentration of component in the mixture in section"""
        R = 8.31432
        return self.mol_fraction * section.pressure_inlet / (R * (section.temperature_inlet + 273.15))

    def set_ratio(self, value: float):
        try:
            self.ratio = float(value)
        except ValueError:
            self.ratio = 0


class Components:
    """This class has all components as objects of class Component"""

    def __init__(self):
        self.components = {}

    def data_table_components(self):
        table_data = []
        for name, component in self.components.items():
            if component.molecular:
                table_data.append([f'{component.name}',
                                   f'{component.molar_mass:.2f}',
                                   f'{component.mol_fraction:.4f}',
                                   f'{component.mol:.2f}',
                                   f'{component.mass:.2f}',
                                   f'{component.mass_fraction:.4f}'])
        return table_data

    def data_table_main(self):
        table_data = []
        for name, component in self.components.items():
            if component.molecular:
                table_data.append([f'{component.name}',
                                   f'{component.mol_fraction:.4f}',
                                   f'{component.mass_fraction:.4f}'])
        return table_data

    # -------------------------------------GETTERS-------------------------------------
    def summary_mol_fraction(self) -> float:
        """Get summary mole fraction from all components."""
        mol_fr = 0
        for component in self.components.values():
            mol_fr += component.mol_fraction
        return mol_fr  # = 1, when working correctly

    def summary_mol_flow(self) -> float:
        """Get summary molar flow."""
        molar_flow = 0
        for component in self.components.values():
            molar_flow += component.mol
        return molar_flow

    def summary_mass_flow(self) -> float:
        """Get summary mass flow."""
        mass_flow = 0
        for component in self.components.values():
            mass_flow += component.mol * component.molar_mass
        return mass_flow  # must be constant, when working correctly

    def summary_mass_fraction(self) -> float:
        """Get summary mass fraction from all components.
        When working correctly, the return is equal to 1."""
        mass_fr = 0
        for component in self.components.values():
            mass_fr += component.mass_fraction
        return mass_fr  # = 1, when working correctly

    def summary_concentration(self) -> float:
        inlet = 0
        for component in self.components.values():
            inlet += component.concentration
        return inlet

    # -------------------------------------SETTERS-------------------------------------
    def set_mol_fr(self):
        """Set mole fraction for each component from value of component_ratio"""
        ratio_summary = 0
        for component in self.components.values():
            ratio_summary += component.ratio
        if ratio_summary != 0:
            for component in self.components.values():
                component.mol_fraction = component.ratio / ratio_summary

    def set_mol_flow(self, molar_flow: float):
        """Set mole flow for each component from value of component_mol_fraction"""
        for component in self.components.values():
            component.mol = component.mol_fraction * molar_flow

    def set_mass_flow(self):
        """Set mass flow for each component from value of component_mol"""
        for component in self.components.values():
            component.mass = component.mol * component.molar_mass

    def set_mass_fr(self):
        """Set mass fraction for each component from value of component_mass"""
        mass_flow = self.summary_mass_flow()
        for component in self.components.values():
            if mass_flow != 0:
                component.mass_fraction = component.mass / mass_flow

    def update_properties(self, molar_flow: float = 10):
        """Updating the composition of flow components"""
        self.set_mol_flow(molar_flow)
        self.set_mass_flow()
        self.set_mass_fr()

    # -------------------------------------OTHER-------------------------------------
    def get_component(self, name: str) -> Component:
        """Get object Component with name = name"""
        return self.components[name]

    def add_component(self, name: str, properties: dict):
        self.components[name] = Component(**properties)
