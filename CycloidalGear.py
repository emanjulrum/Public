import numpy as np
import math
import os
import sys

def main():
    # USER INPUTS =====================================================================================================  
    # target_ratio    = int(sys.argv[1])
    target_ratio    =  25       
        # desired GR = w_out/w_in = w_Disc/w_CarrierOrInputShaft 
        # type following "python CycloidGear.py 25" to get a target_ratio fo 25  
        # cycloidal analog of Willis’ equation
    d_max           = 42         # mm; the max diameter that can fit in a contrained space 
    Offset_radius   = 2          # mm; Radius offset from the root diameter of the ring gear

    # INITIALIZATION ==================================================================================================
    best = None         # will hold the best gear set in terms of lowest ratio-error
    Candidates = []     # will hold the other valid candidates
    # PinDiameters = [1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 15, 16, 20, 25, 30]    # Can you use to get standardized dowel pins
    PinDiameters = np.arange(1,50,0.1)
        # standard metric dowel pins
    e_range = np.arange(0.5,20,0.1)             


    # MAIN CODE =======================================================================================================
    os.system('cls' if os.name == 'nt' else 'clear')
        # the code checks os.name; if it equal 'nt' (Windows), it runs cls, otheriwse it runs clear
    for e in e_range:
        e = round(float(e), 1)          # cleans up the decimal mess
        for d_r in PinDiameters:
            d_r = round(float(d_r), 1)

            # using two loops, find best combination for d_r and e
            delta = d_r - 2*e
            if e > delta/2:             # reject anything when the eccentricity is bigger than the radius of the rolling circle
                continue                # skips to the check iteration since it requires e <= delta/2
            # calculate n, N, D, size
            n = target_ratio            # number of lobes
            N = n + 1                   # number of roller pins
            D = delta * N               # pitch diameter of the rollers to be arranged
            size = D + d_r + 2*Offset_radius     # max possible size
            if d_max < size:            # reject the size if it goes over d_max
                continue                # skips to the next iteration if it goes over d_max
            unused_space = d_max - size # leftover space

            # Parametric equation condition
            condition = D/(2*N*e)       # this condition is also called 1/K1, that K1 is the "Shortening coefficient"
            if condition <= 1.1:
                continue                # skips this combo since the parametric eqns would fail/be discontinuous in SolidWorks
                
            # Calculate the tip and root diameter of the cycloidal disc
            d_bc_tip = delta * target_ratio                     # base circle; the tip of the lobes
            d_bc_root = (d_bc_tip + 2*(delta/2 - e - d_r/2))    # root of the lobes

            # Calculate the clearance between the root of the lobe and the d_h
            d_clearance1_upper =  d_bc_root
            clearance1 = 1.5          #mm; radial clearance between the lobes and the d_h
            d_clearance1_lower = d_clearance1_upper - 2*clearance1

            # Calculate the max diameter for load pins
            d_l =  5                            # mm  M3D5 sleeves will be used for M3 screws; diameter of the load pins
            d_h = d_l + 2*e                     # holes of cycloidial disc
            d_p = d_clearance1_lower - d_h      # pitch diameter for the holes 

            # Calculate the clerance between the d_h and the eccentric shaft
            d_clearance2_upper = d_clearance1_lower - 2*d_h
            clearance2 = 1.5          #mm; the radial clearance between the d_h and the shaft
            d_clearance2_lower = d_clearance2_upper - 2*clearance2

            K1 = e * N / (D/2)
            
            candidate = (unused_space, N, d_r, D, n, e, d_bc_tip, d_bc_root, d_h, d_p, d_clearance2_lower)
                # create a tuple called 'candidate', which is a single value; designated by the curvy brackets
            Candidates.append(candidate)        # adds the tuple 'candidate' to the 'Candidates' list
            Candidates.sort(key=lambda z: (z[0], -z[10]))    # sorts the Candidate list by z[0] least "unused spaced" and then -z[10] most "d_clearance2_lower"
            if best is None or candidate < best:
                best = candidate    # replaces the best


    # UNPACKING THE BEST CANDIDATE ====================================================================================
    if best is None:
        print("No valid gear set found. Try a larger d_max or different ratio.")
            # if there is no "best" found, it will give an error
    else:
        unused_space, N, d_r, D, n, e, d_bc_tip, d_bc_root, d_h, d_p, d_clearance2_lower = best
            # unpacks the tuples into individual values
        print("BEST COMBINATION ================================================================")
        print(f"If the output is the load disc")
        print(f"i_a transmition ratio  w_out/w_in = w_disc/w_carrierinput = -1/{target_ratio}\t={-1/target_ratio:.5f}")
        print(f"Torque has now increased by {target_ratio}x times!")
        print(f"Speed has now decreased by {target_ratio}x times!")
        print()
        print(f"If the output is the ring gear")
        print(f"i_b transmition ratio        = 1/{target_ratio + 1}\t={-1/(target_ratio+1):.5f} if the output is the load disc")
        print(f"Torque has now increased by {target_ratio+1}x times!")
        print(f"Speed has now decreased by {target_ratio+1}x times!")
        print()
        print(f"Ring gear info:")
        print(f"\tN roller pins             = {N:>5}")
        print(f"\td_r roller diameter       = {d_r:>5.2f}")
        print(f"\tD dia pitch for rollers   = {D:>5.2f}")
        print(f"\tD_out roller boundary     = {D+d_r:>5.2f}")
        print(f"\td_max actual boundary     = {D+d_r+2*Offset_radius:>5.2f} which is equal or less than d_max={d_max}")
        print(f"Cyloid gear info:")
        print(f"\tt lobes                   = {n:>5}")
        print(f"\te eccentricity            = {e:>5}")
        print(f"\td tip  dia of lobe        = {d_bc_tip:>5.2f}")
        print(f"\td root dia of lobe        = {d_bc_root:>5.2f}")
        print()
        print(f"\td_h dia of load pin       = {d_h:>5.2f}")    
        print(f"\td_p pitch dia of load pin = {d_p:>5.2f}")
        print(f"\tavailable space for shaft = {d_clearance2_lower:>5.2f}; this is usually for the OD of bearing")
        print()
        print(f"\tunused_space               ={unused_space:>5.2f}")    
        print()
        print(f"Parametric Equations for Cycloidal:")
        print(f"\t  {D:.2f}*cos(t)/2-{d_r}*cos(t+arctan(sin(t*(-1+{N}))/(-{D:.2f}/(2*{N}*{e})+cos(t*(-1+{N})))))/2-{e}*cos({N}*t)")
        print(f"\t -{D:.2f}*sin(t)/2+{d_r}*sin(t+arctan(sin(t*(-1+{N}))/(-{D:.2f}/(2*{N}*{e})+cos(t*(-1+{N})))))/2+{e}*sin({N}*t)")
        print(f"t1=0 \t t2=pi")
        print()
        
        print("ALL OTHER COMBINATIONS ==========================================================")
        # sort the rest of the combinations
        ranked = sorted(Candidates)                     # sorts Candidates based on the first values
        runners_up = [c for c in ranked if c != best]
            # create list comprehension; create a list based on the 'ranked' list given that the 'c' is not the 'best'

        # print the rest of the combinations
        if not runners_up:                        # checks if is blank; runners_up == ""
            print("No other possibilites found")
        else:
            print(f"rank\tunused_space\tN\td_r\tD\t| n\te\td_bc_tip\td_bc_root\t| d_h\td_p\td_clearance2_lower")
            for rank, (unused_spacei, Ni, d_ri, Di, ni, ei, d_bc_tipi, d_bc_rooti, d_hi, d_pi, d_clearance2_loweri) in enumerate(runners_up[:50], start=1):
                # typical syntax for enumerating ---> for index, contentstobeiterated in enumerate(given list, start=1)
                
                print(f"{rank:2d}.\t{unused_spacei:<12.1f}\t{Ni:<5}\t{d_ri:<5}\t{Di:.2f}\t| {ni:<5}\t{ei:<5}\t{d_bc_tipi:.2f}\t\t{d_bc_rooti:.2f}\t\t| {d_hi:.2f}\t{d_pi:.2f}\t{d_clearance2_loweri:.2f}")
                    # < means left align
                    # 5 means the width of the text
                    # .2f means the number of places after the decimal and f means formated as float point
        print()


if __name__ == "__main__":      
    # __name__ is automatically set to __main__ when you run the file it self
    main() 