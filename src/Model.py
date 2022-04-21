from src.Saver import Saver


class Model:
    def __init__(self, reactions, components, cascade):
        self._reactions = reactions
        self._components = components
        self._cascade = cascade
        save = Saver(self)

        start_row = 1
        for name, reactor in self._cascade.get_cascade().items():
            section = reactor.get_section()

            self._components.calculate_components(section.molar_flow_in)

            save.init_in_xlsx(start_row)
            save.reactor_in_xlsx(reactor)

            self.calculate_section(section)

            self._components.calculate_components(section.molar_flow_out)

            save.result_in_xlsx()

            start_row += (len(self._components.get_components()) + 6)

    def calculate_section(self, section):
        while section.next() is True:
            concentration_inlet = {}
            for name, component in self._components.get_components().items():
                concentration_inlet[name] = component.calc_concentration(section)

            concentration_outlet = dict.copy(concentration_inlet)
            total_concentration_inlet = sum(concentration_inlet.values())

            for reaction in self._reactions.get_reactions().values():
                result = reaction.calculate(self._components, section)
                for name, delta in result.items():
                    concentration_outlet[name] += delta
                    if concentration_outlet[name] < 0:
                        print(f'Концентрация {name} меньше нуля!')
                        exit('Ну вот и все...')

            total_concentration_outlet = sum(concentration_outlet.values())
            for name, component in self._components.get_components().items():
                component.mol_fr = concentration_outlet[name] / total_concentration_outlet
            section.molar_flow_out = section.molar_flow_in * total_concentration_outlet / total_concentration_inlet

    def get_cascade(self):
        return self._cascade

    def get_reactions(self):
        return self._reactions

    def get_components(self):
        return self._components
