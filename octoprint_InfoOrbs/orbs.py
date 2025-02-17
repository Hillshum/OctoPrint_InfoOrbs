
class Orb:

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

    def __init__(self, temp: dict):
        self.temp = temp

    def render(self):
        temps = [format_temp(k, v) for k, v in self.temp.items() if v["actual"] is not None]

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
    
    def __init__(self, url: str):
        self.url = url

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
    
    def __init__(self, filename: str):
        self.filename = filename

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

    def __init__(self, status: dict):
        self.status = status

    def render(self):
        remaining = self.status["progress"]["printTimeLeft"]
        elapsed = self.status["progress"]["printTime"]
        progress = self.status["progress"]["completion"]

        remaining_str = "--:--"
        elapsed_str = "--:--"
        if remaining: 
            remaining_str = f"{remaining // 3600:02}:{remaining // 60 % 60:02}"
        if elapsed:
            elapsed_str = f"{elapsed // 3600:02}:{elapsed // 60 % 60:02}"

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

