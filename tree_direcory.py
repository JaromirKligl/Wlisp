import pathlib

class HTMList(list):
    def __repr__(self):
        return f"<ul>{' '.join(map(lambda x: f'<li>{x}</li>', self))}</ul>"

class FileHTMList(list):
    def __repr__(self):
        return f"<a href=\"{' '.join(map(str, self))}\"><li>{' '.join(map(str, self))} </li></a>"

class TreeDirectory:
    def __init__(self,name, folders, files):
        self.name = name
        self.folders = folders
        self.files = files

    def __repr__(self):
        if self.files:
            return f"{self.name}<ul>{self.files}</ul>{self.folders}"

        return f"{self.name}{self.folders}"
def get_tree_from_path(path):
    folders = HTMList([get_tree_from_path(pat) for pat in path.glob("*") if pat.is_dir()])
    files = FileHTMList([pat.relative_to(pathlib.Path.cwd()) for pat in path.glob("*") if pat.is_file()])
    return TreeDirectory(path, folders, files)




if __name__ == "__main__":
    print(get_tree_from_path(pathlib.Path.cwd()))