#!/usr/bin/env python3
"""Replay a collision-check workload (pairwise boolean common on every
bbox-overlapping pair of a .brep directory) with the installed OCP wheel.

Usage: bench_pairs_ocp.py BREP_DIR [pairs_out.txt]
Prints: n_pairs total_seconds. Writes the pair list (for the DRAW replay).
"""
import sys, os, time

from OCP.BRep import BRep_Builder
from OCP.BRepTools import BRepTools
from OCP.TopoDS import TopoDS_Shape
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common


def load(path):
    s = TopoDS_Shape()
    assert BRepTools.Read_s(s, path, BRep_Builder()), path
    return s


def main():
    d = sys.argv[1]
    names = sorted(f[:-5] for f in os.listdir(d)
                   if f.endswith(".brep") and not f.startswith("_"))
    shapes, boxes = {}, {}
    for n in names:
        shapes[n] = load(os.path.join(d, n + ".brep"))
        b = Bnd_Box()
        BRepBndLib.Add_s(shapes[n], b)
        boxes[n] = b
    pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]
             if not boxes[a].IsOut(boxes[b])]
    t0 = time.perf_counter()
    for a, b in pairs:
        op = BRepAlgoAPI_Common(shapes[a], shapes[b])
        assert op.IsDone(), (a, b)
    dt = time.perf_counter() - t0
    print(f"{len(pairs)} pairs  {dt:.2f} s")
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w") as f:
            f.writelines(f"{a} {b}\n" for a, b in pairs)


if __name__ == "__main__":
    main()
