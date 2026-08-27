class MeshStudyError(Exception):

    pass

class LimitExceededError(MeshStudyError):
    
    pass

class SolverError(MeshStudyError):

    pass

class MeshError(MeshStudyError):

    pass