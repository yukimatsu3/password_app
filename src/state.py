from dataclasses import dataclass, field
from typing import List, Dict
from services.database import load_passwords

@dataclass
class AppState:
    # JSONから読み込んだパスワード一覧をそのまま保持する
    passwords: List[Dict] = field(default_factory=list)

    @classmethod
    def load_initial(cls) -> "AppState":
        return cls(passwords=load_passwords())
    
    def reload_from_json(self):
        """JSONから再読み込みしたい場合に使用"""
        self.passwords = load_passwords()