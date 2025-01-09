"""
Thermodynamics Module - Handles thermodynamic calculations
"""
import math
from typing import Dict, Union, Optional
import numpy as np

def ideal_gas_law(
    pressure: Optional[float] = None,
    volume: Optional[float] = None,
    moles: Optional[float] = None,
    temperature: Optional[float] = None,
    gas_constant: float = 8.314
) -> Dict[str, float]:
    """Calculate ideal gas law parameters (PV = nRT)"""
    if sum(x is None for x in [pressure, volume, moles, temperature]) != 1:
        raise ValueError("Exactly three parameters must be provided to solve for the fourth")
    
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

def carnot_efficiency(t_hot: float, t_cold: float) -> Dict[str, float]:
    """Calculate Carnot cycle efficiency"""
    if t_hot <= t_cold:
        raise ValueError("Hot temperature must be greater than cold temperature")
    
    efficiency = 1 - (t_cold / t_hot)
    return {
        "efficiency": efficiency,
        "efficiency_percent": efficiency * 100
    }

def heat_transfer(
    area: float,
    k: float,
    temp_diff: float,
    thickness: float,
    mode: str = "conduction"
) -> Dict[str, float]:
    """Calculate heat transfer rate"""
    results = {}
    
    if mode == "conduction":
        q = k * area * temp_diff / thickness
        results["heat_transfer_rate"] = q
        results["thermal_resistance"] = thickness / (k * area)
    
    elif mode == "convection":
        q = k * area * temp_diff  # k here is heat transfer coefficient h
        results["heat_transfer_rate"] = q
        results["thermal_resistance"] = 1 / (k * area)
    
    elif mode == "radiation":
        sigma = 5.67e-8  # Stefan-Boltzmann constant
        q = sigma * area * k * (temp_diff**4)  # k here is emissivity
        results["heat_transfer_rate"] = q
    
    return results

def steam_properties(
    temperature: float,
    pressure: float
) -> Dict[str, float]:
    """Calculate steam properties using correlations"""
    t_sat = 100 * (pressure / 1.013) ** 0.25
    
    # State determination
    if temperature < t_sat:
        state = "Compressed liquid"
        quality = 0
    elif temperature > t_sat:
        state = "Superheated vapor"
        quality = 1
    else:
        state = "Saturated"
        quality = 0.5
    
    # Properties calculation
    h_fg = 2257  # Latent heat of vaporization at 1 atm (kJ/kg)
    cp_water = 4.186  # Specific heat of water (kJ/kg·K)
    
    # Enthalpy calculation
    if state == "Compressed liquid":
        h = cp_water * temperature
    elif state == "Superheated vapor":
        h = h_fg + cp_water * temperature
    else:
        h = quality * h_fg + cp_water * temperature
    
    # Specific volume approximation (m³/kg)
    if state == "Compressed liquid":
        v = 0.001  # Approximate as water
    else:
        v = 0.018  # Simplified calculation
    
    return {
        "state": state,
        "quality": quality,
        "enthalpy": h,
        "specific_volume": v,
        "saturation_temperature": t_sat
    }

def psychrometric_properties(
    dry_bulb: float,
    wet_bulb: float,
    pressure: float = 101.325
) -> Dict[str, float]:
    """Calculate psychrometric properties of moist air"""
    # Constants
    Ra = 287.058  # Gas constant for air (J/kg·K)
    Rv = 461.495  # Gas constant for water vapor (J/kg·K)
    
    # Convert temperatures to Kelvin
    T_db = dry_bulb + 273.15
    T_wb = wet_bulb + 273.15
    
    # Saturation vapor pressure calculation (Buck equation)
    def p_sat(T):
        Tc = T - 273.15
        return 0.61121 * math.exp((18.678 - Tc/234.5) * (Tc/(257.14 + Tc)))
    
    # Calculate vapor pressures
    p_ws = p_sat(T_wb)
    p_vs = p_sat(T_db)
    
    # Humidity ratio at saturation (wet bulb)
    W_s = 0.62198 * p_ws/(pressure - p_ws)
    
    # Actual humidity ratio
    W = ((2501 - 2.326*wet_bulb)*W_s - 1.006*(dry_bulb - wet_bulb)) / \
        (2501 + 1.86*dry_bulb - 4.186*wet_bulb)
    
    # Relative humidity
    phi = W * pressure / (0.62198 * p_vs)
    
    # Specific volume
    v = Ra * T_db * (1 + 1.6078*W) / pressure
    
    # Enthalpy
    h = 1.006*dry_bulb + W*(2501 + 1.86*dry_bulb)
    
    # Dew point temperature (approximation)
    alpha = math.log(W * pressure / (0.62198 * 0.61121))
    Tdp = (243.5 * alpha) / (17.67 - alpha)
    
    return {
        "humidity_ratio": W,
        "relative_humidity": phi * 100,  # as percentage
        "specific_volume": v,
        "enthalpy": h,
        "dew_point": Tdp,
        "wet_bulb": wet_bulb,
        "dry_bulb": dry_bulb
    }

