from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging
import argparse

parser = argparse.ArgumentParser(description = "sorting folder")
parser.add_argument("--sourse", "-s", help = "sourse folder", required = True)
parser.add_argument("--output", "-o", help = "output folder", default = "dist")

args = vars(parser.parse_args())

sourse = args.get("sourse")
output = args.get("output")


folders = []
def grab_folders(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grab_folders(el)

def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            new_path = output_folder / ext
        try:
            new_path.mkdir(exist_ok = True, parents = True)
            copyfile(el, new_path / el.name)
        except OSError as err:
            logging.error(err)


if __name__ == "__main__":
    logging.basicConfig(level = logging.ERROR, format = "%(threadName)s %(message)s")
    base_folder = Path(sourse)
    output_folder = Path(output)
    folders.append(base_folder)
    grab_folders(base_folder)

threads = []

for folder in folders:
    th = Thread(target = copy_file, args = (folder, ))
    th.start()

[th.join() for th in threads]

