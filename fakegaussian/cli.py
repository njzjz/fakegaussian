import argparse
import os
from .fake import FakeGaussian

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', type=str, default=None)
    args = parser.parse_args()

    if args.input:
        out = os.path.splitext(args.input)[0] + ".log"
    else:
        out = None
    FakeGaussian(inp = args.input, out = out).run()
