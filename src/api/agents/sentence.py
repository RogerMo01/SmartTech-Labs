class Sentence:
    def __init__(self, speaker: str, message: str):
        self.speaker = speaker
        self.message = message

    def __str__(self) -> str:
        return f"{self.speaker} dice: {self.message}"