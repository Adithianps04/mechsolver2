"""
Thermodynamics Module - Termux Version
Optimized for mobile devices with lightweight calculations
"""
import math
from typing import Dict, Union, Optional

def ideal_gas_law(
    pressure: Optional[float] = None,
    volume: Optional[float] = None,
    moles: Optional[float] = None,
    temperature: Optional[float] = None,
    gas_constant: float = 8.314
) -> Dict[str, float]:
    """Calculate ideal gas law parameters (PV = nRT)"""
    if sum(x is None for x in [pressure, volume, moles, temperature]) != 1:
        raise ValueError("Exactly three parameters must be provided")
    
    if pressure is None:
        pressure = (moles * gas_constant * temperature) / volume
        return {"pressure": pressure}
    elif volume is None:
        volume = (moles * gas_constant * temperature) / pressure
        return {"volume": volume}
    elif moles is None:
        moles = (pressure * volume) / (gas_constant * temperature)
        return {"moles": moles}
    else:
        temperature = (pressure * volume) / (moles * gas_constant)
        return {"temperature": temperature}

def heat_transfer(area: float, k: float, temp_diff: float, thickness: float, mode: str = "conduction") -> float:
    """Calculate heat transfer rate using basic formulas"""
    if mode == "conduction":
        return k * area * temp_diff / thickness
    elif mode == "convection":
        return k * area * temp_diff
    else:
        return k * area * (math.pow(temp_diff, 4))

def steam_properties(temperature: float, pressure: float) -> Dict[str, float]:
    """
    Calculate approximate steam properties using simpler correlations
    Temperature in Celsius, Pressure in bar
    """
    # Simple approximations valid for moderate pressures and temperatures
    t_k = temperature + 273.15
    specific_volume = 0.0010  # Approximate for water at room temp
    
    if temperature > 100:  # Steam region
        specific_volume = (8.314 * t_k) / (pressure * 100000)  # Ideal gas approximation
        
    enthalpy = 4.186 * temperature  # Simple approximation
    entropy = 4.186 * math.log(t_k / 273.15)  # Simple approximation
    
    return {
        "specific_volume": specific_volume,
        "enthalpy": enthalpy,
        "entropy": entropy
    }

def calculator():
    """Interactive thermodynamics calculator"""
    while True:
        print("\n=== Thermodynamics Calculator ===")
        print("1: Ideal Gas Law")
        print("2: Heat Transfer")
        print("3: Steam Properties")
        print("B: Back to Main Menu")
        
        choice = input("Select calculation: ").strip().upper()
        
        if choice == "B":
            return
            
        if choice == "1":
            print("\nIdeal Gas Law Calculator (PV = nRT)")
            try:
                p = float(input("Pressure (Pa, or enter 0 to solve for P): ") or 0)
                v = float(input("Volume (m³, or enter 0 to solve for V): ") or 0)
                n = float(input("Moles (mol, or enter 0 to solve for n): ") or 0)
                t = float(input("Temperature (K, or enter 0 to solve for T): ") or 0)
                
                args = {}
                if p != 0: args['pressure'] = p
                if v != 0: args['volume'] = v
                if n != 0: args['moles'] = n
                if t != 0: args['temperature'] = t
                
                result = ideal_gas_law(**args)
                print("\nResult:", result)
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            try:
                area = float(input("Area (m²): "))
                k = float(input("Thermal conductivity/coefficient (W/m·K): "))
                temp_diff = float(input("Temperature difference (K): "))
                thickness = float(input("Thickness (m): "))
                mode = input("Mode (conduction/convection/radiation): ").lower()
                
                result = heat_transfer(area, k, temp_diff, thickness, mode)
                print(f"\nHeat transfer rate: {result:.2f} W")
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "3":
            try:
                temp = float(input("Temperature (°C): "))
                press = float(input("Pressure (bar): "))
                
                props = steam_properties(temp, press)
                print("\nSteam Properties:")
                for prop, value in props.items():
                    print(f"{prop}: {value:.4f}")
            except ValueError as e:
                print(f"Error: {e}")
        
        else:
            print("Invalid choice, please try again")
