"""OCCT 8 compatibility aliases for code written against OCP 7.9.

OCCT 8 removed the legacy collection typedefs (TopTools_*, TColStd_*,
TColgp_*...). OCP 8 binds the raw template instantiations in OCP.collections
instead. This module re-injects the old names so build123d & friends import
unchanged. Import it once, before (or after) anything imports OCP submodules.
"""
from OCP import collections as _C
from OCP import NCollection as _NC, TopTools as _TT, TColStd as _TS, \
    TColgp as _TG, TDF as _TDF

_ALIAS = {
    _TT: {
        "TopTools_ListOfShape": _C.List_TopoDS_Shape,
        "TopTools_IndexedMapOfShape": _C.IndexedMap_TopoDS_Shape_TopTools_ShapeMapHasher,
        "TopTools_IndexedDataMapOfShapeListOfShape": _C.IndexedDataMap_TopoDS_Shape_List_TopoDS_Shape_TopTools_ShapeMapHasher,
        "TopTools_HSequenceOfShape": _C.HSequence_TopoDS_Shape,
        "TopTools_SequenceOfShape": _C.Sequence_TopoDS_Shape,
        "TopTools_MapOfShape": _C.Map_TopoDS_Shape_TopTools_ShapeMapHasher,
        "TopTools_DataMapOfShapeListOfShape": _C.DataMap_TopoDS_Shape_List_TopoDS_Shape_TopTools_ShapeMapHasher,
    },
    _TS: {
        "TColStd_Array1OfReal": _C.Array1_double,
        "TColStd_Array1OfInteger": _C.Array1_int,
        "TColStd_Array2OfReal": _C.Array2_double,
        "TColStd_HArray1OfBoolean": _C.HArray1_bool,
        "TColStd_HArray1OfInteger": _C.HArray1_int,
        "TColStd_HArray1OfReal": _C.HArray1_double,
        "TColStd_HArray2OfReal": _C.HArray2_double,
        "TColStd_IndexedDataMapOfStringString": _C.IndexedDataMap_TCollection_AsciiString_TCollection_AsciiString,
        "TColStd_SequenceOfHAsciiString": _C.Sequence_TCollection_HAsciiString,
    },
    _TG: {
        "TColgp_Array1OfPnt": _C.Array1_gp_Pnt,
        "TColgp_Array1OfVec": _C.Array1_gp_Vec,
        "TColgp_Array2OfPnt": _C.Array2_gp_Pnt,
        "TColgp_HArray1OfPnt": _C.HArray1_gp_Pnt,
        "TColgp_HArray1OfPnt2d": _C.HArray1_gp_Pnt2d,
        "TColgp_HArray2OfPnt": _C.HArray2_gp_Pnt,
    },
    _TDF: {"TDF_LabelSequence": _C.Sequence_TDF_Label},
    _NC: {"NCollection_Utf8String": _NC.NCollection_String},
}
for _mod, _names in _ALIAS.items():
    for _n, _obj in _names.items():
        if not hasattr(_mod, _n):
            setattr(_mod, _n, _obj)
