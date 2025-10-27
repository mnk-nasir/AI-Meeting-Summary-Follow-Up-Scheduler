import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    OPENAI_API_KEY: str
    GOOGLE_API_TOKEN: str
    GOOGLE_CALENDAR_ID: str
    mock: bool

    @staticmethod
    def load_from_env() -> "Config":
        o = os.getenv("OPENAI_API_KEY", "")
        gtoken = os.getenv("GOOGLE_API_TOKEN", "")
        gcal = os.getenv("GOOGLE_CALENDAR_ID", "")
        mock = not (o and gtoken and gcal)
        return Config(o, gtoken, gcal, mock)
