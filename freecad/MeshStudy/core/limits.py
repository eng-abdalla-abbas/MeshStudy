import FreeCAD as App

PARAM_PATH = "User parameter:BaseApp/Preferences/Mod/MeshStudy"

DEFAULT_MAX_ELEMENTS = 1_000_000
DEFAULT_MAX_NODES = 1_000_000


def check_mesh_limits(elements_count, nodes_count):
    prefs = App.ParamGet(PARAM_PATH)

    if not prefs.GetBool("EnableLimits", True):
        return False

    max_elements = prefs.GetInt("MaxElements", DEFAULT_MAX_ELEMENTS)
    max_nodes = prefs.GetInt("MaxNodes", DEFAULT_MAX_NODES)

    if elements_count > max_elements:
        App.Console.PrintError(
            f"Safety Limit Exceeded: "
            f"{elements_count} elements > {max_elements}\n"
        )
        return True

    if nodes_count > max_nodes:
        App.Console.PrintError(
            f"Safety Limit Exceeded: "
            f"{nodes_count} nodes > {max_nodes}\n"
        )
        return True

    return False