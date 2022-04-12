from DATA.reactor.read_reactor import read_reactor_from_xlsx

class Cascade:
    def __init__(self, cascade = read_reactor_from_xlsx()):
        self.cascade = {}
        for number, reactor in cascade.items():
            self.cascade[number] = Reactor(reactor)

    def get_cascade(self):
        return self.cascade

    def get_reactor(self, key):
        return self.cascade[key]


class Reactor:
    def __init__(self, reactor):
        self.__name = reactor['Наименование']
        self.__tempIn = reactor['Температура вход']
        self.__tempOut = reactor['Температура выход']
        self.__pressIn = reactor['Давление вход']
        self.__pressOut = reactor['Давление выход']
        self.__volume = reactor['Объем']
        self.__steps = reactor['Кол-во шагов']
        self.__molarFlowIn = reactor['Мольный расход']
        self.__section = None

    @property
    def name(self):
        return self.__name

    @property
    def temp_in(self):
        return self.__tempIn

    @property
    def temp_out(self):
        return self.__tempOut

    @property
    def press_in(self):
        return self.__pressIn

    @property
    def press_out(self):
        return self.__pressOut

    @property
    def volume(self):
        return self.__volume

    @property
    def steps(self):
        return self.__steps

    @property
    def molar_flow_in(self):
        return self.__molarFlowIn

    @molar_flow_in.setter
    def molar_flow_in(self, value: float):
        self.__molarFlowIn = value

    def create_section(self):
        self.__section = Section(self)
        return self.__section

    def get_section(self):
        return self.__section


class Section:
    __count = 0
    __timeCount = 0

    def __init__(self, reactor):
        self.__numberOfSections = reactor.steps
        self.__molarFlowIn = reactor.molar_flow_in
        self.__molarFlowOut = self.__molarFlowIn

        self.__tempIn = reactor.temp_in
        self.__tempDelta = (reactor.temp_out - reactor.temp_in) / self.__numberOfSections
        self.__tempOut = self.__tempIn

        self.__pressIn = reactor.press_in
        self.__pressDelta = (reactor.press_out - reactor.press_in) / self.__numberOfSections
        self.__pressOut = self.__pressIn

        self.__volume = reactor.volume / self.__numberOfSections
        self.__tay = 0
        self.__volumeFlow = 0

    def next(self):
        if self.__count >= self.__numberOfSections:
            return False
        self.__molarFlowIn = self.__molarFlowOut

        self.__tempIn = self.__tempOut
        self.__tempOut += self.__tempDelta

        self.__pressIn = self.__pressOut
        self.__pressOut += self.__pressDelta

        self.__volumeFlow = self.calc_volume_flow(molarFlow=self.__molarFlowIn, temp=self.__tempIn, press=self.__pressIn)

        self.__tay = self.__volume / self.__volumeFlow
        self.__count += 1
        self.__timeCount += self.__tay
        return True

    @staticmethod
    def calc_volume_flow(molarFlow, temp, press):
        R = 8.31432
        return molarFlow * R * (temp + 273.15) / press

    def calc_component_concentration(self, model, name: str):
        molarFraction = model.get_components().get_component(name).mol_fr
        R = 8.31432
        T = self.temp_in + 273.15
        P = self.press_in
        return molarFraction * P / (R * T)

    @property
    def molar_flow_in(self):
        return self.__molarFlowIn

    @molar_flow_in.setter
    def molar_flow_in(self, value: float):
        self.__molarFlowIn = value

    @property
    def molar_flow_out(self):
        return self.__molarFlowOut

    @molar_flow_out.setter
    def molar_flow_out(self, value: float):
        self.__molarFlowOut = value

    @property
    def temp_in(self):
        return self.__tempIn

    @property
    def temp_out(self):
        return self.__tempOut

    @property
    def press_in(self):
        return self.__pressIn

    @property
    def press_out(self):
        return self.__pressOut

    @property
    def volume(self):
        return self.__volume

    @property
    def tay(self):
        return self.__tay

    @property
    def time_count(self):
        return self.__timeCount

    @property
    def count(self):
        return self.__count

    @property
    def numberOfSections(self):
        return self.__numberOfSections
