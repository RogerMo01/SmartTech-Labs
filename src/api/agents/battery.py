class Battery:
    def __init__(self):
        self.percent_battery = 100
        self.is_charging = False

    def decrease_battery(self, percent):
        self.percent_battery = self.percent_battery - percent

    def increase_battery(self):
        self.percent_battery += 0.007

        if self.percent_battery >= 100:
            self.percent_battery = 100
         
    def __str__(self) -> str:
        return f"Battery: {self.percent_battery}%"
    def __repr__(self) -> str:
        return self.__str__()