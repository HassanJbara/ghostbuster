import argparse
import json

from ghostbuster import Ghostbuster


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="input.txt")

    args = parser.parse_args()
    print("input args:\n", json.dumps(vars(args), indent=4, separators=(",", ":")))
    return args


def main(args):
    ghoostbuster = Ghostbuster()
    with open(args.file, "r") as f:
        text = f.read().strip()
        print(ghoostbuster.predict(text))


if __name__ == "__main__":
    args = parse_args()
    main(args)