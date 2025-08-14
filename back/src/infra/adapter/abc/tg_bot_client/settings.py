from dataclasses import dataclass


@dataclass
class Settings:
    token: str
    username: str
    
    def __hash__(self):
        return hash((self.token, self.username))
    
    def __eq__(self, other):
        if not isinstance(other, Settings):
            return False
        return (self.token == other.token and
                self.username == other.username) 