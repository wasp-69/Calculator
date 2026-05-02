# Calculator

Language: Python 3.13.5
Calculator Version: 3.0 stable.
CLI calculator tool with broad functionality.
Contains instruction on how to use the program, must read.

Includes several util commands:
    ~ /History
    ~ /Sequence
    ~ /Example
    ~ /Memory
    ~ /Detail
    ~ /Variable
    ~ /Function
    
Includes both Pemdas and Letori evaluation sequences (which can be toggled at will).
Features a toggle to enable show-steps solving.
Features custom and built-in Variables and Functions.
Includes Implicit Multiplication wherever necessary.
Packages: Packages are a set of definitions (variable or functions) which can all be installed quickly using- /m a [-your-package-]

Variable Packages:
    Astrophysics = ["M_sun = 1.989e30", "R_sun = 6.957e8", "M_earth = 5.972e24", "R_earth = 6.371e6", "M_moon = 7.347e22", "R_moon = 1.737e6", "H0 = 70.0", "pc = 3.086e16", "ly = 9.461e15", "AU = 1.496e11"]
    QuantumMechanics = ["mp = 1.6726e-27", "mn = 1.6749e-27", "me = 9.1093e-31", "m_mu = 1.8835e-28", "e_charge = 1.6021e-19", "alpha = 0.007297", "Ry = 13.605", "hbar = 1.0545e-34", "sigma = 5.6703e-8", "wiens = 0.002897"]
    ThermoChemistry = ["Na = 6.0221e23", "R = 8.3144", "kB = 1.3806e-23", "F = 96485.3", "Vm = 0.02241", "k_coulomb = 8.9875e9", "eps0 = 8.8541e-12", "mu0 = 1.2566e-6", "G_ice = 334000", "L_steam = 2260000"]
    Engineering = ["phi = 1.61803", "atm = 101325", "rho_water = 1000", "rho_air = 1.225", "c_sound = 343", "G_standard = 6.6743e-11", "g_earth = 9.8066", "g_mars = 3.7207", "g_jupiter = 24.79", "stefan = 5.6703e-8"]

Function Packages:
    Conversion = ["c_to_f : x * 9 / 5 + 32", "/f d c_to_f Celsius to Fahrenheit", "f_to_c : ( x - 32 ) * 5 / 9", "/f d f_to_c Fahrenheit to Celsius", "k_to_c : x - 273.15", "/f d k_to_c Kelvin to Celsius", "kg_to_lb : x * 2.20462", "/f d kg_to_lb Kilograms to Pounds", "lb_to_kg : x / 2.20462", "/f d lb_to_kg Pounds to Kilograms", "m_to_ft : x * 3.28084", "/f d m_to_ft Meters to Feet", "ft_to_m : x / 3.28084", "/f d ft_to_m Feet to Meters", "km_to_mi : x * 0.621371", "/f d km_to_mi Kilometers to Miles", "mi_to_km : x / 0.621371", "/f d mi_to_km Miles to Kilometers"]
    Physics = ["kin_energy : 0.5 * m * x ^ 2", "/f d kin_energy Kinetic energy (needs m)", "pot_energy : m * g * x", "/f d pot_energy Potential energy (needs m, g)", "force_grav : G * m1 * m2 / x ^ 2", "/f d force_grav Gravity (needs G, m1, m2)", "ohm_v : x * r", "/f d ohm_v Voltage (needs r)", "ohm_i : v / x", "/f d ohm_i Current (needs v)", "weight_earth : x * g", "/f d weight_earth Weight on Earth (needs g)"]
    Chemistry = ["moles : x / molar_mass", "/f d moles Moles (needs molar_mass)", "photon_e : h * c / x", "/f d photon_e Photon Energy (needs h, c)", "molarity : x / v", "/f d molarity Molarity (needs v)", "wave_freq : c / x", "/f d wave_freq Frequency (needs c)"]
    Mathematics = ["area_circle : pi * x ^ 2", "/f d area_circle Area of circle", "vol_sphere : 4 / 3 * pi * x ^ 3", "/f d vol_sphere Volume of sphere", "hypotenuse : sqrt ( a ^ 2 + x ^ 2 )", "/f d hypotenuse Pyth. Theorem (needs a)", "deg_to_rad : x * pi / 180", "/f d deg_to_rad Degrees to Radians", "rad_to_deg : x * 180 / pi", "/f d rad_to_deg Radians to Degrees"]
    
