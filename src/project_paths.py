from pathlib import Path


def get_root_path():
    return Path(__file__).resolve().parent.parent

def get_in_project(*args):
    root = Path(__file__).resolve().parent.parent
    for path in args:
        root = root.joinpath(path)
    return root

if __name__ == "__main__":
    print(get_in_project("data", "raw", "data.csv"))