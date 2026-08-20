import FreeCAD as App

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
                nt = None

        mesh_obj = obj.MeshObject
        
        if mesh_obj.TypeId in ("Fem::FemMeshShapeBaseObjectPython", "Fem::FemMeshObjectPython"):
            mesh_obj.CharacteristicLengthMax = size[0]
            mesh_obj.CharacteristicLengthMin = size[1]
            mesh_obj.touch()
            gmsh = gt.GmshTools(mesh_obj)
            gmsh.create_mesh()
                    
        elif mesh_obj.TypeId == "Fem::FemMeshShapeNetgenObject":
            mesh_obj.MaxSize = size[0]
            mesh_obj.MinSize = size[1]
            mesh_obj.touch()
            netgen = nt.NetgenTools(mesh_obj)
            netgen.prepare()
            netgen.compute()

        obj.recompute()
        App.ActiveDocument.recompute()