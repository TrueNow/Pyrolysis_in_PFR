class VolumeFlow:

    @staticmethod
    def calc(molarFlow, temp, press):
        R = 8.31432
        return molarFlow * R * (temp + 273.15) / press
