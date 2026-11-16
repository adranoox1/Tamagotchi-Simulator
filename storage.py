import json
import tamagotchi

SAVE_FILE = "save.json"

# Which class to rebuild for each category saved in the file
CATEGORIES = {
    "Land": tamagotchi.LandTamagotchi,
    "Sea": tamagotchi.SeaTamagotchi,
    "Sky": tamagotchi.SkyTamagotchi,
}


def save_game(pets, filename=SAVE_FILE):
    #US16: save all the player's pets to a JSON file.
    data = [pet.to_dict() for pet in pets.values()]
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_game(filename=SAVE_FILE):
    #US17: read the JSON file and rebuild the pets (deserialization).
    # Raises FileNotFoundError if the file is missing,
    # json.JSONDecodeError if it is not valid JSON,
    # and ValueError if its content is not a valid save.
    with open(filename, "r") as file:
        data = json.load(file)

    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("the save file contains no pets")

    pets = {}
    for pet_data in data:
        try:
            pet_class = CATEGORIES[pet_data["category"]]
            pet = pet_class(
                pet_data["name"],
                pet_data["species"],
                health=int(pet_data["health"]),
                hunger=int(pet_data["hunger"]),
                boredom=int(pet_data["boredom"]),
                exhaustion=int(pet_data["exhaustion"]),
            )
        except (KeyError, TypeError, ValueError):
            raise ValueError("a pet in the save file is incomplete or invalid")

        # The file says the pet is dead: make sure its health agrees
        if pet_data.get("alive") is False:
            pet.health = tamagotchi.Tamagotchi.MIN

        pets[pet.name] = pet
    return pets