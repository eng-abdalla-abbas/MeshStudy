import FreeCAD as App
import FreeCADGui as Gui

class MeshStudyProxy:
    # A proxy object to reprisent Mesh Study object
    def __init__(self, obj):
        obj.Proxy = self
        self.setup_properties(obj)

    def setup_properties(self, obj):

        # Group:
        obj.addExtension("App::GroupExtensionPython")

        # Main (General) Properties
        obj.addProperty("App::PropertyLink", "TheStudyTarget", "General", "The target Body/Analysis")
        obj.addProperty("App::PropertyFloatConstraint", "InitialMeshSize", "General", "Initial mesh size")
        obj.addProperty("App::PropertyInteger", "NumberOfRuns", "General", "Number of runs")
        obj.addProperty("App::PropertyFloatConstraint", "RefinementFactor", "General", "Refinement multiplier")

        # The Details Properties
        obj.addProperty("App::PropertyEnumeration", "AnalysisType", "TheDetails", "Analysis type")
        obj.addProperty("App::PropertyEnumeration", "Solver", "TheDetails", "Solver to use")
        obj.addProperty("App::PropertyEnumeration", "Mesher", "TheDetails", "Mesher to use")
        obj.addProperty("App::PropertyEnumeration", "QuantityOfInterest", "TheDetails", "Target QoI")
        obj.addProperty("App::PropertyFloatConstraint", "Tolerance", "TheDetails", "QoI Tolerance")

        # Internal Properties (links)
        obj.addProperty("App::PropertyLink", "MeshObject", "Internal")
        obj.addProperty("App::PropertyLink", "SolverObject", "Internal")
        obj.addProperty("App::PropertyStringList", "StudyResults", "Internal")

        # Default Values 
        obj.AnalysisType = ["Static structural", "Modal", "Thermal"]
        obj.Solver = ["CalculiX"]
        obj.Mesher = ["Gmsh", "Netgen"]
        obj.QuantityOfInterest = ["Stress", "Strain", "Displacement"]
        obj.Tolerance = (5.0, 0.1, 50.0, 0.1)
        obj.InitialMeshSize = 0.0
        obj.RefinementFactor = (0.5, 0.1, 1.0, 0.5)
        obj.NumberOfRuns = 5

    def execute(self, obj):
        # get called when recomputation in FreeCAD is triggered
        pass

class StudyResultProxy:
        def __init__(self, obj, results, child_index):
                obj.Proxy = self
                self.data = results
                self.indx =  child_index
                self.indexed_results = f"StudyResults{self.indx}"
                self.setup_properties(obj)
                

        
        def setup_properties(self, obj):

            obj.addProperty("App::PropertyStringList", self.indexed_results, "Internal")

            # Default Values 
            import json
            data = json.dumps(self.data)
            setattr(obj, self.indexed_results, data)
        
        def execute(self, obj):
                pass

def create_mesh_study():

    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument()
    
    obj = doc.addObject("App::FeaturePython", "MeshStudy")
    obj.Label = "Mesh Study"
    MeshStudyProxy(obj)
    
    if App.GuiUp:
        from objects.view_providers import MeshStudyViewProvider
        MeshStudyViewProvider(obj.ViewObject)
        
    return obj

def create_study_results(results):
    
    doc = App.ActiveDocument
    obj = doc.getObject("MeshStudy")

    #creat child object
    name = (obj.AnalysisType).split()[0]
    child = doc.addObject("App::FeaturePython", name)
    obj.addObject(child)

    child_index = 0
    for child in obj.Group:
          child_index += 1

    StudyResultProxy(child, results, child_index)
    child.recompute()
    
    # open results window
    if App.GuiUp:
        from objects.view_providers import StudyResultViewProvider
        StudyResultViewProvider(child.ViewObject)
        
    return child