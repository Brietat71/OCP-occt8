#!/bin/bash
# Build OCP (Python bindings) against OCCT 8.0.1, no VTK.
# Tested: Ubuntu 24.04, gcc 13, Python 3.13, EPYC (any x86_64 should do).
# Result: build/OCP.cpython-*.so — put its dir on PYTHONPATH (before any
# installed cadquery-ocp wheel) plus LD_LIBRARY_PATH=<occt8>/lib, and import
# compat/ocp8_compat.py before build123d (or drop a sitecustomize.py).
set -euo pipefail
ROOT=${1:-/opt/occt8}
PY=${PYTHON:-python3}

# 1. OCCT 8.0.1 (full modules, no VTK, no Tk)
sudo apt-get install -y ninja-build cmake g++ tcl-dev tk-dev libfreetype-dev \
     rapidjson-dev libglx-dev libgl-dev libegl-dev libx11-dev libfmt-dev unzip
git clone --depth 1 --branch V8_0_1 https://github.com/Open-Cascade-SAS/OCCT.git $ROOT/src
cmake -S $ROOT/src -B $ROOT/build -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=$ROOT/install \
  -DBUILD_MODULE_Draw=OFF -DUSE_FREETYPE=ON -DUSE_RAPIDJSON=ON \
  -DUSE_TK=OFF -DUSE_OPENGL=ON -DUSE_XLIB=ON
ninja -C $ROOT/build && ninja -C $ROOT/build install

# 2. OCP generated sources (upstream release, generated against OCCT 8.0.0)
gh release download 8.0.0.1 -R CadQuery/OCP -p "OCP_src_stubs_Linux.zip" -D $ROOT
unzip -q $ROOT/OCP_src_stubs_Linux.zip -d $ROOT/ocp_src

# 3. Patches: novtk + 8.0.0->8.0.1 API drift + Bnd_Box.Get() tuple
cd $ROOT/ocp_src
rm -f IVtk*.cpp IVtk*_tmpl.hxx IVtk*_pre.cpp
for p in $(dirname "$0")/patches/*.patch; do patch -p1 < "$p"; done

# 4. Compile the binding
$PY -m pip install pybind11 2>/dev/null || pip install pybind11
cmake -B build -S . -G Ninja -D CMAKE_BUILD_TYPE=Release \
  -D Python_EXECUTABLE=$(command -v $PY) \
  -D OpenCASCADE_DIR=$ROOT/install/lib/cmake/opencascade \
  -D pybind11_DIR=$($PY -c "import pybind11; print(pybind11.get_cmake_dir())") \
  -D CMAKE_CXX_STANDARD=17 \
  -D CMAKE_CXX_FLAGS="-DFMT_HEADER_ONLY -fvisibility=hidden -w"
ninja -C build
echo "OK: $ROOT/ocp_src/build/$(ls build | grep '\.so$')"
