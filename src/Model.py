from src.Saver import Saver
from src.Reactions import Reactions
from src.Flow import Flow
from src.Reactor import Cascade, Section

from src.Flow import MOL


class Model:
    row_composition_inlet = 1
    col_composition_inlet = 3
    col_time = 2

    def __init__(self, reactions: Reactions, flow: Flow, cascade: Cascade):
        self._reactions = reactions
        self._flow = flow
        self._cascade = cascade
        self.save = Saver(self)

    def save_composition(self):
        data_composition = self._flow.data_composition()
        self.save.write_in_xlsx(data_composition, self.row_composition_inlet, self.col_composition_inlet, self.save.sheet_result)
        self.col_composition_inlet += 5

    def save_mass_fraction(self, time_cascade=None):
        if time_cascade is None:
            time_cascade = 0
        mass_fraction_list = self._flow.data_composition_mass_fraction()
        mass_fraction_list[0].append(time_cascade)
        self.save.write_in_xlsx(mass_fraction_list, start_row=1, start_col=self.col_time, sheet=self.save.sheet_time)
        self.col_time += 1

    def calculate(self):
        self.save_composition()

        for reactor in self._cascade.get_reactors():
            section = reactor.section
            section.total_concentration_outlet = 0
            for component in self._flow.get_composition():
                reactor.molar_flow += component.mol
                component.concentration = component.calculate_concentration(section.temperature_out, section.pressure_out)
                section.total_concentration_outlet += component.concentration

            section.molar_flow = reactor.molar_flow

            while section.next():  # and reactor.resident_time < 0.1:
                self.calculate_section(section)
                # progress = (section.current_section * 100) / reactor.sections_count
                # if progress in [1, 20, 40, 60, 80]:
                #     print(f'Прогресс: {progress}%')

                reactor.resident_time += section.resident_time
                self._cascade.resident_time += section.resident_time
                c_t = self._cascade.resident_time
                if abs(c_t - round(c_t, 2)) < 0.00001:
                    self._flow.update_composition(section.molar_flow, 'mol')
                    self.save_mass_fraction(c_t)

            # section.total_concentration_outlet = self._flow.summary_concentration()
            for component in self._flow.get_composition():
                if component.concentration != 0:
                    component.mol_fraction = component.concentration / section.total_concentration_outlet
            self._flow.update_composition(value_flow=section.molar_flow, type_flow=MOL)

            self.save_composition()
            self.save.reactor(reactor)

        self.save.save()

    def calculate_section(self, section: Section):
        volume_flow = self._flow.calculate_volume(section.molar_flow, section.temperature, section.pressure)
        section.resident_time = section.volume / volume_flow

        delta_concentration = {}
        for reaction in self._reactions.get_reactions():
            rate = reaction.calculate_rate(self._flow, section.temperature)
            for component_name, coefficient, _ in reaction.components_reaction:
                try:
                    delta_concentration[component_name] += (coefficient * rate * section.resident_time)
                except KeyError:
                    delta_concentration[component_name] = (coefficient * rate * section.resident_time)

        section.total_concentration_outlet = 0
        for component_name, delta in delta_concentration.items():
            component = self._flow.get_component(component_name)
            component.concentration += delta
            section.total_concentration_outlet += component.concentration
            if component.concentration < 0:
                print(f'Концентрация {component.name} меньше нуля!')
                exit('Ну вот и все...')

        for component in self._flow.get_composition():
            component.mol_fraction = component.concentration / section.total_concentration_outlet

        section.molar_flow *= (section.total_concentration_outlet / section.total_concentration_inlet)

    def get_reactions(self):
        return self._reactions

    def get_flow(self):
        return self._flow

    def get_cascade(self):
        return self._cascade
