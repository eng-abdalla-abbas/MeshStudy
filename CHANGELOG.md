# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-08-19

### Added
- **Modular Architecture**: Complete restructure of the project into `core/`, `gui/`, `strategies/`, `fem/`, `objects/`, `services/`, `resources/` and `predict/`.
- **Tree View Integration**: Implemented `MeshStudy` and `Results` as native FreeCAD FeaturePython objects for proper tree view nesting.
- **Strategy Pattern**: Extensible design for QoI extraction (Stress/Displacement) and refinement strategies (UniformH).

### Refactored (Internal Logic)
- **Mesh Sizing Strategy**: Replaced manual sizing with ordered `Tuples` `[(max, min), ...]` and `enumerate` for predictable iteration loops.
- **Dynamic Path Handling**: Replaced all hardcoded system paths (e.g., `C:\Users\...`) with `App.getUserAppDataDir()` for cross-platform compatibility.
- **Math Robustness**: Added protection against "Division by zero" in convergence math and automatic conversion to percentage format.

### Fixed
- **QoI Extraction**: Eliminated bulky `if/elif` chains by implementing a Registry-based Strategy Pattern.
- **Solver Safety**: Added pre-run validation in `analysis_reader.py` to ensure material, mesh, and solver availability.

### Under Devolopment
- **Safety Limits System**: Integrated `limits.py` to monitor node/element counts and prevent system instability before solver execution.
- **Automated Convergence**: Added `convergence.py` to calculate relative error and deside if convegence happened or not.