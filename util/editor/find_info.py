import pathlib
import sys
import json5

class Info:
    def __init__(self, name: str, path: pathlib.Path, parent = None):
        self.name = name
        self.path = path
        self.children = dict()
        self.info = None
        self.parent = parent

    def walk(self) -> bool:
        has_info = False
        for entry in self.path.iterdir():
            if entry.is_file() and entry.name == "info.json":
                self.info = entry.read_text()
                has_info = True
            elif entry.is_dir():
                subdir = Info(entry.name, entry, self)
                if subdir.walk():
                    self.children[entry.name] = subdir
                    has_info = True
        return has_info

    def load(self):
        if self.info:
            if type(self.info) == str:
                self.info = json5.loads(self.info)

    def __str__(self):
        value = f'{{"name": "{self.name}", "path": "{self.path}", "children": {{'
        for child in self.children.values():
            value = value + str(child)
        value = value + "}}"
        return value

if __name__ == "__main__":
    root = Info("root", pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."))
    root.walk()
    print(root)
