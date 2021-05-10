"""The program is aimed to fabricate a Gaussian program
to test programs that integrate Gaussian, without really
installing it.
"""
import re
import numpy as np
import sys
from ase.data import atomic_numbers


def readinp(inplines):
    flag = 0
    coords = []
    elements = []
    for line in inplines:
        if not line.strip():
            # empty line
            flag += 1
        elif flag == 0:
            # keywords
            if line.startswith("#"):
                # setting
                keywords = line.split()
            elif line.startswith("%"):
                pass
        elif flag == 1:
            # title
            pass
        elif flag == 2:
            # multi and coords
            s = line.split()
            if len(s) == 2:
                pass
            elif len(s) == 4:
                # element
                elements.append(re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", s[0]))
                coords.append(list(map(float, s[1:4])))
        elif flag == 3:
            # end
            break
    return {
        "coords": np.array(coords),
        "elements": np.array(elements),
        "keywords": keywords,
    }


class FakeGaussian:
    """Fake Gaussian.

    Parameters
    ----------
    inp: str, optional
        Input filename. If None (default), input from stdin
    out: str, optional
        Output filename. If None (default), output to stdout.
    """

    def __init__(self, inp=None, out=None):
        if inp:
            with open(inp) as f:
                self.inplines = f.readlines()
        else:
            self.inplines = sys.stdin.readlines()
        if out:
            self.outf = open(out, 'w')
        else:
            self.outf = sys.stdout

    def run(self):
        inpdata = readinp(self.inplines)
        outdata = self.calcalate(inpdata)
        self.write(outdata)

    def calcalate(self, inpdata):
        # randomly generate results
        forces = np.random.rand(*inpdata['coords'].shape)
        energy = np.random.rand(1)
        return {**inpdata, "energy": energy, "forces": forces}

    def write(self, outdata):
        self.fakeline()
        # coords
        self.print(" "*24, "Input orientation:")
        self.print("-"*69)
        self.print(
            "Center     Atomic      Atomic             Coordinates (Angstroms)")
        self.print(
            "Number     Number       Type             X           Y           Z")
        self.print("-"*69)
        for ii, (element, coord) in enumerate(zip(outdata['elements'], outdata['coords']), 1):
            self.print("% 6d" % ii, "% 10d" %
                       atomic_numbers[element], "% 11d" % 0, " "*3, *("% 11.6f" % c for c in coord))
        self.print("-"*69)
        self.fakeline()
        # forces
        self.print("-"*67)
        self.print("Center     Atomic                   Forces (Hartrees/Bohr)")
        self.print(
            "Number     Number              X              Y              Z")
        self.print("-"*67)
        for ii, (element, force) in enumerate(zip(outdata['elements'], outdata['forces']), 1):
            self.print("% 6d" % ii, "% 8d" %
                       atomic_numbers[element], " "*6, *("% 14.9f" % f for f in force))
        self.fakeline()
        # energy
        self.print(
            "SCF Done:  E(XXXXX) =  % 14.10f     A.U. after    8 cycles" % outdata['energy'])
        self.fakeline()

    def print(self, *content):
        if content:
            print("", *content, file=self.outf)
        else:
            print(file=self.outf)

    def fakeline(self):
        fakeline = """This is the fake Gaussian"""
        nline = np.random.randint(100)
        for _ in range(nline):
            self.print(fakeline)
