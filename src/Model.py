import datetime
from src.Saver import Saver


class Model:
    def __init__(self, reactions, components, cascade):
        self._reactions = reactions
        self._components = components
        self._cascade = cascade
        self._section = None
        save = Saver(self)

        molar_flow_out = None

        start_row = 1
        for name, reactor in self._cascade.get_cascade().items():
            if molar_flow_out is not None:
                self._cascade.get_reactor(name).molar_flow_in = molar_flow_out
            self._components.calculate_fractions(self._cascade.get_reactor(name).molar_flow_in)
            save.init_in_xlsx(start_row)
            self.calculate(reactor)
            save.reactor_in_xlsx(reactor)
            self._components.calculate_fractions(self.get_section().molar_flow_out)
            save.result_in_xlsx()

            molar_flow_out = self.get_section().molar_flow_out
            start_row += (len(self._components.get_components()) + 5)

    def calculate(self, reactor):
        self._section = reactor.create_section()
        self.calculate_section()

    def calculate_section(self):
        while self._section.next() is True:
            concentration_inlet = {}
            for name, component in self._components.get_components().items():
                concentration_inlet[name] = self._section.calc_component_concentration(self, name)

            concentration_outlet = dict.copy(concentration_inlet)
            total_concentration_inlet = sum(concentration_inlet.values())

            temp = self._section.temp_in
            tay = self._section.tay
            for reaction in self._reactions.get_reactions().values():
                result = reaction.calculate(self, temp, tay)
                for name, delta in result.items():
                    concentration_outlet[name] += delta
                    if concentration_outlet[name] < 0:
                        print(f'Концентрация {name} меньше нуля!')
                        exit('Ну вот и все...')

            total_concentration_outlet = sum(concentration_outlet.values())
            for name, component in self._components.get_components().items():
                component.ratio = concentration_outlet[name] / total_concentration_outlet
                component.mol_fr = component.ratio
            self._section.molar_flow_out = self._section.molar_flow_in * total_concentration_outlet / total_concentration_inlet

        for name, params in self._components.get_components().items():
            print(name, params.mol_fr)
            # if not self._section.count % int(str(self._section.numberOfSections)[:-2]):
            #     print(f'{(self._section.count / int(str(self._section.numberOfSections)[:-2]))} % {datetime.datetime.now()}')

    def get_cascade(self):
        return self._cascade

    def get_section(self):
        return self._section

    def get_reactions(self):
        return self._reactions

    def get_components(self):
        return self._components

    def get_result_flow(self):
        result = {}
        for name, component in self._components.get_components().items():
            result[name] = component.mol_fr
        return result
