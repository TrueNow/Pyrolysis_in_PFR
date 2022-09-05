class Section:
    """Section in the reactor for step-by-step calculation"""
    molar_flow: float = 0
    resident_time: float = 0
    temperature: float
    pressure: float
    total_concentration_inlet: float
    total_concentration_outlet: float

    def __init__(self, reactor):
        self.temperature_out = reactor.temperature_inlet
        self.temperature_delta = reactor.temperature_delta

        self.pressure_out = reactor.pressure_inlet
        self.pressure_delta = reactor.pressure_delta

        self.current_section = 0
        self.number_last_section = reactor.sections_count
        self.volume = reactor.volume / self.number_last_section

    def next(self) -> bool:
        if self.current_section > self.number_last_section:
            return False
        self.temperature = self.temperature_out
        self.temperature_out += self.temperature_delta

        self.pressure = self.pressure_out
        self.pressure_out += self.pressure_delta

        self.total_concentration_inlet = self.total_concentration_outlet
        self.current_section += 1
        return True


class Reactor:
    molar_flow: float = 0
    resident_time: float = 0

    def __init__(self, name: str, volume: float, steps: int,
                 temp_in: float, temp_out: float,
                 press_in: float, press_out: float):
        self.name = name
        self.volume = volume
        self.sections_count = steps

        self.temperature_inlet = temp_in
        self.temperature_outlet = temp_out
        self.temperature_delta = (self.temperature_outlet - self.temperature_inlet) / self.sections_count
        self.temperature_string = f'{self.temperature_inlet}-{self.temperature_outlet}'

        self.pressure_inlet = press_in
        self.pressure_outlet = press_out
        self.pressure_delta = (self.pressure_outlet - self.pressure_inlet) / self.sections_count
        self.pressure_string = f'{self.pressure_inlet}-{self.pressure_outlet}'

        self.section = Section(self)

    def __str__(self):
        return f'_____{self.name}_____\n' \
               f'Temperature: {self.temperature_string}\n' \
               f'Pressure: {self.pressure_string}\n' \
               f'Volume: {self.volume}\n' \
               f'Steps: {self.sections_count}\n'


class Cascade:
    def __init__(self, filename):
        self._cascade = {}
        self.filename = filename
        self.resident_time = 0

    def __repr__(self) -> str:
        return ''.join([reactor for reactor in self.get_reactors()])

    # def get_reactor(self, name) -> Reactor:
    #     return self._cascade[name]

    def get_reactors(self):
        return self._cascade.values()

    def add_reactor(self, name, parameters) -> None:
        self._cascade[name] = Reactor(name, **parameters)
