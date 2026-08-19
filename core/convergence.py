import FreeCAD as App

def check_convergence(data, tolerance):
    # Checking the convergence from the (Relative errors)
    App.Console.PrintMessage("\n--- Convergence Report ---\n")
    
    if len(data) <= 2:
        App.Console.PrintMessage("Not enough runs to determine convergence.\n")
        return

    App.Console.PrintMessage("Relative Error Convergence: ")
    
    for i in range(len(data)-1):
        CQoI = data[i+1]['QoI']
        PQoI = data[i]['QoI']

        # Avoiding Zero Division
        if PQoI == 0:
            continue
            
        error = abs(CQoI - PQoI) / PQoI
        
        if i <= (len(data) - 2):
            App.Console.PrintMessage(f"~{round(error * 100, 3)}%")
            
        if i != (len(data) - 2):
            App.Console.PrintMessage(" --> ")
        elif error <= tolerance and CQoI != PQoI:
            App.Console.PrintMessage(f"\n => Convergence achieved between run {i+1} and run {i+2}!\n")
            break
        elif i == (len(data) - 2):
            if CQoI == PQoI:
                App.Console.PrintMessage("\nSame Size Through All! No True Convergence Detected.\n")
            else:
                App.Console.PrintMessage("\nNot Converged!\n")