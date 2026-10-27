import math
import os
import numpy as np

def main():
    # ==================================================================================================
    # PLANETARY GEAR TRAIN; Ring fixed case only (w_ring = 0)
    # Sun Gear is the input; Carrier is the output; same rotation direction
    # GR = 1 + Nr/Ns formula <--- derived from setting w_ring = 0

    # User Inputs ======================================================================================
    TargetRatio     = 7       # desired GR = w_sun / w_carrier
    d_max           = 100        # mm; the max diameter that can fit in a contrained space
    RadiusOffset    = 1          # mm; Radius offset from the root diameter of the ring gear; use this for structure like putting screws
    phi             = 20         # pressure angle in degrees, can be left alone; must be 14.5, 20, or 25

    # Inializations ====================================================================================
    best = None         # will hold the best gear set
    Candidates = []     # enpty list; will hold other valid sets
    ModuleSet = np.arange(1,50,0.125)
    PlanetOptions = [6,5,4,3]


    os.system('cls' if os.name == 'nt' else 'clear')
        # the code checks os.name; if it equal 'nt' (Windows), it runs cls, otheriwse it runs clear

    class ExternalGear:
        def __init__(self,N,m,phi):     # initializes it by storing stuff, and calculating stuff
            self.teeth = N
            self.module = m
            self.PressureAngle = phi
            self.pitch  = N*m           # pitch diameter of external gear
            match phi:
                case 14.5:
                    self.addendum = m*1
                    self.dedendum = m*1.157
                case 20 | 25:
                    self.addendum = m*1
                    self.dedendum = m*1.25
            self.tip    = self.pitch +2*self.addendum    # tip diameter of external gear
            self.root   = self.pitch -2*self.dedendum    # root diameter of external gear
            self.base   = self.pitch * math.cos(math.radians(phi))    #base diameter of the external gear
        def __repr__(self):
            return (f"ExternalGear(N={self.teeth}, m={self.module}, phi={self.PressureAngle}, pitch={self.pitch}, tip={self.tip}, root={self.root})")

    class InternalGear:
        def __init__(self,N,m,phi):     # initializes it by storing stuff, and calculating stuff
            self.teeth = N
            self.module = m
            self.PressureAngle = phi
            self.pitch  = N*m           # pitch diameter of internal gear
            match phi:
                case 14.5:
                    self.addendum = m*1
                    self.dedendum = m*1.157
                case 20 | 25:
                    self.addendum = m*1
                    self.dedendum = m*1.25
            self.tip    = self.pitch -2*self.addendum    # tip diameter of internal gear
            self.root   = self.pitch +2*self.dedendum    # root diameter of internal gear
            self.base   = self.pitch * math.cos(math.radians(phi))  #base diameter of the internal gear
        def __repr__(self):
            return (f"ExternalGear(N={self.teeth}, m={self.module}, phi={self.PressureAngle}, pitch={self.pitch}, tip={self.tip}, root={self.root})")


    for m in ModuleSet:
        # print(round(float(m),3))
        
        match phi:
            case 14.5:
                addendum = m*1
                dedendum = m*1.157
            case 20 | 25:
                addendum = m*1
                dedendum = m*1.25

        # Make Ring Gear
        d_ring_root = d_max - 2*RadiusOffset    # calculates the root diameter of the internal ring gear
        d_ring_pitch = d_ring_root -2*dedendum   # calculates the pitch diameter of the internal ring gear
        N_r = int(d_ring_pitch/m)
        if N_r < 6:
            continue    # skips to next iteration since N_r <6
        Ring = InternalGear(N_r,m,phi)

        # Make Sun Gear
        N_s = int(N_r/(TargetRatio-1))          # Solves GR=1+Nr/Ns; floors down to the nearest teeth
        if N_s < 6:
            continue    # skips to next iteration since N_s <6
        Sun = ExternalGear(N_s,m,phi)
        if Sun.root < 6:
            continue            # skips to the next iteration if it is smaller than 6mm
        # print(Sun)        # this is check the sun gear and its dimensions

        # Make Planet Gear
        N_p = (N_r-N_s)/2       # Solves N_r = 2N_p + N_s
        if N_p <= 0 or N_p != int(N_p):
            continue  # skips to next iteration if N_p is negative or a decimal
        Planet = ExternalGear(N_p,m,phi)
        if Planet.root < 6:
            continue            # skips to the next iteration if it is smaller than 6mm
        # print(Planet)        # this is check the Planet gear and its dimensions


        for num_planets in PlanetOptions:
            # Condition # 1
            if (N_s + N_r) % num_planets != 0:  # checks (Ns+Nr) % num_planets == 0; must be an integer; eq 6.3-5     
                continue                        # skips to the next iteration if it aint a integer

            # condition # 2
                # n < 180° / arcsin( (N_p + 2*alpha) / (N_s + N_p) )
            alpha = 1           # alpha = 1 for full-depth teeth
            ratio = (N_p + 2*alpha) / (N_s + N_p)
            if ratio >= 1:              # arcsin can only take an answer less than 1
                continue                # skips to next iteration
            max_n = 180 / math.degrees(math.asin(ratio))
                # math.asin returns the answer in radians
                # math.degrees returns the answer in degrees
            if num_planets > max_n:
                continue                # skips if num_planet exceeds max_n

            GR_actual = 1 + N_r/N_s                     # the real ratio 
            ratio_error = abs(GR_actual-TargetRatio)   # how far off the target_ratio
            unused_space = d_ring_pitch - m*N_r         # leftover space not used by the ring gear

            candidate = (ratio_error, unused_space, m, N_s, N_p, N_r, num_planets, GR_actual)
                # create a tuple called 'candidate', which is a single value; designated by the curvy brackets
            Candidates.append(candidate)        # adds the tuple 'candidate' to the 'Candidates' list
            if best is None or candidate < best:
                best = candidate    # replaces the best if the candidate's ratio_error, and then unused_space is the least
    # asdfasdfasdfs
    # UNPACKING THE BEST CANDIDATE ====================================================================================
    if best is None:
        print("No valid gear set found. Try a larger d_max or different ratio.")
            # if there is no "best" found, it will give an error
    else:
        ratio_error, unused_space, m, N_s, N_p, N_r, num_planets, GR_actual= best
            # unpacks the tuples into individual values    
        Ring = InternalGear(N_r,m,phi)
        Planet = ExternalGear(N_p,m,phi)
        Sun = ExternalGear(N_s,m,phi)

        print("BEST COMBINATION ================================================================")
        print(f"m    module             = {m}")
        print(f"N_s  sun teeth          = {N_s}")
        print(f"N_p  planet teeth       = {N_p}")
        print(f"N_r  ring teeth         = {N_r}")
        print(f"k    number of planets  = {num_planets}")
        print(f"Actual Gear Ratio       = {GR_actual:.2f} (target was {TargetRatio})")
        print(f"Torque has now increased by {GR_actual:.2f}x times!")
        print(f"Speed has now decreased by {GR_actual:.2f}x times!")
        C_sp = (Sun.pitch + Planet.pitch)/2
        print(f"Sun to Planet disntance = {C_sp:.2f}")
        print(f"unused space            = {unused_space:.3f}mm")

        print()
        print("SolidWorks Equation =============================================================")
        print(f'"m"          = {m}\t \'module, mm')
        print(f'"phi"        = {phi}\t \'pressure angle, degrees')
        print(f'"N_s"        = {N_s}\t \'sun tooth count')
        print(f'"N_p"        = {N_p}\t \'planet tooth count')
        print(f'"N_r"        = {N_r}\t \'ring tooth count')
        print(f'"d_s_pitch"  = "m" * "N_s"\t \' sun pitch diameter')
        print(f'"d_p_pitch"  = "m" * "N_p"\t \' planet pitch diameter')
        print(f'"C_sp" = ("d_s_pitch" + "d_p_pitch")/2\t \' planet pitch diameter')

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
            for rank, (r_err, unused_space_i, m_i, N_s_i, N_p_i, N_r_i, k_i, GR_i) in enumerate(runners_up[:50], start=1):
                # typical syntax for enumerating ---> for index, contentstobeiterated in enumerate(given list, start=1)
                print(f"{rank:2d}. m={m_i:<5} Ns={N_s_i:<5} Np={N_p_i:<5} Nr={N_r_i:<5} k={k_i:<3} GR={GR_i:.4f}  err={r_err:.4f}  unused={unused_space_i:.2f}mm")
        print()

if __name__ == "__main__":      
    # __name__ is automatically set to __main__ when you run the file it self
    main() 


