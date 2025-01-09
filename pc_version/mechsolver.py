#!/usr/bin/env python3
"""
MechSolver - A comprehensive mechanical engineering calculator
"""
import sys
from typing import Dict, Any, Optional
from modules import kinematics, stress_analysis, fluid_mechanics, thermodynamics

def clear_screen():
    """Clear the console screen"""
    print('\n' * 50)

def get_float_input(prompt: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> float:
    """Get validated float input from user"""
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Value must be greater than {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be less than {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")

def get_choice(options: Dict[str, str], prompt: str = "Enter your choice: ") -> str:
    """Get validated choice from user"""
    while True:
        print("\nAvailable options:")
        for key, value in options.items():
            print(f"{key}: {value}")
        choice = input(prompt).strip().upper()
        if choice in options:
            return choice
        print("Invalid choice. Please try again.")

def kinematics_calculator():
    """Handle kinematics calculations"""
    options = {
        '1': 'Basic Motion Analysis',
        '2': 'Projectile Motion',
        '3': 'Simple Harmonic Motion',
        '4': 'Four-bar Mechanism',
        '5': 'Gear Train Analysis',
        '6': 'Cam Analysis',
        'B': 'Back to Main Menu'
    }
    
    while True:
        choice = get_choice(options, "Select kinematics calculation: ")
        if choice == 'B':
            return
            
        clear_screen()
        if choice == '1':
            velocity = get_float_input("Enter initial velocity (m/s): ")
            acceleration = get_float_input("Enter acceleration (m/s²): ")
            time = get_float_input("Enter time (s): ")
            results = kinematics.solve_motion(velocity, acceleration, time)
            print("\nResults:")
            print(f"Displacement: {results['displacement']:.2f} m")
            print(f"Final Velocity: {results['final_velocity']:.2f} m/s")
            
        elif choice == '2':
            velocity = get_float_input("Enter initial velocity (m/s): ")
            angle = get_float_input("Enter launch angle (degrees): ", 0, 90)
            height = get_float_input("Enter initial height (m): ", 0)
            air_resistance = input("Consider air resistance? (y/n): ").lower() == 'y'
            
            if air_resistance:
                drag_coeff = get_float_input("Enter drag coefficient (default 0.1): ", 0)
                results = kinematics.projectile_motion(velocity, angle, height, air_resistance=True, drag_coefficient=drag_coeff)
            else:
                results = kinematics.projectile_motion(velocity, angle, height)
            
            print("\nResults:")
            print(f"Maximum Height: {results['max_height']:.2f} m")
            print(f"Range: {results['range']:.2f} m")
            print(f"Time of Flight: {results['time_of_flight']:.2f} s")
            
        elif choice == '3':
            amplitude = get_float_input("Enter amplitude (m): ")
            frequency = get_float_input("Enter frequency (Hz): ", 0)
            phase = get_float_input("Enter phase angle (degrees): ")
            time = get_float_input("Enter time (s): ", 0)
            
            results = kinematics.simple_harmonic_motion(amplitude, frequency, time, phase)
            print("\nResults:")
            print(f"Displacement: {results['displacement']:.2f} m")
            print(f"Velocity: {results['velocity']:.2f} m/s")
            print(f"Acceleration: {results['acceleration']:.2f} m/s²")
            print(f"Period: {results['period']:.2f} s")
            
        elif choice == '4':
            crank = get_float_input("Enter crank length (m): ", 0)
            coupler = get_float_input("Enter coupler length (m): ", 0)
            rocker = get_float_input("Enter rocker length (m): ", 0)
            ground = get_float_input("Enter ground length (m): ", 0)
            angle = get_float_input("Enter crank angle (degrees): ")
            
            results = kinematics.four_bar_mechanism(crank, coupler, rocker, ground, angle)
            print("\nResults:")
            print(f"Rocker Angle: {results['rocker_angle']:.2f} degrees")
            print(f"Coupler Angle: {results['coupler_angle']:.2f} degrees")
            
        elif choice == '5':
            n_gears = int(get_float_input("Enter number of gears: ", 2))
            teeth = []
            for i in range(n_gears):
                teeth.append(int(get_float_input(f"Enter number of teeth for gear {i+1}: ", 1)))
            input_speed = get_float_input("Enter input speed (rpm): ", 0)
            efficiency = get_float_input("Enter efficiency (0-1): ", 0, 1)
            
            results = kinematics.gear_train_analysis(teeth, input_speed, efficiency)
            print("\nResults:")
            print(f"Gear Ratio: {results['gear_ratio']:.3f}")
            print(f"Output Speed: {results['output_speed']:.2f} rpm")
            print(f"Overall Efficiency: {results['efficiency']:.2%}")
            
        elif choice == '6':
            base_radius = get_float_input("Enter base circle radius (m): ", 0)
            lift = get_float_input("Enter maximum lift (m): ", 0)
            angle = get_float_input("Enter cam angle (degrees): ")
            
            cam_types = {'1': 'simple_harmonic', '2': 'cycloidal', '3': 'parabolic'}
            print("\nCam Types:")
            for key, value in cam_types.items():
                print(f"{key}: {value}")
            cam_choice = input("Select cam type: ")
            
            results = kinematics.cam_analysis(base_radius, lift, angle, cam_types.get(cam_choice, 'simple_harmonic'))
            print("\nResults:")
            print(f"Displacement: {results['displacement']:.3f} m")
            print(f"Total Radius: {results['total_radius']:.3f} m")
        
        input("\nPress Enter to continue...")
        clear_screen()

def stress_analysis_calculator():
    """Handle stress analysis calculations"""
    options = {
        '1': 'Normal Stress and Strain',
        '2': 'Beam Bending',
        '3': 'Combined Stress',
        '4': 'Torsional Stress',
        '5': 'Fatigue Analysis',
        '6': 'Pressure Vessel',
        '7': 'Thermal Stress',
        'B': 'Back to Main Menu'
    }
    
    while True:
        choice = get_choice(options, "Select stress analysis calculation: ")
        if choice == 'B':
            return
            
        clear_screen()
        if choice == '1':
            force = get_float_input("Enter force (N): ")
            area = get_float_input("Enter area (m²): ", 0)
            youngs_modulus = get_float_input("Enter Young's modulus (Pa): ", 0)
            
            stress = stress_analysis.calculate_stress(force, area)
            strain = stress_analysis.calculate_strain(stress, youngs_modulus)
            
            print("\nResults:")
            print(f"Stress: {stress:.2e} Pa")
            print(f"Strain: {strain:.2e}")
            
        elif choice == '2':
            moment = get_float_input("Enter bending moment (N⋅m): ")
            distance = get_float_input("Enter distance from neutral axis (m): ", 0)
            inertia = get_float_input("Enter moment of inertia (m⁴): ", 0)
            
            stress = stress_analysis.beam_bending_stress(moment, distance, inertia)
            print("\nResults:")
            print(f"Bending Stress: {stress:.2e} Pa")
            
        elif choice == '3':
            normal = get_float_input("Enter normal stress (Pa): ")
            shear = get_float_input("Enter shear stress (Pa): ")
            
            results = stress_analysis.combined_stress(normal, shear)
            print("\nResults:")
            print(f"Principal Stress 1: {results['principal_stress_1']:.2e} Pa")
            print(f"Principal Stress 2: {results['principal_stress_2']:.2e} Pa")
            print(f"Maximum Shear Stress: {results['max_shear_stress']:.2e} Pa")
            print(f"Principal Angle: {results['angle_principal']:.2f}°")
            
        elif choice == '4':
            torque = get_float_input("Enter torque (N⋅m): ")
            radius = get_float_input("Enter shaft radius (m): ", 0)
            polar_moment = get_float_input("Enter polar moment of inertia (m⁴): ", 0)
            
            results = stress_analysis.torsional_stress(torque, radius, polar_moment)
            print("\nResults:")
            print(f"Shear Stress: {results['shear_stress']:.2e} Pa")
            
        elif choice == '5':
            stress_max = get_float_input("Enter maximum stress (Pa): ")
            stress_min = get_float_input("Enter minimum stress (Pa): ")
            ultimate = get_float_input("Enter ultimate strength (Pa): ", 0)
            endurance = get_float_input("Enter endurance limit (Pa): ", 0)
            
            results = stress_analysis.fatigue_analysis(stress_max, stress_min, ultimate, endurance)
            print("\nResults:")
            print(f"Safety Factor: {results['safety_factor']:.2f}")
            print(f"Modified Endurance Limit: {results['modified_endurance_limit']:.2e} Pa")
            print(f"Cycles to Failure: {results['cycles_to_failure']:.2e}")
            
        elif choice == '6':
            pressure = get_float_input("Enter internal pressure (Pa): ", 0)
            radius = get_float_input("Enter vessel radius (m): ", 0)
            thickness = get_float_input("Enter wall thickness (m): ", 0)
            
            vessel_types = {'1': 'thin_cylinder', '2': 'thick_cylinder', '3': 'sphere'}
            print("\nVessel Types:")
            for key, value in vessel_types.items():
                print(f"{key}: {value}")
            vessel_choice = input("Select vessel type: ")
            
            results = stress_analysis.pressure_vessel_stress(pressure, radius, thickness, 
                                                          vessel_types.get(vessel_choice, 'thin_cylinder'))
            print("\nResults:")
            if 'hoop_stress' in results:
                print(f"Hoop Stress: {results['hoop_stress']:.2e} Pa")
            if 'longitudinal_stress' in results:
                print(f"Longitudinal Stress: {results['longitudinal_stress']:.2e} Pa")
            if 'von_mises_stress' in results:
                print(f"Von Mises Stress: {results['von_mises_stress']:.2e} Pa")
                
        elif choice == '7':
            temp_change = get_float_input("Enter temperature change (K): ")
            expansion = get_float_input("Enter thermal expansion coefficient (1/K): ")
            youngs_modulus = get_float_input("Enter Young's modulus (Pa): ", 0)
            
            constraint_types = {'1': 'full', '2': 'partial'}
            print("\nConstraint Types:")
            for key, value in constraint_types.items():
                print(f"{key}: {value}")
            constraint_choice = input("Select constraint type: ")
            
            results = stress_analysis.thermal_stress(temp_change, expansion, youngs_modulus,
                                                   constraint_types.get(constraint_choice, 'full'))
            print("\nResults:")
            print(f"Thermal Stress: {results['thermal_stress']:.2e} Pa")
            print(f"Thermal Strain: {results['thermal_strain']:.2e}")
        
        input("\nPress Enter to continue...")
        clear_screen()

def fluid_mechanics_calculator():
    """Handle fluid mechanics calculations"""
    options = {
        '1': 'Reynolds Number',
        '2': 'Pipe Flow',
        '3': 'Pump Analysis',
        '4': 'Drag Force',
        '5': 'Bernoulli Equation',
        '6': 'Open Channel Flow',
        '7': 'Weir Flow',
        '8': 'Wave Properties',
        'B': 'Back to Main Menu'
    }
    
    while True:
        choice = get_choice(options, "Select fluid mechanics calculation: ")
        if choice == 'B':
            return
            
        clear_screen()
        if choice == '1':
            velocity = get_float_input("Enter fluid velocity (m/s): ")
            length = get_float_input("Enter characteristic length (m): ", 0)
            viscosity = get_float_input("Enter kinematic viscosity (m²/s): ", 0)
            
            re = fluid_mechanics.reynolds_number(velocity, length, viscosity)
            print("\nResults:")
            print(f"Reynolds Number: {re:.2e}")
            if re < 2300:
                print("Flow is laminar")
            elif re > 4000:
                print("Flow is turbulent")
            else:
                print("Flow is transitional")
                
        elif choice == '2':
            length = get_float_input("Enter pipe length (m): ", 0)
            diameter = get_float_input("Enter pipe diameter (m): ", 0)
            velocity = get_float_input("Enter flow velocity (m/s): ", 0)
            friction = get_float_input("Enter friction factor: ", 0)
            
            include_minor = input("Include minor losses? (y/n): ").lower() == 'y'
            minor_losses = {}
            if include_minor:
                n_losses = int(get_float_input("Enter number of minor loss components: ", 1))
                for i in range(n_losses):
                    k = get_float_input(f"Enter loss coefficient for component {i+1}: ", 0)
                    count = int(get_float_input(f"Enter count of component {i+1}: ", 1))
                    minor_losses[f"component_{i+1}"] = k * count
            
            results = fluid_mechanics.pipe_head_loss(length, diameter, velocity, friction, minor_losses)
            print("\nResults:")
            print(f"Major Head Loss: {results['major_loss']:.2f} m")
            print(f"Minor Head Loss: {results['minor_loss']:.2f} m")
            print(f"Total Head Loss: {results['total_loss']:.2f} m")
            
        elif choice == '3':
            flow_rate = get_float_input("Enter flow rate (m³/s): ", 0)
            head = get_float_input("Enter total head (m): ", 0)
            efficiency = get_float_input("Enter pump efficiency (0-1): ", 0, 1)
            
            results = fluid_mechanics.pump_power(flow_rate, head, efficiency)
            print("\nResults:")
            print(f"Hydraulic Power: {results['hydraulic_power']/1000:.2f} kW")
            print(f"Shaft Power: {results['shaft_power']/1000:.2f} kW")
            
        elif choice == '4':
            velocity = get_float_input("Enter velocity (m/s): ")
            area = get_float_input("Enter reference area (m²): ", 0)
            cd = get_float_input("Enter drag coefficient: ", 0)
            density = get_float_input("Enter fluid density (kg/m³): ", 0)
            
            results = fluid_mechanics.drag_force(velocity, density, area, cd)
            print("\nResults:")
            print(f"Drag Force: {results['drag_force']:.2f} N")
            print(f"Dynamic Pressure: {results['dynamic_pressure']:.2f} Pa")
            
        elif choice == '5':
            h1 = get_float_input("Enter height at point 1 (m): ")
            v1 = get_float_input("Enter velocity at point 1 (m/s): ")
            p1 = get_float_input("Enter pressure at point 1 (Pa): ")
            h2 = get_float_input("Enter height at point 2 (m): ")
            
            solve_for = get_choice({'1': 'Velocity', '2': 'Pressure'}, "Solve for: ")
            if solve_for == '1':
                p2 = get_float_input("Enter pressure at point 2 (Pa): ")
                results = fluid_mechanics.bernoulli_equation(h1, v1, p1, h2, pressure2=p2)
                print(f"\nVelocity at point 2: {results['velocity2']:.2f} m/s")
            else:
                v2 = get_float_input("Enter velocity at point 2 (m/s): ")
                results = fluid_mechanics.bernoulli_equation(h1, v1, p1, h2, velocity2=v2)
                print(f"\nPressure at point 2: {results['pressure2']:.2f} Pa")
                
        elif choice == '6':
            width = get_float_input("Enter channel width (m): ", 0)
            depth = get_float_input("Enter flow depth (m): ", 0)
            slope = get_float_input("Enter channel slope (m/m): ", 0)
            manning = get_float_input("Enter Manning's n: ", 0)
            
            results = fluid_mechanics.open_channel_flow(width, depth, slope, manning)
            print("\nResults:")
            print(f"Flow Rate: {results['flow_rate']:.3f} m³/s")
            print(f"Velocity: {results['velocity']:.2f} m/s")
            print(f"Froude Number: {results['froude_number']:.2f}")
            print(f"Flow Type: {results['flow_type']}")
            
        elif choice == '7':
            height = get_float_input("Enter weir height (m): ", 0)
            width = get_float_input("Enter weir width (m): ", 0)
            head = get_float_input("Enter head above crest (m): ", 0)
            
            weir_types = {'1': 'rectangular', '2': 'v-notch'}
            print("\nWeir Types:")
            for key, value in weir_types.items():
                print(f"{key}: {value}")
            weir_choice = input("Select weir type: ")
            
            results = fluid_mechanics.weir_flow(height, width, head, weir_types.get(weir_choice, 'rectangular'))
            print("\nResults:")
            print(f"Flow Rate: {results['flow_rate']:.3f} m³/s")
            print(f"Discharge Coefficient: {results['discharge_coefficient']:.3f}")
            
        elif choice == '8':
            wavelength = get_float_input("Enter wavelength (m): ", 0)
            depth = get_float_input("Enter water depth (m): ", 0)
            
            results = fluid_mechanics.wave_properties(wavelength, depth)
            print("\nResults:")
            print(f"Wave Speed: {results['wave_speed']:.2f} m/s")
            print(f"Group Velocity: {results['group_velocity']:.2f} m/s")
            print(f"Period: {results['period']:.2f} s")
            print(f"Frequency: {results['frequency']:.2f} Hz")
        
        input("\nPress Enter to continue...")
        clear_screen()

def main():
    """Main program loop"""
    options = {
        '1': 'Kinematics',
        '2': 'Stress Analysis',
        '3': 'Fluid Mechanics',
        '4': 'Thermodynamics',
        'Q': 'Quit'
    }
    
    calculators = {
        '1': kinematics_calculator,
        '2': stress_analysis_calculator,
        '3': fluid_mechanics_calculator,
        '4': None  # Thermodynamics calculator to be implemented
    }
    
    while True:
        clear_screen()
        print("Welcome to MechSolver!")
        print("=" * 50)
        
        choice = get_choice(options, "Select calculation type: ")
        if choice == 'Q':
            print("\nThank you for using MechSolver!")
            sys.exit()
            
        calculator = calculators.get(choice)
        if calculator:
            clear_screen()
            calculator()
        else:
            print("\nThis feature is not yet implemented.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
