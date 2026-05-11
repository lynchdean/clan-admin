from dataclasses import dataclass, field

from models import Attack


@dataclass
class Season:
    year: int
    month: int
    attacks: list[Attack] = field(default_factory=list)

    @classmethod
    def from_data(cls, year: int, month: int, attacks: list[Attack]):
        return cls(year, month, attacks)

    def __str__(self):
        return f"Season: {self.year}-{self.month}"

    def total_attacks(self):
        return len(self.attacks)

    def avg_stars(self):
        return sum(attack.stars or 0 for attack in self.attacks) / len(self.attacks) if self.attacks else 0

    def avg_destruction(self):
        return sum(attack.destruction_percentage or 0 for attack in self.attacks) / len(self.attacks) if self.attacks else 0
