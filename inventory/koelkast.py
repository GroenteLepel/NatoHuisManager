import database as db

import datetime


class Restje:
    def __init__(self, restje: str,
                 date: datetime.datetime = datetime.datetime.now(),
                 dibsed_by: str = "niemand"
                 ):
        self.restje = restje
        self.date = date
        self.dibsed_by = dibsed_by
        if self.dibsed_by != "niemand":
            self.dibsed = True
        else:
            self.dibsed = False

    def dibs(self, dibsed_by: str):
        self.dibsed = True,
        self.dibsed_by = dibsed_by

    def antidibs(self):
        self.dibsed = False,
        self.dibsed_by = "niemand"

    def is_dibsed(self):
        return self.dibsed

    @staticmethod
    def from_string(s: str):
        s_split = s.split()
        restje = s_split[1]
        date = datetime.datetime.strptime(s_split[4], '%d-%m,')
        dibsed_by = s_split[-1][:-1]  # [:-1] removes the period

        new_restje = Restje(
            restje=restje,
            date=date,
            dibsed_by=dibsed_by
        )
        return new_restje

    def __str__(self):
        evaluation = \
            "Restje {0:s} toegevoegd op {1:d}-{2:d}, " \
            "gedibst door {3:s}.".format(
                self.restje,
                self.date.day,
                self.date.month,
                self.dibsed_by
            )
        return evaluation

    # __repr__ = __str__


class Koelkast:
    def __init__(self, inventory: list = []):
        self.inventory = inventory

    @staticmethod
    def from_file(file: str):
        inventory_string = db.load(file).split('\n')[1:]
        inventory = [Restje] * len(inventory_string)
        for i, restje in enumerate(inventory_string):
            # remove the ' - ' with [3:]
            inventory[i] = Restje.from_string(restje[3:])

        new_koelkast = Koelkast(inventory)
        return new_koelkast

    def add(self, restje: Restje):
        self.inventory.append(restje)

    def find(self, restje_to_find: str):
        for iloc, bakje in enumerate(self.inventory):
            if bakje.restje == restje_to_find:
                if bakje.is_dibsed():
                    return "This restje has already been dibsed!", None

                return iloc, bakje

        return "Restje " + restje_to_find + " not found.", None

    def dibs(self, restje: str, dibsed_by: str):
        iloc, bakje = self.find(restje)
        if bakje:
            self.inventory[iloc].dibs(dibsed_by)
            return None
        else:
            return iloc

    def save(self, file):
        db.save(file, str(self))

    def __str__(self):
        s = "NatoHuis koelkast:"
        for restje in self.inventory:
            s += "\n - " + str(restje)
        return s
