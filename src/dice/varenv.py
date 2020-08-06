import json
import logging
import traceback

from .roller import as_ast


class NoEnv:
    def __init__(self):
        self.items = {}

    def set(self, key, value):
        self.items[key] = value

    def get(self, key):
        return self.items[key]


class VarEnv:
    def __init__(self, name, provider):
        self.name = name
        self.items = {}
        self.provider = provider

    def set(self, key, value):
        self.items[key] = value
        self.provider.save()

    def get(self, key):
        return self.items[key]


class VarEnvProvider:
    def __init__(self, db):
        self.db = db
        self.envs = {}
        self.load()

    def load(self):
        try:
            data = json.loads(self.db.load("roller.txt"))
            for person, vars in data.items():
                env = VarEnv(person, self)
                for v in vars:
                    try:
                        env.set(v['name'], as_ast(v['value'], env))
                    except:
                        # this error can occurr due to circular variable dependencies which cannot be resolved
                        pass
                self.envs[person] = env
        except json.JSONDecodeError:
            logging.warning("No rolling envs found.")

    def save(self):
        data = {}
        for person, env in self.envs.items():
            vars = [{'name': k, 'value': v.calc()} for k,v in env.items.items()]
            data[person] = vars
        self.db.save("roller.txt", json.dumps(data))

    def get(self, name):
        if name not in self.envs:
            self.envs[name] = VarEnv(name, self)
            self.save()
        return self.envs[name]
        

    