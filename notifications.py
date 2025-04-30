
class Notification:
    text: str
    lifetime: int
    def __init__(self, text, lifetime):
        self.text = text
        self.lifetime = lifetime