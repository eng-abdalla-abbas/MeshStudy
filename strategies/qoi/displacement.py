from .base import QoIExtractor

class DisplacementExtractor(QoIExtractor):
    def extract(self, result_object) -> float:
        """get max displacement"""
        if not hasattr(result_object, 'DisplacementLengths'):
            return 0.0
        return max(result_object.DisplacementLengths)