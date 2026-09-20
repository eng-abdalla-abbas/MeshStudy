# Changelog

All notable changes to this project will be documented in this file.

## [0.1.3] - 2026-09-20

### Added

- **Preferences Page**: Added a MeshStudy preferences page to FreeCAD settings, with configurable maximum node and element counts.
- **Limits Toggle**: Added an option to enable or disable mesh limits while preserving the configured values.
- **Parameter Validation**: Added pre-run validation to reject invalid study parameters with clear error messages.

### Changed

- **Mesh Limits**: Replaced fixed node and element limits with values stored in FreeCAD user preferences.
- **Execution Safety**: Applied mesh-limit checks after meshing and before solver execution, stopping the study when an enabled limit is exceeded.

---


## [0.1.2] - 2026-09-10

### Changed
- **Backup System**: Moved the backup file `backup_resultes.json` from the install directory `./Resources/data/`, to the freecad user data directory `FreeCAD.getUserAppDataDir()/MeshStudyWorkbench/`.
- **Signal System**: Removed all the singnals files, replaced the "stop" signal for a check function "is_stoped" that checks the dialog object attribute "stoped".
- **Package Metadata**: Restored the required `xmlns` on `package.xml` and bumped the version to `0.1.2`.

### Fixed
- **Fixed Icon Path Mismatch**: Changed the icons folder first case (from `./icons/` to `./Icons/`).
- **Fixed Backup Folder Creation**: `os.makedirs` now creates the user-data directory, not the backup JSON file path.
- **Fixed Dirty Addon Directory**: Runtime backup (and the old stop signal) no longer write into the git-tracked install folder.
- **Fixed Stop Button**: The wait interval pumps Qt events, so Stop can be clicked instead of freezing during `sleep`.
- **Fixed Stop Without Results**: Stopping before any completed solve no longer creates an empty result object or clears backup incorrectly.
- **Fixed Run Object Mix-up**: The run service uses the MeshStudy object it was given, instead of re-reading the current selection mid-run.
- **Fixed Recovery Flow**: Choosing Forfeit no longer aborts Run / Show Results; only Recover returns early.
- **Fixed Missing Backup Directory on Save**: `save_results` creates `DATA_DIR` before writing `backup_results.json`.

---


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