import tamagotchi
import storage
import random
import json

EVENT_CHANCE = 0.2   # 20% chance of a random event after each action


class Game:
    def __init__(self):
        pets_list = [
            # Land
            tamagotchi.LandTamagotchi("Rima", "Bunny"),
            tamagotchi.LandTamagotchi("Pistashe", "Froggie"),
            tamagotchi.LandTamagotchi("Noisette", "Hedgehog"),
            tamagotchi.LandTamagotchi("Biscuit", "Puppy"),
            tamagotchi.LandTamagotchi("Mochi", "Hamster"),
            # Sea
            tamagotchi.SeaTamagotchi("Bubbles", "Sealion"),
            tamagotchi.SeaTamagotchi("Coral", "Turtle"),
            tamagotchi.SeaTamagotchi("Splash", "Dolphin"),
            tamagotchi.SeaTamagotchi("Inky", "Octopus"),
            tamagotchi.SeaTamagotchi("Nemo", "Clownfish"),
            # Sky
            tamagotchi.SkyTamagotchi("Plume", "Owl"),
            tamagotchi.SkyTamagotchi("Kiwi", "Parrot"),
            tamagotchi.SkyTamagotchi("Nuage", "Bat"),
            tamagotchi.SkyTamagotchi("Pepper", "Sparrow"),
            tamagotchi.SkyTamagotchi("Flamme", "Phoenix"),
        ]
        self.catalogue = {pet.name: pet for pet in pets_list}
        self.pets = {}

    def show_catalogue(self):
        """Show all the pets the player can choose from."""
        print("Available pets:")
        for pet in self.catalogue.values():
            print(f"- {pet.name} the {pet.species}")

    def choose_pets(self):
        # US1: the player chooses three pets
        self.show_catalogue()
        while True:
            print("Please choose three pets.")
            chosen_pets = input("choose your three pets : ").split()
            if len(set(chosen_pets)) == 3 and all(pet in self.catalogue for pet in chosen_pets):
                print(f"You have chosen the following pets: {chosen_pets}")
                self.pets = {name: self.catalogue[name] for name in chosen_pets}
                break
            print("Invalid choice: type 3 different names from the list, separated by spaces.")

    # US16: save the game
    def save(self):
        try:
            storage.save_game(self.pets)
            print(f"Game saved to {storage.SAVE_FILE}.")
        except OSError as err:
            print(f"Could not save the game: {err}")

    # US17 + US21: load the game, without crashing if the file is missing or broken
    def load(self):
        try:
            self.pets = storage.load_game()
            print("Game loaded!")
            return True
        except FileNotFoundError:
            print("No saved game found.")
        except json.JSONDecodeError:
            print("The save file is broken (not valid JSON).")
        except ValueError as err:
            print(f"The save file is invalid: {err}")
        return False

    def start_game(self):
        # US17: offer to load a saved game, otherwise choose new pets
        answer = input("Do you want to load a saved game? (yes/no): ").strip().lower()
        if answer != "yes" or not self.load():
            self.choose_pets()

        # US11: the game loop, repeats until the player quits
        actions_menu = ["feed", "play", "sleep", "heal", "status"]
        while True:
            print()
            self.describe_pets()

            # Game over when every pet is dead
            if not any(pet.is_alive() for pet in self.pets.values()):
                print("All your pets are dead. Game over.")
                break

            # US12 + US13: choose a pet, or quit
            chosen_pet = input("Choose a pet to take care of (or 'stats' / 'save' / 'load' / 'quit'): ").strip()
            if chosen_pet.lower() == "quit":
                print("Goodbye!")
                break
            # US16 + US17: save or load from the menu (does not count as a turn)
            if chosen_pet.lower() == "save":
                self.save()
                continue
            if chosen_pet.lower() == "load":
                self.load()
                continue
            # US14: show how many pets are alive and dead (does not count as a turn)
            if chosen_pet.lower() == "stats":
                alive, dead, averages = self.stats()
                print(f"Alive: {alive}, Dead: {dead}")
                # US15: averages of the living pets
                if averages:
                    print(f"Average health: {averages['health']}")
                    print(f"Average hunger: {averages['hunger']}")
                    print(f"Average boredom: {averages['boredom']}")
                    print(f"Average exhaustion: {averages['exhaustion']}")
                else:
                    print("No living pets, so no averages.")
                continue
            if chosen_pet not in self.pets:
                print(f"{chosen_pet} is not one of your pets.")   # US19
                continue
            pet = self.pets[chosen_pet]

            # Choose an action
            action = input("What do you want to do? (feed/play/sleep/heal/status): ").strip().lower()
            if action not in actions_menu:
                print("Invalid action. Please choose from feed, play, sleep, heal, or status.")   # US18
                continue

            # Display only the selected pet's status (does not count as a turn)
            if action == "status":
                print(pet.get_status())
                continue

            # Apply the action to the pet
            if action == "feed":
                print(pet.feed())
            elif action == "play":
                print(pet.play())
            elif action == "sleep":
                print(pet.sleep())
            elif action == "heal":
                print(pet.heal())

            # US8 + US9 + US10: time passes after the action
            for message in self.end_turn():
                print(message)

    # US8 + US9 + US10: what happens after each action
    def end_turn(self):
        """Time passes for every chosen pet, then maybe a random event."""
        messages = []

        # Time passes for ALL chosen pets
        for pet in self.pets.values():
            message = pet.pass_time()
            if message:
                messages.append(message)

        # Sometimes, a random event hits one living pet
        living_pets = [pet for pet in self.pets.values() if pet.is_alive()]
        if living_pets and random.random() < EVENT_CHANCE:
            pet = random.choice(living_pets)
            messages.append(pet.random_event())

        return messages

    # US14 + US15: count living and dead pets, and average the stats of living pets
    def stats(self):
        living_pets = [pet for pet in self.pets.values() if pet.is_alive()]
        dead_pets = [pet for pet in self.pets.values() if not pet.is_alive()]

        # No living pets: no averages (avoids dividing by zero)
        if len(living_pets) == 0:
            return len(living_pets), len(dead_pets), None

        count = len(living_pets)
        averages = {
            "health": round(sum(pet.health for pet in living_pets) / count, 1),
            "hunger": round(sum(pet.hunger for pet in living_pets) / count, 1),
            "boredom": round(sum(pet.boredom for pet in living_pets) / count, 1),
            "exhaustion": round(sum(pet.exhaustion for pet in living_pets) / count, 1),
        }
        return len(living_pets), len(dead_pets), averages

    def describe_pets(self):
        for pet in self.pets.values():
            print(pet.get_status())

    def count_pets(self):
        return f"You have {len(self.pets)} pets."