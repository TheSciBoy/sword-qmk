import pathlib
import sys
import re
import loosejson


class Info:
    def __init__(self, name: str, path: pathlib.Path, parent = None):
        self.name = name
        self.path = path
        self.children = dict()
        self.info = None
        self.parent = parent
        self.regex = r"""("(?:\\"|[^"])*?")|(\/\*(?:.|\s)*?\*\/|\/\/.*)"""

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

    def _remove_comments(self, s):
        s = re.sub(self.regex, r"\1", s)  # , flags = re.X | re.M)
        return s

    def get_layouts(self):
        if "layouts" in self.info:
            for name in self.info["layouts"]:
                if len(name) > 7 and name.startswith("LAYOUT_"):
                    yield name[7:]
        elif self.parent:
            self.parent.get_layouts()

    def load(self):
        if self.info:
            if type(self.info) == str:
                self.info = loosejson.parse_loosely_defined_json(self._remove_comments(self.info))

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

