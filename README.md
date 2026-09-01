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

*(pending)*
