import random


class Tamagotchi:
    HEALTH_MAX = 100
    MIN = 0
    ACTIONS_MAX = 100
    # How much each stat rises per tick of time (US8). Subclasses change these.
    BOREDOM_GAIN = 4
    HUNGER_GAIN = 4
    EXHAUSTION_GAIN = 4
    # Health lost per stat at its max (US9)
    NEGLECT_DAMAGE = 10
    # Saved in the JSON file so loading knows which subclass to rebuild
    CATEGORY = "Base"

    def __init__(self, name, species, health=HEALTH_MAX, hunger=MIN, boredom=MIN, exhaustion=MIN):
        self.species = species
        self.name = name
        self.health = health
        self.hunger = hunger
        self.boredom = boredom
        self.exhaustion = exhaustion

    # US16: turn the pet into a dictionary that JSON can store (serialization)
    def to_dict(self):
        return {
            "category": self.CATEGORY,
            "name": self.name,
            "species": self.species,
            "health": self.health,
            "hunger": self.hunger,
            "boredom": self.boredom,
            "exhaustion": self.exhaustion,
            "alive": self.is_alive(),
        }

    def get_status(self):
        return f"{self.name} is a {self.species} that has {self.health} health, {self.hunger} hunger, {self.boredom} boredom, and {self.exhaustion} exhaustion."

    # US9: a pet is alive while it has health left
    def is_alive(self):
        return self.health > Tamagotchi.MIN

    def feed(self):
        if not self.is_alive():
            return f"{self.name} is dead."
        if self.hunger > Tamagotchi.MIN:
            self.hunger = max(Tamagotchi.MIN, self.hunger - 10)
            self.health = min(Tamagotchi.HEALTH_MAX, self.health + 5)
            return f"{self.name} has been fed."
        else:
            return f"{self.name} is not hungry."

    def play(self):
        if not self.is_alive():
            return f"{self.name} is dead."
        if self.boredom > Tamagotchi.MIN:
            self.boredom = max(Tamagotchi.MIN, self.boredom - 10)
            self.exhaustion = min(Tamagotchi.ACTIONS_MAX, self.exhaustion + 10)
            self.hunger = min(Tamagotchi.ACTIONS_MAX, self.hunger + 10)
            return f"{self.name} has played."
        else:
            return f"{self.name} is not bored."

    def sleep(self):
        if not self.is_alive():
            return f"{self.name} is dead."
        if self.exhaustion > Tamagotchi.MIN:
            self.exhaustion = max(Tamagotchi.MIN, self.exhaustion - 10)
            return f"{self.name} has slept."
        else:
            return f"{self.name} is not tired."

    def heal(self):
        if not self.is_alive():
            return f"{self.name} is dead."
        if self.health < Tamagotchi.HEALTH_MAX:
            self.health = min(Tamagotchi.HEALTH_MAX, self.health + 20)
            return f"{self.name} has been healed."
        else:
            return f"{self.name} is already at full health."

    # US8 + US9: one tick of time
    def pass_time(self):
        """One tick of time: needs rise, and maxed needs hurt health."""
        if not self.is_alive():
            return None

        self.boredom = min(Tamagotchi.ACTIONS_MAX, self.boredom + self.BOREDOM_GAIN)
        self.hunger = min(Tamagotchi.ACTIONS_MAX, self.hunger + self.HUNGER_GAIN)
        self.exhaustion = min(Tamagotchi.ACTIONS_MAX, self.exhaustion + self.EXHAUSTION_GAIN)

        for stat in [self.boredom, self.hunger, self.exhaustion]:
            if stat == Tamagotchi.ACTIONS_MAX:
                self.health = max(Tamagotchi.MIN, self.health - self.NEGLECT_DAMAGE)

        if not self.is_alive():
            return f"{self.name} has died..."
        return None

    # US10: random events
    def random_event(self):
        """Apply one random event to this pet and return what happened."""
        event = random.randint(1, 4)
        if event == 1:
            self.hunger = max(Tamagotchi.MIN, self.hunger - 10)
            message = f"{self.name} found a snack! (hunger -10)"
        elif event == 2:
            self.health = max(Tamagotchi.MIN, self.health - 15)
            message = f"{self.name} caught a cold! (health -15)"
        elif event == 3:
            self.boredom = max(Tamagotchi.MIN, self.boredom - 10)
            message = f"{self.name} found a new toy! (boredom -10)"
        else:
            self.exhaustion = min(Tamagotchi.ACTIONS_MAX, self.exhaustion + 10)
            message = f"{self.name} had a nightmare! (exhaustion +10)"

        if not self.is_alive():
            message += f" {self.name} has died..."
        return message


class LandTamagotchi(Tamagotchi):
    CATEGORY = "Land"
    BOREDOM_GAIN = 6

    def get_status(self):
        return super().get_status() + " (Land)"


class SeaTamagotchi(Tamagotchi):
    CATEGORY = "Sea"
    HUNGER_GAIN = 6

    def get_status(self):
        return super().get_status() + " (Sea)"


class SkyTamagotchi(Tamagotchi):
    CATEGORY = "Sky"
    EXHAUSTION_GAIN = 6

    def get_status(self):
        return super().get_status() + " (Sky)"