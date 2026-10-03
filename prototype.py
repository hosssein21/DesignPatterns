"""
Prototype Pattern
-------------------
Creates new objects by COPYING an existing object (the "prototype")
instead of building one from scratch. Useful when object creation is
expensive, or when you want a fresh object with the same state as a
template.

Real-world use cases:
- Cloning a complex game character/level config
- Duplicating a pre-configured document/report template
- Copying a fully-built object graph without re-running setup logic
"""

import copy


class Prototype:
    def clone(self):
        """Deep copy by default — override per-class if shallow is fine."""
        return copy.deepcopy(self)


class Enemy(Prototype):
    def __init__(self, name, health, inventory=None):
        self.name = name
        self.health = health
        self.inventory = inventory or []

    def __repr__(self):
        return f"Enemy(name={self.name!r}, health={self.health}, inventory={self.inventory})"


if __name__ == "__main__":
    goblin_template = Enemy("Goblin", health=30, inventory=["dagger", "coin"])

    # Spawn many goblins from the same template instead of re-running
    # expensive setup logic (stat calculation, loot table rolls, etc.)
    goblin1 = goblin_template.clone()
    goblin2 = goblin_template.clone()

    goblin1.name = "Goblin #1"
    goblin1.inventory.append("shield")  # safe — deep copy, independent list

    print(goblin_template)  # inventory unaffected by goblin1's change
    print(goblin1)
    print(goblin2)
    print(goblin1 is goblin2)  # False — distinct objects
