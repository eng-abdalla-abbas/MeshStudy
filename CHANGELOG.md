# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2026-08-27

### Changed
- **Addon Architecture**: Migrated the addon to FreeCAD's namespaced directory layout to prevent import conflicts with FreeCAD or other addons.
- **Path Resolution**: Replaced hardcoded addon directory paths with dynamic `os.path.dirname(__file__)` calls to ensure compatibility regardless of the installation folder name.
- **GUI Imports**: Updated all UI modules to use version-agnostic `PySide` imports, allowing FreeCAD to handle Qt version fallbacks automatically.
- **Recover Data**: Added `recover_data.py`  to recover data from previous incomplete studies (due to unexpected crashes), saved into `backup_data.json`.

### Fixed
- **First run error**: fixed it by initiating a backup file (`backup_data.json`) if not exsisted.
- **Other bugs**: Fixed many other bugs, enhancing user experiance.

---


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
- **Recover Data**: Adding `recover_data.py`  to recover data from previous incomplete studies (due to unexpected crashes)
- **Safety Limits System**: Integrating `limits.py` to monitor node/element counts and prevent system instability before solver execution.