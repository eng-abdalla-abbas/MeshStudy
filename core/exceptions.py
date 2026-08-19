class MeshStudyError(Exception):
    # The main class for Mesh Study errors
    pass

class LimitExceededError(MeshStudyError):
    
    # Geted when a limit is exceeded in the Mesh Study process
    pass

class SolverError(MeshStudyError):
    # Geted when a solver error is encountered in the Mesh Study process
    pass