# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-08-19

### Added
#### Bulk Features
- **Modular Architecture**: Complete restructure of the project into `core/`, `gui/`, `strategies/`, `fem/`, `objects/`, `services/`, `resources/` and `predict/`.
- **Tree View Integration**: Implemented `MeshStudy` and `Results` as native FreeCAD FeaturePython objects for proper tree view nesting.
- **Strategy Pattern**: Extensible design for quantity of interest (QoI) extraction methods (Stress/Displacement) and refinement strategies (UniformH).

#### Internal Logic
- **Convergence**: Added `convergence.py` to calculate relative error and decide if convergence happened or not.
- **QoI Extraction**: Eliminated bulky `if/elif` chains by using a Registry-based Strategy.
- **Solver Safety**: Added pre-run validation in `analysis_reader.py` to ensure material, mesh, and solver availability.

#### Under Devolopment
- **Recover Data**: Added `recover_data.py`  to recover data from previous incomplete studies (due to unexpected crashes)
- **Safety Limits System**: Integrated `limits.py` to monitor node/element counts and prevent system instability before solver execution.