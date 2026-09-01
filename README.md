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

Verdict: real but modest. Phase 2 went ahead.

### Phase 2 (same day) — the binding works

Upstream [CadQuery/OCP releases](https://github.com/CadQuery/OCP/releases)
already ship **generated binding sources for OCCT 8.0.0** (tags `8.0.0.0` /
`8.0.0.1`) — no PyPI wheel, but the hard part (pywrap generation) is done.
What it took to compile them against OCCT **8.0.1** without VTK:

- the CI `novtk` transform (drop VTK from CMakeLists, remove `IVtk*` sources,
  drop `register_IVtk*` from `OCP.cpp`) — see `patches/`;
- two classes existed in 8.0.0 but were removed in 8.0.1
  (`Approx_BSplineApproxInterp`, `GeomFill_GordonBuilder`): bindings purged;
- one signature drift (`OpenGl_ShaderManager::BindFaceProgram`): binding purged;
- `Bnd_Box::Get()` returns a `Limits` struct in OCCT 8; patched the binding to
  return the 7.9-style 6-tuple `(xmin, ymin, zmin, xmax, ymax, zmax)`;
- OCCT 8 removed the legacy collection typedefs (`TopTools_*`, `TColStd_*`,
  `TColgp_*`, `TDF_LabelSequence`, `NCollection_Utf8String`). OCP 8 binds the
  raw template instantiations in `OCP.collections`; `compat/ocp8_compat.py`
  re-injects ~22 aliases so **build123d 0.11 imports and runs unchanged** —
  no fork, no pin change needed at runtime (bypass the pin by putting the
  built `.so` dir on `PYTHONPATH`).

Reproduce with `./build-ocp8.sh` (Ubuntu 24.04, ~40 min on 32 cores).

### End-to-end results on a real parametric CAD project

63-solid helicopter model, build123d, heavy boolean verification suite:

| | OCCT 7.9.3 | OCCT 8.0.1 |
|---|---|---|
| geometry + exports | 176 s | **135 s (−23 %)** |
| full build script | 370 s | **296 s (−20 %)** |
| CI gate (14 scripts) | 281 s | **248 s (−12 %)** |
| result manifest (masses, checks) | — | **identical to 1e-6 relative** |

Every downstream script (BEMT, MBDyn export, UQ, mass audits) passed green,
and the machine's published numbers did not move at all.
