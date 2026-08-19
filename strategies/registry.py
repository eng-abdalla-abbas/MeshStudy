from .qoi.stress import StressExtractor
from .qoi.displacement import DisplacementExtractor
from .refinement.uniform_h import UniformHRefinement

def get_qoi_extractor(qoi_name: str):
    """Get the right Quantity"""
    registry = {
        "Stress": StressExtractor(),
        "Displacement": DisplacementExtractor(),
        # "Strain": StrainExtractor(), # For future (v0.2)
    }
    return registry.get(qoi_name, DisplacementExtractor()) # Default to Displacement

def get_refinement_strategy():
    """Get the desired Refinement method"""
    return UniformHRefinement()