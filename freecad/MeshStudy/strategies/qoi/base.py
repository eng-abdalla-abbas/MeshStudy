class QoIExtractor:
    """main class to Extracts a QoI from a result object"""
    def extract(self, result_object) -> float:
        raise NotImplementedError("Subclasses must implement this method")