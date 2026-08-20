import FreeCAD as App

def check_convergence(data, tolerance):
    App.Console.PrintMessage("\n--- Convergence Report ---\n")
    
    if len(data) <= 2:
        App.Console.PrintMessage("Not enough runs to determine convergence.\n")
        return

    App.Console.PrintMessage("Relative Error Convergence: ")
    
    last_index = len(data) - 2
    all_same = True
    convergence = None
    is_currently_converged = False

    for i in range(len(data) - 1):
        CQoI = data[i+1]['QoI']
        PQoI = data[i]['QoI']

        if CQoI != PQoI:
            all_same = False

        # Handle zero division safely
        if PQoI == 0:
            App.Console.PrintMessage("N/A")
            is_currently_converged = False
        else:
            error = (abs(CQoI - PQoI) / abs(PQoI)) * 100 
            App.Console.PrintMessage(f"~{round(error, 3)}%")
            
            # Track convergence status and preserve the FIRST converged step, and restore the status if it diverges again.
            if error <= tolerance:
                is_currently_converged = True
                if convergence is None:
                    convergence = (i + 1, i + 2)
            else:
                is_currently_converged = False

        if i != last_index:
            App.Console.PrintMessage(" --> ")
            
    # Evaluate results in strict order of priority

    if all_same:
        App.Console.PrintMessage("\nSame Size Through All! No True Convergence Detected.\n")
    elif convergence and is_currently_converged:
        App.Console.PrintMessage(f"\n => Convergence achieved starting between run {convergence[0]} and run {convergence[1]}!\n")
    else:
        App.Console.PrintMessage("\nNot Converged!\n")