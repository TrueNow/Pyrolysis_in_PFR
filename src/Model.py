from src.Saver import Saver


class Model:
    def __init__(self, reactions, components, cascade):
        self._reactions = reactions
        self._components = components
        self._cascade = cascade

        save = Saver(self)

        for name, reactor in self._cascade.cascade.items():
            print(reactor)
            reactor.molar_flow = self._components.summary_mol_flow()
            section = reactor.section
            section.molar_flow = reactor.molar_flow

            save.init_in_xlsx()
            self.calculate_section(section)
            save.reactor_in_xlsx(reactor)
            self._components.update_properties(section.molar_flow)
            save.result_in_xlsx()

    def calculate_section(self, section):
        while section.next() is True:
            for name, component in self._components.components.items():
                component.concentration = component.calculate_concentration(section)

            total_concentration_inlet = self._components.summary_concentration()

            for reaction in self._reactions.reactions.values():
                result = reaction.calculate(self._components, section)
                for name, delta in result.items():
                    self._components.get_component(name).concentration += delta
                    if self._components.get_component(name).concentration < 0:
                        print(f'Концентрация {name} меньше нуля!')
                        exit('Ну вот и все...')

            total_concentration_outlet = self._components.summary_concentration()
            for name, component in self._components.components.items():
                component.mol_fraction = component.concentration / total_concentration_outlet
            section.molar_flow *= (total_concentration_outlet / total_concentration_inlet)

    def get_cascade(self):
        return self._cascade

    def get_reactions(self):
        return self._reactions

    def get_components(self):
        return self._components
