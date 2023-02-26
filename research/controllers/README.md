# Demo controllers


## Implemented controllers

  * ### [`C01_Sfp_V100_Dump_Controller`](C01_Sfp_V100_Dump.py)
    __or '_Dump Simple-Flagged Single-Cabin Controller_'__  
    Most basic controller - implements commands from in-cabin requests first, then commands from on-floor calls.
    No commands stack sorting provided.

  * ### [`C01_Sfp_V200_Basic_Controller`](C01_Sfp_V200_Basic.py) 
    __or '_Basic Simple-Flagged Single-Cabin Controller_'__

    Another simple controller, like [`C01_Sfp_V100_Dump_Controller`](C01_Sfp_V100_Dump.py), but provides commands stack sorting.
    Algorithms of this kind are used in most ordinary residential buildings.

  * ### [`C01_Sfp_V250_Basic_Controller`](C01_Sfp_V250_Advanced.py)
    __or '_Advanced Simple-Flagged Single-Cabin Controller_'__  
    Modified version of [`C01_V200_Sfp_Basic_Controller`](C01_Sfp_V200_Basic.py).
    Differs from it in that it returns the cabin to the first floor, when no other commands exist.
