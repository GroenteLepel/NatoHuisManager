import json
import logging
import datetime


class Koelkast:
    def __init__(self, db):
        self.logger = logging.getLogger(__name__)
        self.inventory = []
        self.db = db
        self.load()

    def load(self):
        try:
            self.inventory = json.loads(self.db.load("koelkast.txt"))
        except:
            self.logger.info("Could not load Koelkast from db")

    def save(self):
        self.db.save("koelkast.txt", json.dumps(self.inventory))

    def add(self, restje):
        now = datetime.datetime.now()
        self.inventory.append({
            'name': restje,
            'date': f"{now.day}-{now.month}",
            'dibsed': "niemand"
        })
        self.save()

    def find(self, restje_to_find: str):
        for iloc, bakje in enumerate(self.inventory):
            if bakje['name'] == restje_to_find:
                return iloc, bakje

        return "Restje " + restje_to_find + " not found.", None

    def remove(self, restje: str):
        msg, bakje = self.find(restje)
        if bakje:
            self.inventory.remove(bakje)
            self.save()
            return f"Restje {restje} removed from the koelkast."
        else:
            return msg

    def dibs(self, restje: str, dibsed_by: str):
        msg, bakje = self.find(restje)
        if bakje:
            if bakje['dibsed'] != "niemand":
                return msg

            iloc = msg
            self.inventory[iloc]['dibsed'] = dibsed_by
            self.save()
            return None
        else:
            return msg

    def to_string(self):
        s = "NatoHuis koelkast:"
        for restje in self.inventory:
            s += f"\n - Restje {restje['name']} toegevoegd op {restje['date']}, " \
                 f"gedibst door {restje['dibsed']}."
        return s
