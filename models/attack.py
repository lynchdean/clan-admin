from dataclasses import dataclass

@dataclass
class Attack:
    type: str
    attacker_tag: str
    attacker_name: str
    defender_tag: str
    defender_name: str
    stars: int
    destruction_percentage: int

    @classmethod
    def from_api(cls, data):
        attack = data.get("attacks")[0]
        member = data.get("member_data")
        return cls(
            type=data.get("war_data", {}).get("type"),
            attacker_tag=member.get("tag"),
            attacker_name=member.get("name"),
            defender_tag=attack.get("defenderTag"),
            defender_name=attack.get("defender", {}).get("name"),
            stars=attack.get("stars"),
            destruction_percentage=attack.get("destructionPercentage")
        )

    def __str__(self):
        return f"{self.attacker_name} ({self.attacker_tag}) attacked {self.defender_name} ({self.defender_tag}) with {self.stars} stars and {self.destruction_percentage}% destruction"


