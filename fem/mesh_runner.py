import FreeCAD as App

class MeshRunner:
    @staticmethod
    def generate(obj, size):
        import femmesh.gmshtools as gt
        import femmesh.netgentools as nt

        mesh_obj = obj.MeshObject
        
        if mesh_obj.TypeId == "Fem::FemMeshShapeBaseObjectPython":
            mesh_obj.CharacteristicLengthMax = size[0]
            mesh_obj.CharacteristicLengthMin = size[1]
            gmsh = gt.GmshTools(mesh_obj)
            gmsh.create_mesh()
                    
        elif mesh_obj.TypeId == "Fem::FemMeshShapeNetgenObject":
            mesh_obj.MaxSize = size[0]
            mesh_obj.MinSize = size[1]
            netgen = nt.NetgenTools(mesh_obj)
            netgen.prepare()
            netgen.compute()

        obj.recompute()