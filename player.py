

class player:
    def __init__(self, fc, vp, combo, name, time):
        self.name = name
        self.vp = vp
        self.combo = combo
        self.fc = fc
        self.time = time
    
    def dict(self):
        return {
            "name":  self.name,
            "vp":    self.vp,
            "combo": self.combo,
            "fc":    self.fc,
            "time":    self.time,

        }

    def __repr__(self) -> str:
        return f"player(fc={self.fc}, vp={self.vp}, combo={self.combo}, name={self.name})"
    
    def __str__(self) -> str:
        return f"player {self.name} with {self.vp} VP running {self.combo}"