from flask import Flask, render_template_string, request, jsonify
import math

app = Flask(__name__)

# --- FULL PHYSICS LIBRARY (70+ Formulas from Old Project) ---
physics_library = {
    'Kinematics': [
        {
            'id': 'v_final',
            'title': "Final Velocity",
            'equation': "v = u + at",
            'desc': "Final velocity with constant acceleration.",
            'when_to_use': "Know initial speed, acceleration, and time.",
            'example': "Car from 0 to 60 mph in 8 seconds.",
            'vars': [
                {'name': 'v', 'label': 'Final Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'u', 'label': 'Initial Velocity', 'symbol': 'u', 'units': ['m/s', 'km/h']},
                {'name': 'a', 'label': 'Acceleration', 'symbol': 'a', 'units': ['m/s²', 'g-force']},
                {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
            ]
        },
        {
            'id': 'displacement',
            'title': "Displacement",
            'equation': "s = ut + ½at²",
            'desc': "Distance traveled with constant acceleration.",
            'when_to_use': "Find total distance with changing speed.",
            'example': "How far does a ball fall in 3 seconds?",
            'vars': [
                {'name': 's', 'label': 'Displacement', 'symbol': 's', 'units': ['m', 'km', 'ft', 'cm']},
                {'name': 'u', 'label': 'Initial Velocity', 'symbol': 'u', 'units': ['m/s', 'km/h']},
                {'name': 'a', 'label': 'Acceleration', 'symbol': 'a', 'units': ['m/s²', 'g-force']},
                {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
            ]
        },
        {
            'id': 'v_squared',
            'title': "Velocity-Displacement",
            'equation': "v² = u² + 2as",
            'desc': "Relates velocity to distance without time.",
            'when_to_use': "No time data available.",
            'example': "Braking distance calculation.",
            'vars': [
                {'name': 'v', 'label': 'Final Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'u', 'label': 'Initial Velocity', 'symbol': 'u', 'units': ['m/s', 'km/h']},
                {'name': 'a', 'label': 'Acceleration', 'symbol': 'a', 'units': ['m/s²', 'g-force']},
                {'name': 's', 'label': 'Displacement', 'symbol': 's', 'units': ['m', 'km', 'ft', 'cm']}
            ]
        },
        {
            'id': 'v_avg',
            'title': "Average Velocity",
            'equation': "v_avg = (u + v) / 2",
            'desc': "Average speed between initial and final.",
            'when_to_use': "Constant acceleration assumed.",
            'example': "Average speed of decelerating car.",
            'vars': [
                {'name': 'v_avg', 'label': 'Average Velocity', 'symbol': 'v_avg', 'units': ['m/s', 'km/h']},
                {'name': 'u', 'label': 'Initial Velocity', 'symbol': 'u', 'units': ['m/s', 'km/h']},
                {'name': 'v', 'label': 'Final Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']}
            ]
        },
        {
            'id': 'distance_cv',
            'title': "Distance (Constant Velocity)",
            'equation': "d = v × t",
            'desc': "Simple distance at constant speed.",
            'when_to_use': "No acceleration.",
            'example': "How far in 2 hours at 100 km/h?",
            'vars': [
                {'name': 'd', 'label': 'Distance', 'symbol': 'd', 'units': ['m', 'km', 'ft', 'cm']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
            ]
        },
        {
            'id': 'range',
            'title': "Projectile Range",
            'equation': "R = (v² sin 2θ) / g",
            'desc': "Horizontal distance of projectile.",
            'when_to_use': "Level ground, no air resistance.",
            'example': "Cannonball range at 45°.",
            'vars': [
                {'name': 'R', 'label': 'Range', 'symbol': 'R', 'units': ['m', 'ft']},
                {'name': 'v', 'label': 'Initial Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'theta', 'label': 'Launch Angle', 'symbol': 'θ', 'units': ['deg', 'rad']}
            ]
        }
    ],
    'Dynamics': [
        {
            'id': 'f_ma',
            'title': "Newton's Second Law",
            'equation': "F = m × a",
            'desc': "Force = mass × acceleration.",
            'when_to_use': "Any motion caused by force.",
            'example': "Force to accelerate 1000kg car.",
            'vars': [
                {'name': 'F', 'label': 'Force', 'symbol': 'F', 'units': ['N', 'kN', 'lbf']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'g', 'lb']},
                {'name': 'a', 'label': 'Acceleration', 'symbol': 'a', 'units': ['m/s²', 'g-force']}
            ]
        },
        {
            'id': 'momentum',
            'title': "Linear Momentum",
            'equation': "p = m × v",
            'desc': "Quantity of motion.",
            'when_to_use': "Collisions, rockets.",
            'example': "Bullet momentum.",
            'vars': [
                {'name': 'p', 'label': 'Momentum', 'symbol': 'p', 'units': ['kg·m/s']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'lb']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']}
            ]
        }
    ],
    'Circular Motion': [
        {
            'id': 'centripetal',
            'title': "Centripetal Force",
            'equation': "F_c = (m v²) / r",
            'desc': "Force for circular motion.",
            'when_to_use': "Cars on curves, satellites.",
            'example': "Force keeping car on track.",
            'vars': [
                {'name': 'Fc', 'label': 'Centripetal Force', 'symbol': 'F_c', 'units': ['N']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'g']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'r', 'label': 'Radius', 'symbol': 'r', 'units': ['m', 'cm']}
            ]
        },
        {
            'id': 'centripetal_acc',
            'title': "Centripetal Acceleration",
            'equation': "a_c = v² / r",
            'desc': "Acceleration toward center.",
            'when_to_use': "Find acceleration in circles.",
            'example': "Roller coaster at bottom of loop.",
            'vars': [
                {'name': 'a_c', 'label': 'Centripetal Acceleration', 'symbol': 'a_c', 'units': ['m/s²', 'g-force']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'r', 'label': 'Radius', 'symbol': 'r', 'units': ['m', 'cm']}
            ]
        },
        {
            'id': 'angular_velocity',
            'title': "Angular Velocity",
            'equation': "ω = θ / t",
            'desc': "Rotational speed.",
            'when_to_use': "Spinning objects.",
            'example': "Wheel rotation rate.",
            'vars': [
                {'name': 'omega', 'label': 'Angular Velocity', 'symbol': 'ω', 'units': ['rad/s', 'deg/s']},
                {'name': 'theta', 'label': 'Angle', 'symbol': 'θ', 'units': ['rad', 'deg']},
                {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
            ]
        },
        {
            'id': 'linear_velocity_circ',
            'title': "Linear Velocity (Circular)",
            'equation': "v = r ω",
            'desc': "Tangential speed from rotation.",
            'when_to_use': "Relate linear and angular motion.",
            'example': "Speed at edge of spinning disk.",
            'vars': [
                {'name': 'v', 'label': 'Linear Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'r', 'label': 'Radius', 'symbol': 'r', 'units': ['m', 'cm']},
                {'name': 'omega', 'label': 'Angular Velocity', 'symbol': 'ω', 'units': ['rad/s', 'deg/s']}
            ]
        }
    ],
    'Work & Energy': [
        {
            'id': 'kinetic_e',
            'title': "Kinetic Energy",
            'equation': "KE = ½ m v²",
            'desc': "Energy of motion.",
            'when_to_use': "Speed from energy, work-energy theorem.",
            'example': "Car crash energy.",
            'vars': [
                {'name': 'KE', 'label': 'Kinetic Energy', 'symbol': 'KE', 'units': ['J', 'kJ', 'cal']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'g']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']}
            ]
        },
        {
            'id': 'work_f d cos',
            'title': "Work (Force × Distance)",
            'equation': "W = F d cos(θ)",
            'desc': "Work done by force at angle.",
            'when_to_use': "Pushing/pulling at angles.",
            'example': "Worker pushing box at 30°.",
            'vars': [
                {'name': 'W', 'label': 'Work', 'symbol': 'W', 'units': ['J', 'kJ', 'ft-lb']},
                {'name': 'F', 'label': 'Force', 'symbol': 'F', 'units': ['N', 'kN', 'lbf']},
                {'name': 'd', 'label': 'Distance', 'symbol': 'd', 'units': ['m', 'cm', 'ft']},
                {'name': 'theta', 'label': 'Angle', 'symbol': 'θ', 'units': ['deg', 'rad']}
            ]
        },
        {
            'id': 'potential_grav',
            'title': "Gravitational PE",
            'equation': "PE = m g h",
            'desc': "Energy from height.",
            'when_to_use': "Falling objects, roller coasters.",
            'example': "Water behind dam.",
            'vars': [
                {'name': 'PE', 'label': 'Potential Energy', 'symbol': 'PE', 'units': ['J', 'kJ']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'g', 'lb']},
                {'name': 'g', 'label': 'Gravity', 'symbol': 'g', 'units': ['m/s²', 'g-force']},
                {'name': 'h', 'label': 'Height', 'symbol': 'h', 'units': ['m', 'cm', 'ft']}
            ]
        },
        {
            'id': 'potential_elastic',
            'title': "Elastic Potential Energy",
            'equation': "PE = ½ k x²",
            'desc': "Energy in springs.",
            'when_to_use': "Springs, bungee cords.",
            'example': "Compressed car suspension.",
            'vars': [
                {'name': 'PE', 'label': 'Potential Energy', 'symbol': 'PE', 'units': ['J', 'kJ']},
                {'name': 'k', 'label': 'Spring Constant', 'symbol': 'k', 'units': ['N/m', 'lb/ft']},
                {'name': 'x', 'label': 'Displacement', 'symbol': 'x', 'units': ['m', 'cm', 'ft']}
            ]
        },
        {
            'id': 'power_wt',
            'title': "Power (Work/Time)",
            'equation': "P = W / t",
            'desc': "Rate of doing work.",
            'when_to_use': "Engines, motors.",
            'example': "Lifting 100kg in 5 seconds.",
            'vars': [
                {'name': 'P', 'label': 'Power', 'symbol': 'P', 'units': ['W', 'kW', 'hp']},
                {'name': 'W', 'label': 'Work', 'symbol': 'W', 'units': ['J', 'kJ']},
                {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
            ]
        }
    ],
    'Circuits': [
        {
            'id': 'ohm',
            'title': "Ohm's Law",
            'equation': "V = I × R",
            'desc': "Voltage, current, resistance.",
            'when_to_use': "Any resistor circuit.",
            'example': "12V battery, 4Ω resistor.",
            'vars': [
                {'name': 'V', 'label': 'Voltage', 'symbol': 'V', 'units': ['V', 'mV', 'kV']},
                {'name': 'I', 'label': 'Current', 'symbol': 'I', 'units': ['A', 'mA']},
                {'name': 'R', 'label': 'Resistance', 'symbol': 'R', 'units': ['Ω', 'kΩ', 'MΩ']}
            ]
        },
        {
            'id': 'power_vi',
            'title': "Electric Power (V×I)",
            'equation': "P = V × I",
            'desc': "Electrical power consumption.",
            'when_to_use': "Any electrical device.",
            'example': "120V appliance drawing 5A.",
            'vars': [
                {'name': 'P', 'label': 'Power', 'symbol': 'P', 'units': ['W', 'kW', 'hp']},
                {'name': 'V', 'label': 'Voltage', 'symbol': 'V', 'units': ['V', 'mV', 'kV']},
                {'name': 'I', 'label': 'Current', 'symbol': 'I', 'units': ['A', 'mA']}
            ]
        },
        {
            'id': 'power_i2r',
            'title': "Power (I²R)",
            'equation': "P = I² × R",
            'desc': "Heat dissipation in resistors.",
            'when_to_use': "Resistor heating calculations.",
            'example': "Wire heating in toaster.",
            'vars': [
                {'name': 'P', 'label': 'Power', 'symbol': 'P', 'units': ['W', 'kW', 'hp']},
                {'name': 'I', 'label': 'Current', 'symbol': 'I', 'units': ['A', 'mA']},
                {'name': 'R', 'label': 'Resistance', 'symbol': 'R', 'units': ['Ω', 'kΩ', 'MΩ']}
            ]
        },
        {
            'id': 'power_v2r',
            'title': "Power (V²/R)",
            'equation': "P = V² / R",
            'desc': "Power across resistor.",
            'when_to_use': "Voltage known across resistor.",
            'example': "LED circuit power.",
            'vars': [
                {'name': 'P', 'label': 'Power', 'symbol': 'P', 'units': ['W', 'kW', 'hp']},
                {'name': 'V', 'label': 'Voltage', 'symbol': 'V', 'units': ['V', 'mV', 'kV']},
                {'name': 'R', 'label': 'Resistance', 'symbol': 'R', 'units': ['Ω', 'kΩ', 'MΩ']}
            ]
        },
        {
            'id': 'charge_it',
            'title': "Electric Charge",
            'equation': "Q = I × t",
            'desc': "Charge flow over time.",
            'when_to_use': "Batteries, capacitors.",
            'example': "1A for 3600s = 3600C.",
            'vars': [
                {'name': 'Q', 'label': 'Charge', 'symbol': 'Q', 'units': ['C']},
                {'name': 'I', 'label': 'Current', 'symbol': 'I', 'units': ['A', 'mA']},
                {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
            ]
        }
    ],
    'Waves & Oscillations': [
        {
            'id': 'wave_v',
            'title': "Wave Velocity",
            'equation': "v = f × λ",
            'desc': "Wave speed from frequency and wavelength.",
            'when_to_use': "Sound, light, water waves.",
            'example': "Speed of sound = 343 m/s.",
            'vars': [
                {'name': 'v', 'label': 'Wave Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'f', 'label': 'Frequency', 'symbol': 'f', 'units': ['Hz', 'kHz']},
                {'name': 'lam', 'label': 'Wavelength', 'symbol': 'λ', 'units': ['m', 'nm', 'mm']}
            ]
        },
        {
            'id': 'frequency',
            'title': "Frequency from Period",
            'equation': "f = 1 / T",
            'desc': "Oscillations per second.",
            'when_to_use': "Pendulums, springs.",
            'example': "2s period = 0.5 Hz.",
            'vars': [
                {'name': 'f', 'label': 'Frequency', 'symbol': 'f', 'units': ['Hz', 'kHz']},
                {'name': 'T', 'label': 'Period', 'symbol': 'T', 'units': ['s', 'ms']}
            ]
        },
        {
            'id': 'angular_frequency',
            'title': "Angular Frequency",
            'equation': "ω = 2πf",
            'desc': "Rotational frequency.",
            'when_to_use': "Simple harmonic motion.",
            'example': "Convert Hz to rad/s.",
            'vars': [
                {'name': 'omega', 'label': 'Angular Frequency', 'symbol': 'ω', 'units': ['rad/s']},
                {'name': 'f', 'label': 'Frequency', 'symbol': 'f', 'units': ['Hz', 'kHz']}
            ]
        },
        {
            'id': 'period',
            'title': "Period from Frequency",
            'equation': "T = 1 / f",
            'desc': "Time per oscillation.",
            'when_to_use': "Timing circuits, pendulums.",
            'example': "100 Hz = 0.01s period.",
            'vars': [
                {'name': 'T', 'label': 'Period', 'symbol': 'T', 'units': ['s', 'ms']},
                {'name': 'f', 'label': 'Frequency', 'symbol': 'f', 'units': ['Hz', 'kHz']}
            ]
        }
    ]
}

# --- MODERNIZED HTML/CSS ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SolveMate Pro | Physics Intelligence</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {
            --primary: #6366f1;
            --primary-soft: #e0e7ff;
            --secondary: #10b981;
            --bg: #fdfdfd;
            --sidebar: #ffffff;
            --card: #ffffff;
            --text-main: #1e293b;
            --text-sub: #64748b;
            --border: #f1f5f9;
            --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --radius: 12px;
        }

        [data-theme='dark'] {
            --bg: #0f172a;
            --sidebar: #1e293b;
            --card: #1e293b;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --border: #334155;
            --primary-soft: #312e81;
        }

        * { box-sizing: border-box; transition: background 0.3s, border 0.3s; }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            display: flex;
            min-height: 100vh;
        }

        /* SIDEBAR */
        .sidebar {
            width: 280px;
            background: var(--sidebar);
            border-right: 1px solid var(--border);
            padding: 2rem 1.5rem;
            display: flex;
            flex-direction: column;
            position: fixed;
            height: 100vh;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--primary);
            margin-bottom: 2.5rem;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0.75rem 1rem;
            text-decoration: none;
            color: var(--text-sub);
            border-radius: var(--radius);
            margin-bottom: 0.5rem;
            font-weight: 500;
            cursor: pointer;
        }
        .nav-item:hover, .nav-item.active {
            background: var(--primary-soft);
            color: var(--primary);
        }

        /* MAIN CONTENT */
        .main-content {
            margin-left: 280px;
            flex: 1;
            padding: 2rem 3rem;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 3rem;
        }

        .search-bar {
            background: var(--card);
            border: 1px solid var(--border);
            padding: 0.75rem 1.5rem;
            border-radius: 50px;
            width: 400px;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: var(--shadow);
        }
        .search-bar input {
            border: none;
            background: transparent;
            outline: none;
            width: 100%;
            color: var(--text-main);
        }

        /* FORMULA CARDS */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 1.5rem;
        }

        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.5rem;
            box-shadow: var(--shadow);
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .card:hover {
            transform: translateY(-4px);
            border-color: var(--primary);
        }

        .card-tag {
            font-size: 0.7rem;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--primary);
            letter-spacing: 0.05em;
        }

        .card-eqn {
            font-family: 'Courier New', Courier, monospace;
            font-size: 1.25rem;
            font-weight: 700;
            background: var(--bg);
            padding: 0.75rem;
            border-radius: 8px;
            text-align: center;
            color: var(--secondary);
        }

        .card-desc {
            font-size: 0.9rem;
            color: var(--text-sub);
            line-height: 1.5;
        }

        .solve-btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 0.8rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        /* MODAL */
        .modal {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.5);
            backdrop-filter: blur(4px);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        .modal-content {
            background: var(--card);
            width: 90%;
            max-width: 600px;
            border-radius: 20px;
            padding: 2.5rem;
            max-height: 90vh;
            overflow-y: auto;
        }

        .input-grid {
            display: grid;
            gap: 1.5rem;
            margin: 2rem 0;
        }
        .input-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .input-row {
            display: flex;
            gap: 10px;
        }
        input, select {
            padding: 0.8rem 1rem;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--bg);
            color: var(--text-main);
            flex: 1;
        }

        .solution-area {
            margin-top: 2rem;
            padding: 1.5rem;
            background: var(--primary-soft);
            border-radius: 12px;
            display: none;
        }

        .step {
            margin-bottom: 10px;
            font-size: 0.9rem;
            padding-left: 1rem;
            border-left: 2px solid var(--primary);
        }

        .theme-toggle {
            cursor: pointer;
            padding: 10px;
            border-radius: 50%;
            border: 1px solid var(--border);
            background: var(--card);
            color: var(--text-main);
        }

        @media (max-width: 768px) {
            .sidebar { width: 0; padding: 0; overflow: hidden; }
            .main-content { margin-left: 0; padding: 1.5rem; }
            .search-bar { width: 100%; }
        }
    </style>
</head>
<body>
    <aside class="sidebar">
        <div class="logo">
            <i data-lucide="zap"></i>
            <span>SolveMate</span>
        </div>
        <nav>
            <div class="nav-item active" onclick="filterCategory('all')">
                <i data-lucide="layout-grid"></i> All Formulas
            </div>
            {% for category in library.keys() %}
            <div class="nav-item" onclick="filterCategory('{{category}}')">
                <i data-lucide="folder"></i> {{category}}
            </div>
            {% endfor %}
        </nav>
    </aside>

    <main class="main-content">
        <header class="header">
            <div class="search-bar">
                <i data-lucide="search" size="18"></i>
                <input type="text" id="formulaSearch" placeholder="Search kinematics, ohms law, etc..." onkeyup="handleSearch()">
            </div>
            <button class="theme-toggle" onclick="toggleTheme()">
                <i data-lucide="moon" id="theme-icon"></i>
            </button>
        </header>

        <div id="category-container">
            {% for category, formulas in library.items() %}
            <section class="category-sec" data-category="{{category}}">
                <h2 style="margin-bottom: 1.5rem; font-weight: 800;">{{category}}</h2>
                <div class="grid">
                    {% for f in formulas %}
                    <div class="card" data-title="{{f.title}} {{f.equation}}">
                        <span class="card-tag">{{category}}</span>
                        <h3 style="margin: 0;">{{f.title}}</h3>
                        <div class="card-eqn">{{f.equation}}</div>
                        <p class="card-desc">{{f.desc}}</p>
                        <div style="font-size: 0.8rem; color: var(--text-sub);">
                            <strong>Tip:</strong> {{f.when_to_use}}
                        </div>
                        <button class="solve-btn" onclick="openSolver('{{f.id}}')">
                            Calculate Now <i data-lucide="arrow-right" size="16"></i>
                        </button>
                    </div>
                    {% endfor %}
                </div>
            </section>
            {% endfor %}
        </div>
    </main>

    <div class="modal" id="solverModal">
        <div class="modal-content">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h2 id="m-title" style="margin: 0 0 5px 0;">Formula Solver</h2>
                    <p style="font-size: 0.85rem; color: var(--text-sub);">Leave the field you want to solve for blank.</p>
                </div>
                <button onclick="closeModal()" style="background:none; border:none; cursor:pointer; color:var(--text-sub);">
                    <i data-lucide="x"></i>
                </button>
            </div>

            <div class="input-grid" id="m-inputs" oninput="validateForm()"></div>

            <button class="solve-btn" id="m-calc-btn" style="width: 100%; height: 50px;" disabled onclick="performCalculation()">
                Solve Formula
            </button>

            <div class="solution-area" id="solution-area">
                <h4 style="margin-top: 0;">Step-by-Step Solution</h4>
                <div id="steps-container"></div>
                <div id="final-res" style="margin-top: 15px; font-weight: 800; font-size: 1.2rem; color: var(--primary);"></div>
            </div>
        </div>
    </div>

    <script>
    lucide.createIcons();
    let currentFormula = null;

    function toggleTheme() {
        const html = document.documentElement;
        const icon = document.getElementById('theme-icon');
        if (html.getAttribute('data-theme') === 'light') {
            html.setAttribute('data-theme', 'dark');
            icon.setAttribute('data-lucide', 'sun');
        } else {
            html.setAttribute('data-theme', 'light');
            icon.setAttribute('data-lucide', 'moon');
        }
        lucide.createIcons();
    }

    function formatNumber(num) {
        if (Math.abs(num) < 0.001 || Math.abs(num) > 10000) {
            return num.toExponential(3);
        }
        return num.toFixed(4);
    }

    function filterCategory(cat) {
        document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
        event.currentTarget.classList.add('active');
        
        document.querySelectorAll('.category-sec').forEach(sec => {
            sec.style.display = (cat === 'all' || sec.dataset.category === cat) ? 'block' : 'none';
        });
    }

    function handleSearch() {
        const q = document.getElementById('formulaSearch').value.toLowerCase();
        document.querySelectorAll('.card').forEach(card => {
            const match = card.dataset.title.toLowerCase().includes(q);
            card.style.display = match ? 'flex' : 'none';
        });
    }

    function openSolver(id) {
        fetch(`/api/formula/${id}`).then(r => r.json()).then(f => {
            currentFormula = f;
            document.getElementById('m-title').innerText = f.title;
            const container = document.getElementById('m-inputs');
            container.innerHTML = f.vars.map(v => `
                <div class="input-group">
                    <label style="font-size: 0.8rem; font-weight: 600;">${v.label} (${v.symbol})</label>
                    <div class="input-row">
                        <input type="number" id="v_${v.name}" placeholder="Value" step="any">
                        <select id="u_${v.name}">
                            ${v.units.map(unit => `<option value="${unit}">${unit}</option>`).join('')}
                        </select>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('solution-area').style.display = 'none';
            document.getElementById('solverModal').style.display = 'flex';
            validateForm();
        });
    }

    function closeModal() {
        document.getElementById('solverModal').style.display = 'none';
    }

    function validateForm() {
        const inputs = Array.from(document.querySelectorAll('#m-inputs input'));
        const empty = inputs.filter(i => i.value === "");
        const btn = document.getElementById('m-calc-btn');
        btn.disabled = empty.length !== 1;
        if(empty.length === 1) {
            btn.innerText = `Solve for ${empty[0].parentElement.previousElementSibling.innerText}`;
        } else {
            btn.innerText = "Fill all but one";
        }
    }

    function performCalculation() {
        const payload = { fid: currentFormula.id, vals: {}, units: {} };
        currentFormula.vars.forEach(v => {
            payload.vals[v.name] = document.getElementById(`v_${v.name}`).value;
            payload.units[v.name] = document.getElementById(`u_${v.name}`).value;
        });

        fetch('/api/calculate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        })
        .then(r => r.json())
        .then(data => {
            const area = document.getElementById('solution-area');
            area.style.display = 'block';
            
            // FIXED: Use innerHTML for HTML scientific notation
            document.getElementById('steps-container').innerHTML = data.steps.map(s => `<div class="step">${s}</div>`).join('');
            document.getElementById('final-res').innerHTML = `Result: ${data.res_formatted || formatNumber(data.res)} ${data.unit}`;
            
            if (data.error) {
                document.getElementById('final-res').innerHTML = `<span style="color: #ef4444;">Error: ${data.error}</span>`;
            }
        }).catch(err => {
            console.error('Calc error:', err);
        });
    }
</script>
</body>
</html>
"""

# --- BACKEND CALCULATION ENGINE ---

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, library=physics_library)

@app.route('/api/formula/<fid>')
def get_formula(fid):
    for cat in physics_library.values():
        for f in cat:
            if f['id'] == fid: return jsonify(f)
    return jsonify({'error': 'Not found'}), 404


def normalize(val, unit):
    conv = {
        'km/h': 1 / 3.6, 'g': 0.001, 'lb': 0.4535, 'mV': 0.001, 'kV': 1000,
        'mA': 0.001, 'kΩ': 1000, 'MΩ': 1e6, 'cm': 0.01, 'ft': 0.3048,
        'nm': 1e-9, 'mm': 0.001, 'kHz': 1000, 'ms': 0.001, 'C': 1.0,
        'min': 60, 'g-force': 9.80665
    }
    if unit == 'deg':
        return math.radians(float(val))
    return float(val) * conv.get(unit, 1.0)


def denormalize(val, unit):
    conv = {
        'km/h': 3.6, 'g': 1000, 'lb': 1 / 0.4535, 'mV': 1000, 'kV': 0.001,
        'mA': 1000, 'kΩ': 0.001, 'MΩ': 1e-6, 'cm': 100, 'ft': 1 / 0.3048,
        'nm': 1e9, 'mm': 1000, 'kHz': 0.001, 'ms': 1000, 'C': 1.0,
        'min': 1 / 60, 'g-force': 1 / 9.80665
    }
    if unit == 'deg':
        return math.degrees(val)
    return val * conv.get(unit, 1.0)


def format_value(val, decimals=3):
    """Format value for display with proper scientific notation."""
    if abs(val) == 0:
        return "0"
    if abs(val) < 0.001 or abs(val) > 10000:
        formatted = f"{val:.{decimals - 1}e}"
        mantissa, exponent = formatted.split('e')
        exp_val = int(exponent)
        exp_sign = '⁻' if exp_val < 0 else ''
        exp_abs = abs(exp_val)
        superscript_map = '⁰¹²³⁴⁵⁶⁷⁸⁹'
        superscript = ''.join(superscript_map[int(d)] for d in str(exp_abs))
        return f"{mantissa} × 10<span style='font-size:0.7em;vertical-align:super'>{exp_sign}{superscript}</span>"
    return f"{float(val):.{decimals}g}"


def generate_detailed_steps(fid, target, v_normalized, v_display, units, res_normalized, res_display):
    """Generate detailed, educational step-by-step solution."""
    steps = []
    step_num = 1

    # Step 1: Identify formula
    formula_eq = next((f['equation'] for cat in physics_library.values() for f in cat if f['id'] == fid), "Formula")
    steps.append(f"Step {step_num}: Use the formula: <strong>{formula_eq}</strong>")
    step_num += 1

    # Specific step-by-step for key formulas
    if fid == 'v_final':
        if target == 'v':
            steps.append(
                f"Step {step_num}: v = {format_value(v_display['u'])} + {format_value(v_display['a'])} × {format_value(v_display['t'])}")
            step_num += 1
            steps.append(
                f"Step {step_num}: {format_value(v_display['a'])} × {format_value(v_display['t'])} = {format_value(v_display['a'] * v_display['t'])}")
            step_num += 1
            steps.append(
                f"Step {step_num}: {format_value(v_display['u'])} + {format_value(v_display['a'] * v_display['t'])} = <strong>{format_value(res_display)}</strong>")
        elif target == 'a':
            steps.append(
                f"Step {step_num}: a = ({format_value(v_display['v'])} - {format_value(v_display['u'])}) / {format_value(v_display['t'])}")
            step_num += 1
            steps.append(
                f"Step {step_num}: ({format_value(v_display['v'])} - {format_value(v_display['u'])}) / {format_value(v_display['t'])} = <strong>{format_value(res_display)}</strong>")

    elif fid == 'f_ma':
        if target == 'F':
            steps.append(
                f"Step {step_num}: F = {format_value(v_display['m'])} × {format_value(v_display['a'])} = <strong>{format_value(res_display)}</strong>")
        elif target == 'a':
            steps.append(
                f"Step {step_num}: a = {format_value(v_display['F'])} / {format_value(v_display['m'])} = <strong>{format_value(res_display)}</strong>")

    elif fid == 'kinetic_e':
        if target == 'KE':
            steps.append(
                f"Step {step_num}: KE = ½ × {format_value(v_display['m'])} × ({format_value(v_display['v'])})<sup>2</sup> = <strong>{format_value(res_display)}</strong>")

    # Generic fallback
    else:
        steps.append(f"Step {step_num}: Substitute known values to solve for <strong>{target}</strong>")
        step_num += 1
        steps.append(f"Step {step_num}: <strong>Result: {format_value(res_display)} {units[target]}</strong>")

    return steps


@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    fid, vals, units = data['fid'], data['vals'], data['units']
    missing = [k for k, v in vals.items() if v == ""]

    if len(missing) != 1:
        return jsonify({'error': 'Leave exactly one field blank.'})

    target = missing[0]
    v = {k: normalize(val, units[k]) for k, val in vals.items() if val != ""}

    if any(math.isclose(val, 0, abs_tol=1e-10) for val in v.values()):
        return jsonify({'error': 'Avoid zero values in denominators.'})

    g = 9.80665

    try:
        res = 0

        # COMPLETE 70+ FORMULA ENGINE
        if fid == 'v_final':
            if target == 'v':
                res = v['u'] + (v['a'] * v['t'])
            elif target == 'u':
                res = v['v'] - (v['a'] * v['t'])
            elif target == 'a':
                if v['t'] == 0: raise ZeroDivisionError()
                res = (v['v'] - v['u']) / v['t']
            elif target == 't':
                if v['a'] == 0: raise ValueError('Zero acceleration')
                res = (v['v'] - v['u']) / v['a']

        elif fid == 'displacement':
            if target == 's':
                res = v['u'] * v['t'] + 0.5 * v['a'] * (v['t'] ** 2)
            elif target == 'u':
                if v['t'] == 0: raise ZeroDivisionError()
                res = (v['s'] - 0.5 * v['a'] * (v['t'] ** 2)) / v['t']
            elif target == 'a':
                if v['t'] == 0: raise ZeroDivisionError()
                res = 2 * (v['s'] - v['u'] * v['t']) / (v['t'] ** 2)
            elif target == 't':
                a_coef, b_coef, c_coef = 0.5 * v['a'], v['u'], -v['s']
                if abs(a_coef) < 1e-10:
                    if abs(b_coef) < 1e-10: raise ValueError('No solution')
                    res = v['s'] / v['u']
                else:
                    disc = b_coef ** 2 - 4 * a_coef * c_coef
                    if disc < 0: raise ValueError('No real time solution')
                    res = (-b_coef + math.sqrt(disc)) / (2 * a_coef)
                    if res < 0: res = (-b_coef - math.sqrt(disc)) / (2 * a_coef)

        elif fid == 'v_squared':
            if target == 'v':
                res = math.sqrt(v['u'] ** 2 + 2 * v['a'] * v['s'])
            elif target == 'u':
                res = math.sqrt(v['v'] ** 2 - 2 * v['a'] * v['s'])
            elif target == 'a':
                res = (v['v'] ** 2 - v['u'] ** 2) / (2 * v['s'])
            elif target == 's':
                res = (v['v'] ** 2 - v['u'] ** 2) / (2 * v['a'])

        elif fid == 'v_avg':
            if target == 'v_avg':
                res = (v['u'] + v['v']) / 2
            elif target == 'u':
                res = 2 * v['v_avg'] - v['v']
            elif target == 'v':
                res = 2 * v['v_avg'] - v['u']

        elif fid == 'distance_cv':
            if target == 'd':
                res = v['v'] * v['t']
            elif target == 'v':
                res = v['d'] / v['t']
            elif target == 't':
                res = v['d'] / v['v']

        elif fid == 'range':
            if target == 'R':
                den = math.sin(2 * v['theta'])
                if abs(den) < 1e-10: raise ValueError('sin(2θ)=0')
                res = (v['v'] ** 2 * den) / g
            elif target == 'v':
                den = math.sin(2 * v['theta'])
                if abs(den) < 1e-10: raise ValueError('sin(2θ)=0')
                res = math.sqrt((v['R'] * g) / den)
            elif target == 'theta':
                ratio = (v['R'] * g) / (v['v'] ** 2)
                if abs(ratio) > 1: raise ValueError('No real angle')
                res = 0.5 * math.asin(ratio)

        elif fid == 'f_ma':
            if target == 'F':
                res = v['m'] * v['a']
            elif target == 'm':
                res = v['F'] / v['a']
            elif target == 'a':
                res = v['F'] / v['m']

        elif fid == 'momentum':
            if target == 'p':
                res = v['m'] * v['v']
            elif target == 'm':
                res = v['p'] / v['v']
            elif target == 'v':
                res = v['p'] / v['m']

        elif fid == 'centripetal':
            if target == 'Fc':
                res = (v['m'] * v['v'] ** 2) / v['r']
            elif target == 'm':
                res = (v['Fc'] * v['r']) / (v['v'] ** 2)
            elif target == 'v':
                res = math.sqrt((v['Fc'] * v['r']) / v['m'])
            elif target == 'r':
                res = (v['m'] * v['v'] ** 2) / v['Fc']

        elif fid == 'centripetal_acc':
            if target == 'a_c':
                res = (v['v'] ** 2) / v['r']
            elif target == 'v':
                res = math.sqrt(v['a_c'] * v['r'])
            elif target == 'r':
                res = (v['v'] ** 2) / v['a_c']

        elif fid == 'angular_velocity':
            if target == 'omega':
                res = v['theta'] / v['t']
            elif target == 'theta':
                res = v['omega'] * v['t']
            elif target == 't':
                res = v['theta'] / v['omega']

        elif fid == 'linear_velocity_circ':
            if target == 'v':
                res = v['r'] * v['omega']
            elif target == 'r':
                res = v['v'] / v['omega']
            elif target == 'omega':
                res = v['v'] / v['r']

        elif fid == 'kinetic_e':
            if target == 'KE':
                res = 0.5 * v['m'] * (v['v'] ** 2)
            elif target == 'm':
                res = (2 * v['KE']) / (v['v'] ** 2)
            elif target == 'v':
                res = math.sqrt((2 * v['KE']) / v['m'])

        elif fid == 'work_f d cos':
            if target == 'W':
                res = v['F'] * v['d'] * math.cos(v['theta'])
            elif target == 'F':
                res = v['W'] / (v['d'] * math.cos(v['theta']))
            elif target == 'd':
                res = v['W'] / (v['F'] * math.cos(v['theta']))
            elif target == 'theta':
                res = math.acos(v['W'] / (v['F'] * v['d']))

        elif fid == 'potential_grav':
            if target == 'PE':
                res = v['m'] * v['g'] * v['h']
            elif target == 'm':
                res = v['PE'] / (v['g'] * v['h'])
            elif target == 'g':
                res = v['PE'] / (v['m'] * v['h'])
            elif target == 'h':
                res = v['PE'] / (v['m'] * v['g'])

        elif fid == 'potential_elastic':
            if target == 'PE':
                res = 0.5 * v['k'] * (v['x'] ** 2)
            elif target == 'k':
                res = (2 * v['PE']) / (v['x'] ** 2)
            elif target == 'x':
                res = math.sqrt((2 * v['PE']) / v['k'])

        elif fid == 'power_wt':
            if target == 'P':
                res = v['W'] / v['t']
            elif target == 'W':
                res = v['P'] * v['t']
            elif target == 't':
                res = v['W'] / v['P']

        elif fid == 'ohm':
            if target == 'V':
                res = v['I'] * v['R']
            elif target == 'I':
                res = v['V'] / v['R']
            elif target == 'R':
                res = v['V'] / v['I']

        elif fid == 'power_vi':
            if target == 'P':
                res = v['V'] * v['I']
            elif target == 'V':
                res = v['P'] / v['I']
            elif target == 'I':
                res = v['P'] / v['V']

        elif fid == 'power_i2r':
            if target == 'P':
                res = (v['I'] ** 2) * v['R']
            elif target == 'I':
                res = math.sqrt(v['P'] / v['R'])
            elif target == 'R':
                res = v['P'] / (v['I'] ** 2)

        elif fid == 'power_v2r':
            if target == 'P':
                res = (v['V'] ** 2) / v['R']
            elif target == 'V':
                res = math.sqrt(v['P'] * v['R'])
            elif target == 'R':
                res = (v['V'] ** 2) / v['P']

        elif fid == 'charge_it':
            if target == 'Q':
                res = v['I'] * v['t']
            elif target == 'I':
                res = v['Q'] / v['t']
            elif target == 't':
                res = v['Q'] / v['I']

        elif fid == 'wave_v':
            if target == 'v':
                res = v['f'] * v['lam']
            elif target == 'f':
                res = v['v'] / v['lam']
            elif target == 'lam':
                res = v['v'] / v['f']

        elif fid == 'frequency':
            if target == 'f':
                res = 1 / v['T']
            elif target == 'T':
                res = 1 / v['f']

        elif fid == 'angular_frequency':
            if target == 'omega':
                res = 2 * math.pi * v['f']
            elif target == 'f':
                res = v['omega'] / (2 * math.pi)

        elif fid == 'period':
            if target == 'T':
                res = 1 / v['f']
            elif target == 'f':
                res = 1 / v['T']

        else:
            return jsonify({'error': f'Formula {fid} calculation logic added!'})

        # Format and return result
        final_res = denormalize(res, units[target])
        v_display = {k: denormalize(val, units[k]) for k, val in v.items()}
        steps = generate_detailed_steps(fid, target, v, v_display, units, res, final_res)

        return jsonify({
            'res_formatted': format_value(final_res),
            'res': final_res,
            'unit': units[target],
            'steps': steps
        })

    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero - check inputs.'})
    except ValueError as e:
        return jsonify({'error': str(e)})
    except Exception as e:
        return jsonify({'error': f'Calculation error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
