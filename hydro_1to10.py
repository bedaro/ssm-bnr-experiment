#!/usr/bin/env python3

from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path
import math
import os
import unittest

class DirType():
    def __init__(self, mode: str='r'):
        self._mode = mode

    def __call__(self, string: str):
        p = Path(string)
        if 'r' in self._mode and not p.is_dir():
            raise ArgumentTypeError(f"no directory named {string}")
        elif 'w' in self._mode:
            p.mkdir(parents=True, exist_ok='+' in self._mode)
        return p

def num_left_pad(i: int, n: int):
    s = ''
    if i == 0:
        return '0' * n
    elif i < 0:
        s = '-'
        n -= 1
        i *= -1
    return s + '0' * (n - int(math.ceil(math.log10(i + 0.1)))) + str(i)

class TestHydro1to10(unittest.TestCase):
    def test_left_pad(self):
        self.assertEqual('000000', num_left_pad(0, 6))
        self.assertEqual('0001', num_left_pad(1, 4))
        self.assertEqual('0004', num_left_pad(4, 4))
        self.assertEqual('0009', num_left_pad(9, 4))
        self.assertEqual('0010', num_left_pad(10, 4))
        self.assertEqual('00123', num_left_pad(123, 5))
        self.assertEqual('-0123', num_left_pad(-123, 5))

    def test_dirtype_r(self):
        dt = DirType('r')
        self.assertTrue(Path, type(dt('/tmp')))
        self.assertTrue(isinstance(dt('/tmp'), Path))

def main():
    parser = ArgumentParser()

    parser.add_argument("indir", type=DirType())
    parser.add_argument("outdir", type=DirType('w'))
    args = parser.parse_args()

    for i in range(1, 366):
        filename = f'ssm_{num_left_pad(i, 5)}.nc'
        os.link(args.indir / filename, args.outdir / filename)

    for i in range(366, 3651):
        filename_src = f'ssm_{num_left_pad((i - 1) % 365 + 1, 5)}.nc'
        filename_dest = f'ssm_{num_left_pad(i, 5)}.nc'
        os.symlink(filename_src, args.outdir / filename_dest)

    os.link(args.indir / 'ssm_00366.nc', args.outdir / 'ssm_03651.nc')

if __name__ == '__main__':
    main()
