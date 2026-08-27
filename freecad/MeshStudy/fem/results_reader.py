import FreeCAD as App

class ResultsReader:
    def __init__(self, obj):
        self.obj = obj
        self.result_object = None
        for m in obj.TheStudyTarget.Group:
            if m.isDerivedFrom('Fem::FemResultObject'):
                self.result_object = m
                break

    def extract(self, size, run_index):
        mesh_obj = self.obj.MeshObject
        nodes_count = len(mesh_obj.FemMesh.Nodes) if mesh_obj.FemMesh else 0
        elements_count = len(mesh_obj.FemMesh.Volumes) if mesh_obj.FemMesh else 0

        qoi_val = 0.0
        if self.result_object:
            if self.obj.QuantityOfInterest == "Stress":
                qoi_val = max(self.result_object.vonMises) * 1e+6  # Pa
            elif self.obj.QuantityOfInterest == "Displacement":
                qoi_val = max(self.result_object.DisplacementLengths) * 1000 # mm

        App.Console.PrintMessage(f"Nodes: {nodes_count}, Elements: {elements_count}, QoI: {qoi_val}\n")

        return {
            "Run": run_index,
            "Size": size,
            "Nodes": nodes_count,
            "Elements": elements_count,
            "QoI": round(qoi_val, 3)
        }