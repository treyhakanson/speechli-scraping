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
    json_array = []
    for fpath in iterate(BASE_DIR):
        if "".join(fpath.suffixes) != ".txt":
            continue

        data = {}
        preamble = ""
        f = fpath.open(mode="r")
        line = f.readline()
        while not (line.startswith('[') or line.startswith('(')):
            preamble += f"{line}\n"
            line = f.readline()
            print(line)
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
        data["type"] = "lyrics"
        data["content"] = f.read()
        f.close()
        artist = data["artist"]
        output_fpath = fpath.parent.parent.joinpath("lyrics.json")
        print(f"{fpath} -> {output_fpath}")
        if not output_fpath.parent.exists():
            output_fpath.parent.mkdir(parents=True)
        with output_fpath.open(mode="w+") as f:
            json_array.append(data)
            s = json.dumps(json_array)
            f.write(s)

        f.close()
    print("Done.")
