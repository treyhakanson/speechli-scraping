"""Parser for content from Genius."""
import re
import json
from .constants import DATA_DIR

BASE_DIR = DATA_DIR.joinpath("genius")


def iterate(fpath):
    """Iterate over arbitrarily nested directories."""
    if not fpath.is_dir():
        yield fpath
    else:
        for subpath in fpath.iterdir():
            yield from iterate(subpath)


def parse(no_cache=False, **kwargs):
    """Parse all content from Genius."""
    content_start_re = re.compile(r"^(?:\*{3}[^*]*\*{3})$", re.M)
    regexes = [
        ("title", re.compile(r"Title:\s+(.*)")),
        ("artist", re.compile(r"Artist:\s+(.*)"))
    ]
    for fpath in iterate(BASE_DIR):
        if "".join(fpath.suffixes) != ".txt":
            continue
        output_fpath = fpath.parent.joinpath(f"parsed/{fpath.name[:-4]}.json")
        print(f"{fpath} -> {output_fpath}")
        if not no_cache and output_fpath.exists():
            print("Using cache.")
            continue
        data = {}
        preamble = ""
        f = fpath.open(mode="r")
        line = f.readline()
        while not content_start_re.match(line):
            preamble += f"{line}\n"
            line = f.readline()
            #Throwing error, removing the following 2 lines causes infinite loop
            if line == "":
                raise Exception("Malformed file")
        for key, regex in regexes:
            try:
                data[key] = regex.search(preamble).group(1)
            except AttributeError as e:
                raise Exception(
                    f"Failed to match \"{key}\" regex in:\n",
                    preamble
                )
        data["content"] = f.read()
        f.close()
        if not output_fpath.parent.exists():
            output_fpath.parent.mkdir(parents=True)
        with output_fpath.open(mode="w") as f:
            json.dump(data, f)
        print("Done.")
