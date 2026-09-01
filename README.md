# OCP-occt8

Goal: **Python bindings (OCP) built against OCCT 8.x**, plus the measurements
that justify (or kill) the effort.

Upstream [CadQuery/OCP](https://github.com/CadQuery/OCP) ships wheels up to
OCCT 7.9.3, and [build123d](https://github.com/gumyr/build123d) pins
`cadquery-ocp-novtk<8.0`. OCCT 8.0 (May 2026) advertises performance work in
boolean operations — unquantified. This repo measures first, builds second.

## Phase 1 — benchmark (this exists)

Replay *your own* heavy boolean operations (dumped as `.brep` pairs) against:

- the OCCT embedded in your installed OCP wheel (7.9.x), via `bench/bench_ocp.py`
- a locally compiled OCCT 8.0.1 `DRAWEXE`, via `bench/bench_draw.tcl`

Minimal OCCT 8 build for benchmarking (no visu, no Tk, ~15 min on 32 cores):

```bash
git clone --depth 1 --branch V8_0_1 https://github.com/Open-Cascade-SAS/OCCT.git src
cmake src -G Ninja -B build -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_MODULE_Draw=ON -DBUILD_MODULE_Visualization=OFF \
  -DBUILD_MODULE_ApplicationFramework=OFF -DBUILD_MODULE_DataExchange=OFF \
  -DUSE_FREETYPE=OFF -DUSE_TK=OFF -DUSE_OPENGL=OFF -DUSE_XLIB=OFF
ninja -C build
```

`.brep` inputs are not committed (project geometry); point the scripts at your
own dumps.

## Phase 2 — the binding (only if phase 1 shows a real win)

Regenerate OCP's pywrap bindings against OCCT 8 headers, patch build123d's
version pin, publish wheels. Not started; results of phase 1 will be recorded
here either way.

## Results

### Phase 1 (2026-09-01, EPYC 7543, 63-solid CAD model)

Workload: 199 bbox-overlapping pairwise `BRepAlgoAPI_Common` on real project
geometry (collision checking — the dominant boolean load of our build).

| | median of 3 |
|---|---|
| OCCT 7.9.3 (cadquery-ocp 7.9.3.1 wheel) | 15.6 s |
| OCCT 8.0.1 (local build, DRAWEXE) | **13.1 s (−16 %)** |

Capping the OCCT 7.9 `OSD_ThreadPool` to 8 threads changed nothing (15.57 s):
these small booleans are effectively single-threaded, so the delta is the
kernel itself, not thread-pool contention. Tcl-vs-Python per-call overhead is
negligible at 199 ops.

Verdict: real but modest. Phase 2 goes ahead.
