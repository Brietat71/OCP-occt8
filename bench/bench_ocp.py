#!/usr/bin/env python3
"""Time boolean ops on .brep pairs with the *installed* OCP (OCCT 7.9.x).

Usage:  python bench_ocp.py A.brep B.brep [cut|fuse|common] [repeats]
Prints one line: median wall seconds over `repeats` (default 3).
Each repeat re-reads the shapes so OCCT caches don't flatter later runs.
"""
import sys, time, statistics

from OCP.BRep import BRep_Builder
from OCP.BRepTools import BRepTools
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepAlgoAPI import (BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse,
                             BRepAlgoAPI_Common)

OPS = {"cut": BRepAlgoAPI_Cut, "fuse": BRepAlgoAPI_Fuse,
       "common": BRepAlgoAPI_Common}


def load(path):
    s = TopoDS_Shape()
    if not BRepTools.Read_s(s, path, BRep_Builder()):
        sys.exit(f"cannot read {path}")
    return s


def main():
    a_p, b_p = sys.argv[1], sys.argv[2]
    op = OPS[sys.argv[3] if len(sys.argv) > 3 else "cut"]
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    times = []
    for _ in range(n):
        a, b = load(a_p), load(b_p)
        t0 = time.perf_counter()
        r = op(a, b)
        assert r.IsDone()
        times.append(time.perf_counter() - t0)
    print(f"{statistics.median(times):.3f}")


if __name__ == "__main__":
    main()
