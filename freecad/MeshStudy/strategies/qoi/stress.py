from .base import QoIExtractor

class StressExtractor(QoIExtractor):
    def extract(self, result_object) -> float:
        """extract max von mise stress from result object"""
        if not hasattr(result_object, 'vonMises'):
            return 0.0
        return max(result_object.vonMises) * 1e+6  # Convert MPa to Pa