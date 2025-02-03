

class TempOrb:

    def __init__(self, temp: dict):
        self.temp = temp["tool0"]["actual"]

    def render(self):
        return {
            "label": "Temp",
            "data": 0,
        }


class ProgressOrb:

    def render(self):
        return {
            "label": "Progress",
            "data": "24/100",
        }

