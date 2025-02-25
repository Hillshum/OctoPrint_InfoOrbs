import logging

class Orb:

    logger = None

    def __init__(self, logger=None):
        self.logger = logger

    def log(self, level, message, *args, **kwargs):
        if self.logger:
            self.logger.log(level, message, *args, **kwargs)

    def render(self):
        return {
            "data": {
                "background": "black",
            },
        }

def format_temp_label(label: str):
    label = label.replace("tool", "T")
    label = label.replace("bed", "B")
    return label

def format_temp(label: str, data: dict):
    return f"{format_temp_label(label)}: {data['actual']}C/{data['target']}C"

class TempOrb(Orb):

    def __init__(self, temp: dict, logger=None):
        self.temp = temp
        super().__init__(logger)

    def render(self):
        temps = [format_temp(k, v) for k, v in self.temp.items() if v["actual"] is not None]

        self.log(logging.DEBUG, f"Temps: {temps}")

        row = {
            "type": "text",
            "font": 1,
            "size": 30,
            "align": "center",
            "color": "white",
            "background": "black",
            "y": 100,
            "x": 110,
        }

        rows = []
        for temp in temps:
            row["text"] = temp
            row["y"] += 30
            rows.append(row.copy())

        return {
            "fullDraw": True,
            "data": rows
        }

class ImageOrb(Orb):

    def __init__(self, url: str, logger=None):
        self.url = url
        super().__init__(logger)

    def render(self):
        return {
            "fullDraw": True,
            "data": [
                {
                    "type": "image",
                    "x": 0,
                    "y": 0,
                    "width": 240,
                    "height": 240,
                    "imageUrl": self.url,
                }
            ]
        }

class StatusOrb(Orb):

    def __init__(self, filename: str, logger=None):
        self.filename = filename
        super().__init__(logger)

    def render(self):
        return {
            "fullDraw": True,
            "data": [
                {
                    "type": "text",
                    "background": "black",
                    "text": self.filename,
                    "color": "white",
                    "align": "center",
                    "font": 6,
                    "size": 10,
                    "x": 110,
                    "y": 100,
                }
            ]
        }

class ProgressOrb(Orb):

    def __init__(self, status: dict, logger=None):
        self.status = status
        super().__init__(logger)

    def render(self):
        remaining = self.status["progress"]["printTimeLeft"]
        elapsed = self.status["progress"]["printTime"]
        progress = self.status["progress"]["completion"]
        origin = self.status["progress"]["printTimeLeftOrigin"]

        self.log(
            logging.DEBUG,
            f"Progress: {progress}, Remaining: {remaining}, Elapsed: {elapsed}",
        )
        remaining_str = "--:--"
        elapsed_str = "--:--"
        if remaining is not None: 
            remaining_str = f"{remaining // 3600:02}:{remaining // 60 % 60:02}"
        if elapsed is not None:
            elapsed_str = f"{elapsed // 3600:02}:{elapsed // 60 % 60:02}"

        if origin == "genius":
            progress = elapsed / (remaining + elapsed) * 100
            self.log(logging.DEBUG, f"Calculated progress from PTG: {progress}")

        progress_arcs = []
        if progress:
            angle_end = int(progress / 100 * 360 + 180)
            arc = {
                "type": "arc",
                "x": 120,
                "y": 120,
                "radius": 120,
                "innerRadius": 100,
                "angleStart": 180,
                "angleEnd": angle_end,
                "color": "green",
            }
            progress_arcs.append(arc)

            if angle_end > 360:
                arc = {
                    "type": "arc",
                    "x": 120,
                    "y": 120,
                    "radius": 120,
                    "innerRadius": 100,
                    "angleStart": 0,
                    "angleEnd": angle_end - 360,
                    "color": "green",
                }
                progress_arcs.append(arc)

        return {
            "fullDraw": True,
            "data": [
                *progress_arcs,
                {
                    "type": "text",
                    "background": "black",
                    "text": elapsed_str,
                    "color": "white",
                    "alignment": "cc",
                    "font": 1,
                    "size": 60,
                    "x": 120,
                    "y": 90,
                },
                {
                    "type": "text",
                    "background": "black",
                    "text": "Elapsed",
                    "font": 1,
                    "size": 20,
                    "color": "white",
                    "alignment": "cc",
                    "x": 120,
                    "y": 50,
                },
                {
                    "type": "text",
                    "background": "black",
                    "text": "Remaining",
                    "font": 1,
                    "size": 20,
                    "color": "white",
                    "alignment": "cc",
                    "x": 120,
                    "y": 190,
                },
                {
                    "type": "text",
                    "background": "black",
                    "text": remaining_str,
                    "color": "white",
                    "alignment": "cc",
                    "font": 1,
                    "size": 60,
                    "x": 120,
                    "y": 150,
                },
            ]
        }


class StateOrb(Orb):

    def __init__(self, state, logger=None):
        self.state = state
        super().__init__(logger)

    def render(self):
        self.log(logging.DEBUG, f"Rendering state orb with state: {self.state}")
        return {
            "fullDraw": True,
            "data": [
                {
                    "type": "text",
                    "background": "black",
                    "text": self.state["text"],
                    "color": "white",
                    "align": "center",
                    "font": 6,
                    "size": 10,
                    "x": 110,
                    "y": 100,
                }
            ],
        }
