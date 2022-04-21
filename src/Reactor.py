class Cascade:
    def __init__(self, cascade, filename):
        self.layout = []
        self.cascade = {}
        self.filename = filename
        for name, reactor in cascade.items():
            self.cascade[name] = Reactor(reactor)
        self.set_cascade_layout()

    def set_cascade_layout(self):
        for name, reactor in self.cascade.items():
            self.layout.append(
                [
                    self.cascade[name].name,
                    self.cascade[name].temp_in, self.cascade[name].temp_out,
                    self.cascade[name].press_in, self.cascade[name].press_out,
                    self.cascade[name].volume,
                    f'{self.cascade[name].steps:.1e}'
                ]
            )

    def get_cascade_layout(self):
        return self.layout

    def get_cascade(self):
        return self.cascade

    def get_reactor(self, name):
        return self.cascade[name]


class Reactor:
    def __init__(self, reactor):
        self._name = reactor['Наименование']
        self._temp_in = reactor['Температура вход']
        self._temp_out = reactor['Температура выход']
        self._press_in = reactor['Давление вход']
        self._press_out = reactor['Давление выход']
        self._volume = reactor['Объем']
        self._steps = reactor['Кол-во шагов']
        self._molar_flow_in = reactor['Мольный расход']
        self._residence_time = 0
        self._section = Section(self)

    @property
    def name(self):
        return self._name

    @property
    def temp_in(self):
        return self._temp_in

    @property
    def temp_out(self):
        return self._temp_out

    @property
    def press_in(self):
        return self._press_in

    @property
    def press_out(self):
        return self._press_out

    @property
    def volume(self):
        return self._volume

    @property
    def steps(self):
        return self._steps

    @property
    def residence_time(self):
        return self._residence_time

    @residence_time.setter
    def residence_time(self, value: float):
        self._residence_time = value

    @property
    def molar_flow_in(self):
        return self._molar_flow_in

    @molar_flow_in.setter
    def molar_flow_in(self, value: float):
        self._molar_flow_in = value

    def get_section(self):
        return self._section


class Section:
    _count = 0
    _timeCount = 0

    def __init__(self, reactor):
        self.reactor = reactor
        self._number_of_sections = reactor.steps
        self._molar_flow_in = reactor.molar_flow_in
        self._molar_flow_out = self._molar_flow_in

        self._tempIn = reactor.temp_in
        self._tempDelta = (reactor.temp_out - reactor.temp_in) / self._number_of_sections
        self._tempOut = self._tempIn

        self._pressIn = reactor.press_in
        self._pressDelta = (reactor.press_out - reactor.press_in) / self._number_of_sections
        self._pressOut = self._pressIn

        self._volume = reactor.volume / self._number_of_sections
        self._tay = 0
        self._volumeFlow = 0

    def next(self):
        if self._count >= self._number_of_sections:
            return False
        self._molar_flow_in = self._molar_flow_out

        self._tempIn = self._tempOut
        self._tempOut += self._tempDelta

        self._pressIn = self._pressOut
        self._pressOut += self._pressDelta

        self._volumeFlow = self.calc_volume_flow(molarFlow=self._molar_flow_in, temp=self._tempIn,
                                                 press=self._pressIn)

        self._tay = self._volume / self._volumeFlow
        self._count += 1
        self.reactor.residence_time += self._tay
        percent = self._count / self._number_of_sections * 100
        if percent in [20, 40, 60, 80, 100]:
            print(f'Статус расчета {int(percent)} %')
        return True

    @staticmethod
    def calc_volume_flow(molarFlow, temp, press):
        R = 8.31432
        return molarFlow * R * (temp + 273.15) / press

    @property
    def molar_flow_in(self):
        return self._molar_flow_in

    @molar_flow_in.setter
    def molar_flow_in(self, value: float):
        self._molar_flow_in = value

    @property
    def molar_flow_out(self):
        return self._molar_flow_out

    @molar_flow_out.setter
    def molar_flow_out(self, value: float):
        self._molar_flow_out = value

    @property
    def temp_in(self):
        return self._tempIn

    @property
    def temp_out(self):
        return self._tempOut

    @property
    def press_in(self):
        return self._pressIn

    @property
    def press_out(self):
        return self._pressOut

    @property
    def volume(self):
        return self._volume

    @property
    def tay(self):
        return self._tay

    @property
    def time_count(self):
        return self._timeCount

    @property
    def count(self):
        return self._count

    @property
    def numberOfSections(self):
        return self._number_of_sections
