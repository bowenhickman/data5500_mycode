class Pet:
    species = "unknown"

    species_avg_lifespan = {
        "dog": 12,
        "cat": 15,
        "parrot": 50,
        "rabbit": 9,
        "hamster": 3,
        "goldish": 4,
        "guniea pig": 4,
        "bird": 10,
        "lizard": 10
    }

    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species
    def human_age (self):
        return (self.age * 7)
    def lifespan(self):
        return self.species_avg_lifespan.get(self.species.lower(), "unknown")

Pet1 = Pet("Scout", 4, "dog")

print (Pet1.name, "is about ", Pet1.human_age(), "years old in human years. Their lifespan in animal years is about ", Pet1.lifespan())