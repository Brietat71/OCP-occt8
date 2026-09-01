"""Injecte les alias 7.9 (ocp8_compat) juste apres le premier `import OCP`.

Paresseux et silencieux : un python qui n'importe jamais OCP ne paie rien
(ni les 0,6 s de chargement des 51 .so OCCT, ni un traceback si
LD_LIBRARY_PATH manque)."""
import sys


class _Ocp8Compat:
    def find_module(self, name, path=None):  # meta_path legacy API, suffit ici
        return None

    def find_spec(self, name, path=None, target=None):
        if name == "OCP" and not self._done:
            import importlib.util
            self._done = True          # avant l'import : pas de reentrance
            spec = importlib.util.find_spec("OCP")
            if spec is not None:
                orig = spec.loader.exec_module

                def exec_module(module, _orig=orig):
                    _orig(module)
                    try:
                        import ocp8_compat  # noqa: F401
                    except Exception:
                        pass
                spec.loader.exec_module = exec_module
                return spec
        return None

    _done = False


sys.meta_path.insert(0, _Ocp8Compat())
