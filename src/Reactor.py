class Section:
    """Section in the reactor for step-by-step calculation"""

    def __init__(self, reactor):
        self.reactor = reactor

        self.current_section = 0
        self.number_of_sections = self.reactor.number_of_sections

        self.molar_flow = self.reactor.molar_flow

        self.temperature_delta = self.reactor.temperature_delta
        self.temperature_inlet = self.reactor.temperature_inlet
        self.temperature_outlet = self.temperature_inlet

        self.pressure_delta = self.reactor.pressure_delta
        self.pressure_inlet = self.reactor.pressure_inlet
        self.pressure_outlet = self.pressure_inlet

        self.volume = self.reactor.volume / self.number_of_sections

        self.time = 0
        self.volume_flow = 0

    def next(self) -> bool:
        if self.current_section >= self.number_of_sections:
            return False

        self.temperature_inlet = self.temperature_outlet
        self.temperature_outlet += self.temperature_delta

        self.pressure_inlet = self.pressure_outlet
        self.pressure_outlet += self.pressure_delta

        self.volume_flow = self.calculate_volume_flow()

        self.time = self.volume / self.volume_flow

        self.current_section += 1
        self.reactor.time += self.time

        percent = self.current_section / self.number_of_sections * 100
        if percent in [20, 40, 60, 80, 100]:
            print(f'Статус расчета {int(percent)} %')
        return True

    def calculate_volume_flow(self) -> float:
        R = 8.31432
        return self.molar_flow * R * (self.temperature_inlet + 273.15) / self.pressure_inlet


class Reactor:
    def __init__(self, name, temp_in, temp_out, press_in, press_out, molar_flow_in, volume, steps):
        self.name = name
        self.temperature = [temp_in, temp_out, (temp_out - temp_in) / steps]
        self.pressure = [press_in, press_out, (press_out - press_in) / steps]
        self.molar_flow = molar_flow_in
        self.volume = volume
        self.number_of_sections = int(steps)
        self.time = 0

        self.section = Section(self)

    def __repr__(self):
        return f'_____{self.name}_____\n' \
               f'Temperature: {self.temperature}\n' \
               f'Pressure: {self.pressure}\n' \
               f'Molar flow: {self.molar_flow}\n' \
               f'Volume: {self.volume}\n' \
               f'Steps: {self.number_of_sections}\n'

    def get_section(self):
        return self.section

    @property
    def temperature_inlet(self):
        return self.temperature[0]

    @temperature_inlet.setter
    def temperature_inlet(self, value):
        self.temperature[0] = value

    @property
    def temperature_outlet(self):
        return self.temperature[1]

    @temperature_outlet.setter
    def temperature_outlet(self, value):
        self.temperature[1] = value

    @property
    def temperature_delta(self):
        return self.temperature[2]

    @property
    def pressure_inlet(self):
        return self.pressure[0]

    @pressure_inlet.setter
    def pressure_inlet(self, value):
        self.pressure[0] = value

    @property
    def pressure_outlet(self):
        return self.pressure[1]

    @pressure_outlet.setter
    def pressure_outlet(self, value):
        self.pressure[1] = value

    @property
    def pressure_delta(self):
        return self.pressure[2]


class Cascade:
    def __init__(self, filename):
        self.cascade = {}
        self.filename = filename

    def __repr__(self) -> str:
        cascade = []
        for reactor in self.cascade.values():
            cascade.append(reactor.__repr__())
        return ''.join(cascade)

    def get_reactor(self, name) -> Reactor:
        return self.cascade[name]

    def data_table(self) -> list:
        data = []
        for reactor in self.cascade.values():
            data.append([reactor.name,
                         f'{reactor.temperature_inlet:.1f}-{reactor.temperature_outlet:.1f}',
                         f'{reactor.pressure_inlet:.1f}-{reactor.pressure_outlet:.1f}',
                         f'{reactor.volume:.1f}', f'{reactor.number_of_sections:.0f}'])
        return data

    def add_reactor(self, name, parameters) -> None:
        self.cascade[name] = Reactor(**parameters)
