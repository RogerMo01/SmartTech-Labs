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
         