import datetime
from src.Saver import Saver


class Model:
    def __init__(self, reactions, components, cascade):
        self.__reactions = reactions
        self.__components = components
        self.__cascade = cascade
        self.__section = None
        save = Saver(self, 'example.xlsx')

        for number, reactor in self.__cascade.get_cascade().items():
            save.init_in_xlsx(number)
            self.calculate(reactor)
            save.reactor_in_xlsx(number)
            save.result_in_xlsx(number)

            try:
                self.__cascade.get_reactor(number + 1).molar_flow_in = self.get_section().molar_flow_out
            except KeyError:
                pass

    def calculate(self, reactor):
        self.__section = reactor.create_section()
        self.calculate_section()

    def calculate_section(self):
        while self.__section.next() is True:
            concentration_inlet = {}
            for name, component in self.__components.get_components().items():
                concentration_inlet[name] = self.__section.calc_component_concentration(self, name)

            concentration_outlet = dict.copy(concentration_inlet)
            total_concentration_inlet = sum(concentration_inlet.values())

            temp = self.__section.temp_in
            tay = self.__section.tay
            for reaction in self.__reactions.get_reactions().values():
                result = reaction.calculate(self, temp, tay)
                for name, delta in result.items():
                    concentration_outlet[name] += delta
                    if concentration_outlet[name] < 0:
                        print(f'Концентрация {name} меньше нуля!')
                        exit('Ну вот и все...')

            total_concentration_outlet = sum(concentration_outlet.values())
            for name, component in self.__components.get_components().items():
                component.mol_fr = concentration_outlet[name] / total_concentration_outlet
            self.__section.molar_flow_out = self.__section.molar_flow_in * total_concentration_outlet / total_concentration_inlet

            if not self.__section.count % int(str(self.__section.numberOfSections)[:-2]):
                print(f'{(self.__section.count / int(str(self.__section.numberOfSections)[:-2]))} % {datetime.datetime.now()}')

    def get_cascade(self):
        return self.__cascade

    def get_section(self):
        return self.__section

    def get_reactions(self):
        return self.__reactions

    def get_components(self):
        return self.__components

    def get_result_flow(self):
        result = {}
        for name, component in self.__components.get_used_components().items():
            result[name] = component.mol_fr
        return result