def refrigeration_cycle(
    evaporator_temp: float,
    condenser_temp: float,
    mass_flow: float,
    refrigerant: str = "R134a"
) -> Dict[str, float]:
    """Calculate basic vapor compression refrigeration cycle parameters"""
    # Simplified properties for R134a (you would use real property tables in practice)
    properties = {
        "R134a": {
            "h_fg": 200,  # kJ/kg (approximate)
            "cp": 1.43,   # kJ/kg·K
        }
    }
    
    if refrigerant not in properties:
        raise ValueError(f"Properties for {refrigerant} not available")
    
    prop = properties[refrigerant]
    
    # Calculate enthalpies at key points (simplified)
    h1 = prop["cp"] * evaporator_temp + prop["h_fg"]  # Evaporator outlet
    h2 = h1 + prop["cp"] * (condenser_temp - evaporator_temp)  # Compressor outlet
    h3 = prop["cp"] * condenser_temp  # Condenser outlet
    h4 = h3  # Assumed isenthalpic expansion
    
    # Calculate work and heat transfer
    w_comp = mass_flow * (h2 - h1)  # Compressor work
    q_evap = mass_flow * (h1 - h4)  # Cooling effect
    q_cond = mass_flow * (h2 - h3)  # Heat rejected
    
    # Calculate COP
    cop = q_evap / w_comp
    
    return {
        "compressor_work": w_comp,
        "cooling_effect": q_evap,
        "heat_rejected": q_cond,
        "cop": cop,
        "mass_flow_rate": mass_flow
    }

def heat_exchanger_design(
    hot_inlet_temp: float,
    hot_outlet_temp: float,
    cold_inlet_temp: float,
    mass_flow_hot: float,
    mass_flow_cold: float,
    cp_hot: float,
    cp_cold: float,
    overall_htc: float
) -> Dict[str, float]:
    """Design calculations for heat exchanger"""
    # Calculate heat transfer rate
    q = mass_flow_hot * cp_hot * (hot_inlet_temp - hot_outlet_temp)
    
    # Calculate cold fluid outlet temperature
    cold_outlet_temp = cold_inlet_temp + q / (mass_flow_cold * cp_cold)
    
    # Calculate LMTD
    delta_t1 = hot_inlet_temp - cold_outlet_temp
    delta_t2 = hot_outlet_temp - cold_inlet_temp
    lmtd = (delta_t1 - delta_t2) / math.log(delta_t1 / delta_t2)
    
    # Calculate required heat transfer area
    area = q / (overall_htc * lmtd)
    
    # Calculate effectiveness
    q_max = min(mass_flow_hot * cp_hot, mass_flow_cold * cp_cold) * \
            (hot_inlet_temp - cold_inlet_temp)
    effectiveness = q / q_max
    
    return {
        "heat_transfer_rate": q,
        "cold_outlet_temp": cold_outlet_temp,
        "lmtd": lmtd,
        "required_area": area,
        "effectiveness": effectiveness,
        "ntu": overall_htc * area / (min(mass_flow_hot * cp_hot, mass_flow_cold * cp_cold))
    }
