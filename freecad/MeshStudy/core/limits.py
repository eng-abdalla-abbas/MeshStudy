import FreeCAD as App


MAX_ELEMENTS = 1_000_000
MAX_NODES = 500_000

def check_mesh_limits(results, elements_count, nodes_count):
   
    if elements_count > MAX_ELEMENTS:
        App.Console.PrintError(f"Safety Limit Exceeded: {elements_count} elements > {MAX_ELEMENTS}\n")
        return True
        
    if nodes_count > MAX_NODES:
        App.Console.PrintError(f"Safety Limit Exceeded: {nodes_count} nodes > {MAX_NODES}\n")
        return True
    
    return False