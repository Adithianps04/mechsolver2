"""
Materials Module - Termux Version
Lightweight implementation of materials engineering calculations and properties
"""
import math
from typing import Dict, Union, Optional

# Common materials database
MATERIALS_DB = {
    "STEEL_1045": {
        "name": "Steel AISI 1045",
        "density": 7850,  # kg/m³
        "elastic_modulus": 205,  # GPa
        "poisson_ratio": 0.29,
        "yield_strength": 505,  # MPa
        "ultimate_strength": 585,  # MPa
        "thermal_conductivity": 49.8,  # W/(m·K)
        "thermal_expansion": 11.5e-6  # 1/K
    },
    "AL_6061": {
        "name": "Aluminum 6061-T6",
        "density": 2700,
        "elastic_modulus": 68.9,
        "poisson_ratio": 0.33,
        "yield_strength": 276,
        "ultimate_strength": 310,
        "thermal_conductivity": 167,
        "thermal_expansion": 23.6e-6
    },
    "BRASS_360": {
        "name": "Brass C360",
        "density": 8500,
        "elastic_modulus": 97,
        "poisson_ratio": 0.34,
        "yield_strength": 310,
        "ultimate_strength": 379,
        "thermal_conductivity": 115,
        "thermal_expansion": 20.3e-6
    }
}

def get_material_properties(material_code: str) -> Dict[str, float]:
    """Get properties of a specific material"""
    return MATERIALS_DB.get(material_code, {})

def calculate_stress_strain(
    force: float,  # in N
    area: float,  # in m²
    material_code: str
) -> Dict[str, float]:
    """Calculate stress and strain for given load and material"""
    properties = get_material_properties(material_code)
    if not properties:
        raise ValueError("Material not found in database")
    
    stress = force / area
    strain = stress / (properties["elastic_modulus"] * 1e9)
    safety_factor = properties["yield_strength"] * 1e6 / stress
    
    return {
        "stress": stress,
        "strain": strain,
        "safety_factor": safety_factor
    }

def thermal_expansion(
    material_code: str,
    initial_length: float,  # in m
    temperature_change: float  # in K
) -> Dict[str, float]:
    """Calculate thermal expansion"""
    properties = get_material_properties(material_code)
    if not properties:
        raise ValueError("Material not found in database")
    
    delta_l = initial_length * properties["thermal_expansion"] * temperature_change
    final_length = initial_length + delta_l
    
    return {
        "length_change": delta_l,
        "final_length": final_length,
        "strain": delta_l / initial_length
    }

def heat_conduction(
    material_code: str,
    area: float,  # in m²
    thickness: float,  # in m
    temperature_difference: float  # in K
) -> Dict[str, float]:
    """Calculate heat conduction through material"""
    properties = get_material_properties(material_code)
    if not properties:
        raise ValueError("Material not found in database")
    
    heat_flux = properties["thermal_conductivity"] * area * temperature_difference / thickness
    thermal_resistance = thickness / (properties["thermal_conductivity"] * area)
    
    return {
        "heat_flux": heat_flux,
        "thermal_resistance": thermal_resistance
    }

def material_cost_estimate(
    material_code: str,
    volume: float,  # in m³
    processing_factor: float = 1.0
) -> Dict[str, float]:
    """Estimate material cost"""
    # Approximate costs per kg (USD)
    material_costs = {
        "STEEL_1045": 2.5,
        "AL_6061": 4.8,
        "BRASS_360": 7.2
    }
    
    properties = get_material_properties(material_code)
    if not properties:
        raise ValueError("Material not found in database")
    
    mass = properties["density"] * volume
    base_cost = mass * material_costs.get(material_code, 0)
    total_cost = base_cost * processing_factor
    
    return {
        "mass": mass,
        "material_cost": base_cost,
        "total_cost": total_cost
    }

def calculator():
    """Interactive materials calculator"""
    while True:
        print("\n=== Materials Calculator ===")
        print("1: Material Properties")
        print("2: Stress-Strain Analysis")
        print("3: Thermal Expansion")
        print("4: Heat Conduction")
        print("5: Cost Estimation")
        print("B: Back to Main Menu")
        
        choice = input("Select calculation: ").strip().upper()
        
        if choice == "B":
            return
            
        if choice == "1":
            print("\nAvailable Materials:")
            for code, props in MATERIALS_DB.items():
                print(f"{code}: {props['name']}")
            
            material = input("\nEnter material code: ").strip().upper()
            properties = get_material_properties(material)
            
            if properties:
                print("\nMaterial Properties:")
                for prop, value in properties.items():
                    print(f"{prop}: {value}")
            else:
                print("Material not found")
                
        elif choice == "2":
            try:
                material = input("Enter material code: ").strip().upper()
                force = float(input("Enter force (N): "))
                area = float(input("Enter cross-sectional area (m²): "))
                
                results = calculate_stress_strain(force, area, material)
                print("\nResults:")
                print(f"Stress: {results['stress']/1e6:.2f} MPa")
                print(f"Strain: {results['strain']*100:.4f}%")
                print(f"Safety Factor: {results['safety_factor']:.2f}")
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "3":
            try:
                material = input("Enter material code: ").strip().upper()
                length = float(input("Enter initial length (m): "))
                temp_change = float(input("Enter temperature change (K): "))
                
                results = thermal_expansion(material, length, temp_change)
                print("\nResults:")
                print(f"Length change: {results['length_change']*1000:.3f} mm")
                print(f"Final length: {results['final_length']*1000:.3f} mm")
                print(f"Thermal strain: {results['strain']*100:.4f}%")
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "4":
            try:
                material = input("Enter material code: ").strip().upper()
                area = float(input("Enter cross-sectional area (m²): "))
                thickness = float(input("Enter thickness (m): "))
                temp_diff = float(input("Enter temperature difference (K): "))
                
                results = heat_conduction(material, area, thickness, temp_diff)
                print("\nResults:")
                print(f"Heat flux: {results['heat_flux']:.2f} W")
                print(f"Thermal resistance: {results['thermal_resistance']:.4f} K/W")
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "5":
            try:
                material = input("Enter material code: ").strip().upper()
                volume = float(input("Enter volume (m³): "))
                factor = float(input("Enter processing factor (default=1.0): ") or 1.0)
                
                results = material_cost_estimate(material, volume, factor)
                print("\nResults:")
                print(f"Mass: {results['mass']:.2f} kg")
                print(f"Material cost: ${results['material_cost']:.2f}")
                print(f"Total cost: ${results['total_cost']:.2f}")
                
            except ValueError as e:
                print(f"Error: {e}")
        
        else:
            print("Invalid choice, please try again")
            
        input("\nPress Enter to continue...")
