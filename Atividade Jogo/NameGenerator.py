from random import randint

class NameGenerator():
    def __init__(self):
        with open("assets/names.txt", "r") as f:
            self.fruits = f.readline().split(',')
            self.adjectives = f.readline().split(',')

    def generate(self):
        random_fruit = randint(0, len(self.fruits) - 1)
        random_adjectives= randint(0, len(self.adjectives) - 1)

        chosen_fruit = self.fruits[random_fruit].capitalize()
        chosen_adjective = self.adjectives[random_adjectives].capitalize()

        return chosen_fruit + " " + chosen_adjective