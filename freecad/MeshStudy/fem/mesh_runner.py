import FreeCAD as App
from ..core.exceptions import MeshError

class MeshRunner:
    @staticmethod
    def generate(obj, size):
        import femmesh.gmshtools as gt
        try:
            import femmesh.netgentools as nt
        except ImportError:
            try:
                import ObjectsFem.makeMeshNetgen as nt
            except ImportError:
                pass

        mesh_obj = obj.MeshObject
        
        if mesh_obj.TypeId in ("Fem::FemMeshShapeBaseObjectPython", "Fem::FemMeshObjectPython"):
            mesh_obj.CharacteristicLengthMax = size[0]
            mesh_obj.CharacteristicLengthMin = size[1]
            mesh_obj.touch()
            gmsh = gt.GmshTools(mesh_obj)
            gmsh.create_mesh()
                    
        elif mesh_obj.TypeId == "Fem::FemMeshShapeNetgenObject":
            raise MeshError("Netgen Mesher is not supported yet! (Mesh Study Workbench)")

        obj.recompute()
        App.ActiveDocument.recompute()