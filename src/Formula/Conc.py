

class Conc:

    @staticmethod
    def calc(molarFraction, temp, press):
        R = 8.31432
        T = temp + 273.15
        return molarFraction * press / (R * T)
