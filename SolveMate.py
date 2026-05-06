from flask import Flask, render_template_string, request, jsonify
import math

app = Flask(__name__)

# --- STRUCTURED PHYSICS LIBRARY ---
physics_library = {
    'Motion (1D & 2D)': [
        {
            'id': 'v_final',
            'title': "Kinematics: Final Velocity",
            'equation': "v = u + at",
            'desc': "Calculates the final speed of an object moving with constant acceleration[cite: 2].",
            'vars': [
                {'name': 'v', 'label': 'Final Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'u', 'label': 'Initial Velocity', 'symbol': 'u', 'units': ['m/s', 'km/h']},
                {'name': 'a', 'label': 'Acceleration', 'symbol': 'a', 'units': ['m/s²', 'g-force']},
                {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
            ]
        },
{
    'id': 'displacement',
    'title': "Displacement (Kinematics)",
    'equation': "s = ut + ½at²",
    'desc': "Displacement of an object with constant acceleration[cite: 2].",
    'vars': [
        {'name': 's', 'label': 'Displacement', 'symbol': 's', 'units': ['m', 'cm', 'ft']},
        {'name': 'u', 'label': 'Initial Velocity', 'symbol': 'u', 'units': ['m/s', 'km/h']},
        {'name': 'a', 'label': 'Acceleration', 'symbol': 'a', 'units': ['m/s²', 'g-force']},
        {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
    ]
},
{
    'id': 'v_squared',
    'title': "Velocity-Displacement",
    'equation': "v² = u² + 2as",
    'desc': "Relates final velocity to initial velocity and displacement[cite: 2].",
    'vars': [
        {'name': 'v', 'label': 'Final Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
        {'name': 'u', 'label': 'Initial Velocity', 'symbol': 'u', 'units': ['m/s', 'km/h']},
        {'name': 'a', 'label': 'Acceleration', 'symbol': 'a', 'units': ['m/s²', 'g-force']},
        {'name': 's', 'label': 'Displacement', 'symbol': 's', 'units': ['m', 'cm', 'ft']}
    ]
},
{
    'id': 'v_avg',
    'title': "Average Velocity",
    'equation': "v_avg = (u + v) / 2",
    'desc': "Average velocity between initial and final velocities[cite: 2].",
    'vars': [
        {'name': 'v_avg', 'label': 'Average Velocity', 'symbol': 'v_avg', 'units': ['m/s', 'km/h']},
        {'name': 'u', 'label': 'Initial Velocity', 'symbol': 'u', 'units': ['m/s', 'km/h']},
        {'name': 'v', 'label': 'Final Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']}
    ]
},
{
    'id': 'distance_cv',
    'title': "Distance (Constant Velocity)",
    'equation': "d = v * t",
    'desc': "Distance traveled at constant velocity[cite: 2].",
    'vars': [
        {'name': 'd', 'label': 'Distance', 'symbol': 'd', 'units': ['m', 'cm', 'ft']},
        {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
        {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
    ]
},
        {
            'id': 'range',
            'title': "Projectile Range",
            'equation': "R = (v² sin 2θ) / g",
            'desc': "The horizontal distance traveled by a projectile on level ground[cite: 2].",
            'vars': [
                {'name': 'R', 'label': 'Range', 'symbol': 'R', 'units': ['m', 'ft']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'theta', 'label': 'Angle', 'symbol': 'θ', 'units': ['deg', 'rad']}
            ]
        }
    ],
    'Forces & Circular Motion': [
        {
            'id': 'f_ma',
            'title': "Newton’s Second Law",
            'equation': "F = m * a",
            'desc': "Net force equals mass times acceleration[cite: 2].",
            'vars': [
                {'name': 'F', 'label': 'Force', 'symbol': 'F', 'units': ['N', 'kN', 'lbf']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'g', 'lb']},
                {'name': 'a', 'label': 'Acceleration', 'symbol': 'a', 'units': ['m/s²', 'g-force']}
            ]
        },
        {
            'id': 'centripetal',
            'title': "Centripetal Force",
            'equation': "Fc = (m * v²) / r",
            'desc': "The inward force required to keep an object in circular motion[cite: 2].",
            'vars': [
                {'name': 'Fc', 'label': 'Centripetal Force', 'symbol': 'Fc', 'units': ['N']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'g']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'r', 'label': 'Radius', 'symbol': 'r', 'units': ['m', 'cm']}
            ]
        },
{
    'id': 'centripetal_acc',
    'title': "Centripetal Acceleration",
    'equation': "a_c = v² / r",
    'desc': "Acceleration toward center of circular path[cite: 2].",
    'vars': [
        {'name': 'a_c', 'label': 'Centripetal Acceleration', 'symbol': 'a_c', 'units': ['m/s²', 'g-force']},
        {'name': 'v', 'label': 'Tangential Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
        {'name': 'r', 'label': 'Radius', 'symbol': 'r', 'units': ['m', 'cm']}
    ]
},
{
    'id': 'angular_velocity',
    'title': "Angular Velocity",
    'equation': "ω = θ / t",
    'desc': "Rate of angular displacement[cite: 2].",
    'vars': [
        {'name': 'omega', 'label': 'Angular Velocity', 'symbol': 'ω', 'units': ['rad/s', 'deg/s']},
        {'name': 'theta', 'label': 'Angular Displacement', 'symbol': 'θ', 'units': ['rad', 'deg']},
        {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
    ]
},
{
    'id': 'linear_velocity_circ',
    'title': "Linear Velocity (Circular)",
    'equation': "v = r ω",
    'desc': "Tangential speed in circular motion[cite: 2].",
    'vars': [
        {'name': 'v', 'label': 'Linear Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
        {'name': 'r', 'label': 'Radius', 'symbol': 'r', 'units': ['m', 'cm']},
        {'name': 'omega', 'label': 'Angular Velocity', 'symbol': 'ω', 'units': ['rad/s', 'deg/s']}
    ]
}
    ],
    'Energy & Momentum': [
        {
            'id': 'kinetic_e',
            'title': "Kinetic Energy",
            'equation': "KE = ½ * m * v²",
            'desc': "The energy of an object due to its motion[cite: 2].",
            'vars': [
                {'name': 'KE', 'label': 'Kinetic Energy', 'symbol': 'KE', 'units': ['J', 'kJ', 'cal']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'g']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']}
            ]
        },
{
    'id': 'work_fdcos',
    'title': "Work (Force × Distance)",
    'equation': "W = F d cos(θ)",
    'desc': "Work done by a force over distance at an angle[cite: 2].",
    'vars': [
        {'name': 'W', 'label': 'Work', 'symbol': 'W', 'units': ['J', 'kJ', 'ft-lb']},
        {'name': 'F', 'label': 'Force', 'symbol': 'F', 'units': ['N', 'kN', 'lbf']},
        {'name': 'd', 'label': 'Distance', 'symbol': 'd', 'units': ['m', 'cm', 'ft']},
        {'name': 'theta', 'label': 'Angle', 'symbol': 'θ', 'units': ['deg', 'rad']}
    ]
},
{
    'id': 'potential_grav',
    'title': "Gravitational Potential Energy",
    'equation': "PE = m g h",
    'desc': "Potential energy due to height in gravitational field[cite: 2].",
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
    'desc': "Energy stored in a stretched/compressed spring[cite: 2].",
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
    'desc': "Rate of doing work or transferring energy[cite: 2].",
    'vars': [
        {'name': 'P', 'label': 'Power', 'symbol': 'P', 'units': ['W', 'kW', 'hp']},
        {'name': 'W', 'label': 'Work', 'symbol': 'W', 'units': ['J', 'kJ']},
        {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
    ]
},
        {
            'id': 'momentum',
            'title': "Linear Momentum",
            'equation': "p = m * v",
            'desc': "The product of an object's mass and its velocity[cite: 2].",
            'vars': [
                {'name': 'p', 'label': 'Momentum', 'symbol': 'p', 'units': ['kg·m/s']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'lb']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']}
            ]
        }
    ],
    'Electricity & Optics': [
        {
            'id': 'ohm',
            'title': "Ohm's Law",
            'equation': "V = I * R",
            'desc': "Fundamental relationship for electrical circuits[cite: 2].",
            'vars': [
                {'name': 'V', 'label': 'Voltage', 'symbol': 'V', 'units': ['V', 'mV', 'kV']},
                {'name': 'I', 'label': 'Current', 'symbol': 'I', 'units': ['A', 'mA']},
                {'name': 'R', 'label': 'Resistance', 'symbol': 'R', 'units': ['Ω', 'kΩ', 'MΩ']}
            ]
        },
{
    'id': 'power_vi',
    'title': "Electric Power (V×I)",
    'equation': "P = V * I",
    'desc': "Electrical power from voltage and current[cite: 2].",
    'vars': [
        {'name': 'P', 'label': 'Power', 'symbol': 'P', 'units': ['W', 'kW', 'hp']},
        {'name': 'V', 'label': 'Voltage', 'symbol': 'V', 'units': ['V', 'mV', 'kV']},
        {'name': 'I', 'label': 'Current', 'symbol': 'I', 'units': ['A', 'mA']}
    ]
},
{
    'id': 'power_i2r',
    'title': "Electric Power (I²R)",
    'equation': "P = I² * R",
    'desc': "Power dissipation in resistor (Joule heating)[cite: 2].",
    'vars': [
        {'name': 'P', 'label': 'Power', 'symbol': 'P', 'units': ['W', 'kW', 'hp']},
        {'name': 'I', 'label': 'Current', 'symbol': 'I', 'units': ['A', 'mA']},
        {'name': 'R', 'label': 'Resistance', 'symbol': 'R', 'units': ['Ω', 'kΩ', 'MΩ']}
    ]
},
{
    'id': 'power_v2r',
    'title': "Electric Power (V²/R)",
    'equation': "P = V² / R",
    'desc': "Power from voltage across resistor[cite: 2].",
    'vars': [
        {'name': 'P', 'label': 'Power', 'symbol': 'P', 'units': ['W', 'kW', 'hp']},
        {'name': 'V', 'label': 'Voltage', 'symbol': 'V', 'units': ['V', 'mV', 'kV']},
        {'name': 'R', 'label': 'Resistance', 'symbol': 'R', 'units': ['Ω', 'kΩ', 'MΩ']}
    ]
},
{
    'id': 'charge_it',
    'title': "Electric Charge",
    'equation': "Q = I * t",
    'desc': "Charge transferred by current over time[cite: 2].",
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
        'equation': "v = f * λ",
        'desc': "Relates wave speed to frequency and wavelength[cite: 2].",
        'vars': [
            {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
            {'name': 'f', 'label': 'Frequency', 'symbol': 'f', 'units': ['Hz', 'kHz']},
            {'name': 'lam', 'label': 'Wavelength', 'symbol': 'λ', 'units': ['m', 'nm', 'mm']}
        ]
    },
    {
        'id': 'frequency',
        'title': "Frequency",
        'equation': "f = 1 / T",
        'desc': "Frequency is the number of oscillations per second.",
        'vars': [
            {'name': 'f', 'label': 'Frequency', 'symbol': 'f', 'units': ['Hz', 'kHz']},
            {'name': 'T', 'label': 'Period', 'symbol': 'T', 'units': ['s', 'ms']}
        ]
    },
    {
        'id': 'angular_frequency',
        'title': "Angular Frequency",
        'equation': "ω = 2πf",
        'desc': "Angular frequency relates frequency to rotational motion.",
        'vars': [
            {'name': 'omega', 'label': 'Angular Frequency', 'symbol': 'ω', 'units': ['rad/s']},
            {'name': 'f', 'label': 'Frequency', 'symbol': 'f', 'units': ['Hz', 'kHz']}
        ]
    },
    {
        'id': 'period',
        'title': "Period",
        'equation': "T = 1 / f",
        'desc': "Period is the time for one complete cycle.",
        'vars': [
            {'name': 'T', 'label': 'Period', 'symbol': 'T', 'units': ['s', 'ms']},
            {'name': 'f', 'label': 'Frequency', 'symbol': 'f', 'units': ['Hz', 'kHz']}
        ]
    }
]
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SolveMate | Physics Library</title>
    <style>
        :root { --primary: #3b82f6; --bg: #ffffff; --card: #f8fafc; --text: #1e293b; --border: #e2e8f0; }
        [data-theme='dark'] { --bg: #0f172a; --card: #1e293b; --text: #f8fafc; --border: #334155; }

        body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', sans-serif; transition: all 0.3s; margin: 0; }
        .nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 40px; border-bottom: 1px solid var(--border); }
        .container { max-width: 1200px; margin: auto; padding: 40px 20px; }

        .theme-toggle { background: var(--primary); color: white; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; }
        .search-box { width: 100%; padding: 15px; border-radius: 12px; border: 1px solid var(--border); background: var(--card); color: var(--text); margin-bottom: 40px; font-size: 1rem; }

        .library-section { margin-bottom: 40px; }
        .section-title { font-size: 1.5rem; margin-bottom: 20px; padding-left: 10px; border-left: 4px solid var(--primary); }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; }

        .card { background: var(--card); padding: 25px; border-radius: 16px; border: 1px solid var(--border); cursor: pointer; transition: transform 0.2s; }
        .card:hover { transform: translateY(-5px); border-color: var(--primary); }
        .eqn { font-family: monospace; color: #f59e0b; font-size: 1.3rem; margin: 10px 0; }
        .desc { font-size: 0.9rem; opacity: 0.8; height: 40px; overflow: hidden; }

        .modal { position: fixed; inset: 0; background: rgba(0,0,0,0.8); display: none; align-items: center; justify-content: center; z-index: 100; }
        .modal-content { background: var(--bg); width: 90%; max-width: 500px; padding: 30px; border-radius: 24px; border: 1px solid var(--border); }
        .input-row { display: grid; grid-template-columns: 2fr 1fr; gap: 10px; margin-bottom: 15px; }
        input, select { background: var(--card); color: var(--text); border: 1px solid var(--border); padding: 10px; border-radius: 8px; width: 100%; }
        .solve-btn { width: 100%; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; }
        #result-box { margin-top: 20px; padding: 15px; border-radius: 10px; display: none; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="nav">
        <h1>SolveMate</h1>
        <button class="theme-toggle" onclick="toggleTheme()">🌓 Toggle Theme</button>
    </div>

    <div class="container">
        <input type="text" class="search-box" id="search" placeholder="Search formulas..." onkeyup="searchLib()">

        {% for category, formulas in library.items() %}
        <div class="library-section">
            <h2 class="section-title">{{category}}</h2>
            <div class="grid">
                {% for f in formulas %}
                <div class="card" onclick="openSolver('{{f.id}}')" data-search="{{f.title}} {{f.equation}} {{category}}">
                    <h3>{{f.title}}</h3>
                    <div class="eqn">{{f.equation}}</div>
                    <p class="desc">{{f.desc}}</p>
                    <button class="solve-btn" style="margin-top:10px;">Open Solver</button>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>

    <div class="modal" id="modal">
        <div class="modal-content">
            <h2 id="m-title"></h2>
            <p style="font-size: 0.85rem; opacity:0.7;">Leave one field blank to solve for it[cite: 2].</p>
            <div id="m-inputs" oninput="updateBtn()"></div>
            <button class="solve-btn" id="m-calc" onclick="runCalc()">Calculate</button>
            <div id="result-box"></div>
            <button onclick="closeModal()" style="width:100%; background:none; border:none; margin-top:15px; color:var(--text); cursor:pointer;">Close</button>
        </div>
    </div>

    <script>
        let activeF = null;

        function toggleTheme() {
            const current = document.documentElement.getAttribute('data-theme');
            const target = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', target);
            localStorage.setItem('theme', target);
        }

        if(localStorage.getItem('theme')) {
            document.documentElement.setAttribute('data-theme', localStorage.getItem('theme'));
        }

        function searchLib() {
            const query = document.getElementById('search').value.toLowerCase();
            document.querySelectorAll('.card').forEach(card => {
                card.style.display = card.dataset.search.toLowerCase().includes(query) ? 'block' : 'none';
            });
        }

        function openSolver(id) {
            fetch(`/api/formula/${id}`).then(r => r.json()).then(f => {
                activeF = f;
                document.getElementById('m-title').innerText = f.title;
                document.getElementById('m-inputs').innerHTML = f.vars.map(v => `
                    <div class="input-row">
                        <div>
                            <label style="font-size:0.75rem;">${v.label} (${v.symbol})</label>
                            <input type="number" id="v_${v.name}" data-label="${v.label}" step="any">
                        </div>
                        <div>
                            <label style="font-size:0.75rem;">Unit</label>
                            <select id="u_${v.name}">${v.units.map(u => `<option value="${u}">${u}</option>`).join('')}</select>
                        </div>
                    </div>
                `).join('');
                document.getElementById('modal').style.display = 'flex';
                document.getElementById('result-box').style.display = 'none';
                updateBtn();
            });
        }

        function updateBtn() {
            const empty = Array.from(document.querySelectorAll('#m-inputs input')).filter(i => i.value === "");
            const btn = document.getElementById('m-calc');
            btn.innerText = empty.length === 1 ? `Solve for ${empty[0].dataset.label}` : "Fill Values";
            btn.disabled = empty.length !== 1;
        }

        function closeModal() { document.getElementById('modal').style.display = 'none'; }

                function runCalc() {
            const payload = { fid: activeF.id, vals: {}, units: {} };
            activeF.vars.forEach(v => {
                payload.vals[v.name] = document.getElementById(`v_${v.name}`).value;
                payload.units[v.name] = document.getElementById(`u_${v.name}`).value;
            });

            fetch('/api/calculate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            }).then(r => r.json()).then(data => {
                const box = document.getElementById('result-box');
                box.style.display = 'block';
                if(data.error) {
                    box.style.background = '#fee2e2'; box.style.color = '#dc2626'; box.innerText = data.error;
                } else {
                    box.style.background = '#dcfce7'; box.style.color = '#166534';
                                                    if(data.steps) {
                    let stepsHtml = data.steps.map(s => `<div>${s}</div>`).join('');
                    box.innerHTML = `
                        <strong>Result: ${data.res.toFixed(4)} ${data.unit}</strong>
                        <div style="margin-top:8px; font-size:0.9em; text-align:left;">
                            ${stepsHtml}
                        </div>
                    `;
                } else {
                    box.innerHTML = `Result: ${data.res.toFixed(4)} ${data.unit}`;
                }
                }
            });
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, library=physics_library)


@app.route('/api/formula/<fid>')
def get_f(fid):
    for formulas in physics_library.values():
        for f in formulas:
            if f['id'] == fid: return jsonify(f)
    return jsonify({'error': '404'}), 404


def normalize(val, unit):
    conv = {
        'km/h': 1 / 3.6, 'g': 0.001, 'lb': 0.4535, 'mV': 0.001, 'kV': 1000,
        'mA': 0.001, 'kΩ': 1000, 'MΩ': 1e6, 'cm': 0.01, 'ft': 0.3048,
        'nm': 1e-9, 'mm': 0.001, 'kHz': 1000, 'ms': 0.001, 'C': 1.0
    }
    if unit == 'deg':
        return math.radians(float(val))
    return float(val) * conv.get(unit, 1.0)

def denormalize(val, unit):
    conv = {
        'km/h': 3.6, 'g': 1000, 'lb': 1 / 0.4535, 'mV': 1000, 'kV': 0.001,
        'mA': 1000, 'kΩ': 0.001, 'MΩ': 1e-6, 'cm': 100, 'ft': 1 / 0.3048,
        'nm': 1e9, 'mm': 1000, 'kHz': 0.001, 'ms': 1000, 'C': 1.0
    }
    if unit == 'deg':
        return math.degrees(val)
    return val * conv.get(unit, 1.0)


def format_value(val, decimals=3):
    """Format value for display with proper scientific notation."""
    if abs(val) == 0:
        return "0"

    # Use scientific notation for very small/large numbers
    if abs(val) < 0.001 or abs(val) > 10000:
        formatted = f"{val:.{decimals - 1}e}"
        mantissa, exponent = formatted.split('e')

        # Handle exponent properly (supports up to 10^99+)
        exp_val = int(exponent)
        exp_sign = '⁻' if exp_val < 0 else ''
        exp_abs = abs(exp_val)

        # Convert number to superscript string
        superscript_map = '⁰¹²³⁴⁵⁶⁷⁸⁹'
        superscript = ''.join(superscript_map[int(d)] for d in str(exp_abs))

        return f"{mantissa} × 10<span style='font-size:0.7em;vertical-align:super'>{exp_sign}{superscript}</span>"

    # Regular formatting for normal range (preserves significant figures)
    return f"{float(val):.{decimals}g}"


def generate_detailed_steps(fid, target, v_normalized, v_display, units, res_normalized, res_display):
    """Generate detailed, educational step-by-step solution."""
    steps = []
    step_num = 1

    # Step 1: Identify formula
    formula_eq = "Formula not found"
    for cat in physics_library.values():
        for f in cat:
            if f['id'] == fid:
                formula_eq = f['equation']
                break
        if formula_eq != "Formula not found": break

    steps.append(f"Step {step_num}: Use the formula: <strong>{formula_eq}</strong>")
    step_num += 1

    # Step 2: Rearrange for target variable (if needed)
    rearrange_step = {
        'v_final': {'v': '', 'u': 'v - at', 'a': '(v - u)/t', 't': '(v - u)/a'},
        'displacement': {'s': '', 'u': '(s - ½at²)/t', 'a': '2(s - ut)/t²', 't': 'Quadratic solution'},
        'v_squared': {'v': '√(u² + 2as)', 'u': '√(v² - 2as)', 'a': '(v² - u²)/(2s)', 's': '(v² - u²)/(2a)'},
        'f_ma': {'F': '', 'm': 'F/a', 'a': 'F/m'},
        'kinetic_e': {'KE': '', 'm': '2KE/v²', 'v': '√(2KE/m)'},
        # Add more as needed
    }.get(fid, {}).get(target, f"Solve for {target}")

    if rearrange_step:
        steps.append(f"Step {step_num}: Rearrange to solve for {target}: <strong>{target} = {rearrange_step}</strong>")
        step_num += 1

    # Step 3+: Substitute values and show calculations
    if fid == 'v_final':
        if target == 'v':
            steps.append(
                f"Step {step_num}: Substitute: v = {format_value(v_display['u'])} + {format_value(v_display['a'])} × {format_value(v_display['t'])}")
            step_num += 1
            steps.append(
                f"Step {step_num}: Multiply: {format_value(v_display['a'])} × {format_value(v_display['t'])} = {format_value(v_display['a'] * v_display['t'])}")
            step_num += 1
            steps.append(
                f"Step {step_num}: Add: {format_value(v_display['u'])} + {format_value(v_display['a'] * v_display['t'])} = <strong>{format_value(res_display)}</strong> {units[target]}")
        elif target == 'a':
            steps.append(
                f"Step {step_num}: Substitute: a = ({format_value(v_display['v'])} - {format_value(v_display['u'])}) / {format_value(v_display['t'])}")
            step_num += 1
            steps.append(
                f"Step {step_num}: Subtract: {format_value(v_display['v'])} - {format_value(v_display['u'])} = {format_value(v_display['v'] - v_display['u'])}")
            step_num += 1
            steps.append(
                f"Step {step_num}: Divide: {format_value(v_display['v'] - v_display['u'])} / {format_value(v_display['t'])} = <strong>{format_value(res_display)}</strong> {units[target]}")

    elif fid == 'f_ma':
        if target == 'F':
            steps.append(
                f"Step {step_num}: Substitute: F = {format_value(v_display['m'])} × {format_value(v_display['a'])}")
            step_num += 1
            steps.append(
                f"Step {step_num}: Multiply: {format_value(v_display['m'])} × {format_value(v_display['a'])} = <strong>{format_value(res_display)}</strong> {units[target]}")
        elif target == 'a':
            steps.append(
                f"Step {step_num}: Divide: a = {format_value(v_display['F'])} / {format_value(v_display['m'])}")
            step_num += 1
            steps.append(
                f"Step {step_num}: {format_value(v_display['F'])} / {format_value(v_display['m'])} = <strong>{format_value(res_display)}</strong> {units[target]}")

    elif fid == 'distance_cv':
        if target == 'd':
            steps.append(
                f"Step {step_num}: Multiply: d = {format_value(v_display['v'])} × {format_value(v_display['t'])} = <strong>{format_value(res_display)}</strong> {units[target]}")
        elif target == 't':
            steps.append(
                f"Step {step_num}: Divide: t = {format_value(v_display['d'])} / {format_value(v_display['v'])} = <strong>{format_value(res_display)}</strong> {units[target]}")

    # Generic substitution for simple cases
    else:
        steps.append(f"Step {step_num}: Substitute known values into formula for {target}")
        step_num += 1
        steps.append(f"Step {step_num}: <strong>Result: {format_value(res_display)} {units[target]}</strong>")

    return steps


@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    fid, vals, units = data['fid'], data['vals'], data['units']
    missing = [k for k, v in vals.items() if v == ""]

    if len(missing) != 1: return jsonify({'error': 'Leave exactly one blank[cite: 2].'})

    target = missing[0]
    v = {k: normalize(val, units[k]) for k, val in vals.items() if val != ""}
    if any(val == 0 for val in v.values()):
        return jsonify({'error': 'Zero values may cause invalid calculations.'})
    g = 9.806

    try:
        res = 0
        if fid == 'v_final':
            if target == 'v':
                res = v['u'] + (v['a'] * v['t'])
            elif target == 'u':
                res = v['v'] - (v['a'] * v['t'])
            elif target == 'a':
                res = (v['v'] - v['u']) / v['t']
            elif target == 't':
                if v['a'] == 0:
                    return jsonify({'error': 'Cannot solve for time with zero acceleration.'})
                res = (v['v'] - v['u']) / v['a']
        elif fid == 'range':
            if target == 'R':
                den = math.sin(2 * v['theta'])
                if abs(den) < 1e-10:
                    return jsonify({'error': 'Angle makes range undefined (sin(2θ)=0).'})
                res = (v['v'] ** 2 * den) / g
            elif target == 'v':
                den = math.sin(2 * v['theta'])
                if abs(den) < 1e-10:
                    return jsonify({'error': 'Angle makes range undefined (sin(2θ)=0).'})
                res = math.sqrt((v['R'] * g) / den)
            elif target == 'theta':
                # Solve for theta (more complex, using inverse trig)
                ratio = (v['R'] * g) / (v['v'] ** 2)
                if abs(ratio) > 1:
                    return jsonify({'error': 'No real angle solution exists.'})
                res = 0.5 * math.asin(ratio)
        elif fid == 'displacement':
            if target == 's':
                res = v['u'] * v['t'] + 0.5 * v['a'] * (v['t'] ** 2)
            elif target == 'u':
                # s = ut + ½at² → u = (s - ½at²)/t
                if v['t'] == 0:
                    return jsonify({'error': 'Cannot solve for initial velocity with zero time.'})
                res = (v['s'] - 0.5 * v['a'] * (v['t'] ** 2)) / v['t']
            elif target == 'a':
                # s = ut + ½at² → a = 2(s - ut)/t²
                if v['t'] == 0:
                    return jsonify({'error': 'Cannot solve for acceleration with zero time.'})
                res = 2 * (v['s'] - v['u'] * v['t']) / (v['t'] ** 2)
            elif target == 't':
                # Quadratic equation: ½at² + ut - s = 0
                a_coef, b_coef, c_coef = 0.5 * v['a'], v['u'], -v['s']
                if abs(a_coef) < 1e-10:  # No acceleration
                    if abs(b_coef) < 1e-10:
                        return jsonify({'error': 'No solution with zero acceleration and velocity.'})
                    res = v['s'] / v['u']
                else:
                    disc = b_coef ** 2 - 4 * a_coef * c_coef
                    if disc < 0:
                        return jsonify({'error': 'No real time solution exists.'})
                    res = (-b_coef + math.sqrt(disc)) / (2 * a_coef)  # Positive root
                    if res < 0:
                        res = (-b_coef - math.sqrt(disc)) / (2 * a_coef)
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
                if v['v'] == 0:
                    return jsonify({'error': 'Cannot solve for time with zero velocity.'})
                res = v['d'] / v['v']
        elif fid == 'work_fdcos':
            if target == 'W':
                res = v['F'] * v['d'] * math.cos(v['theta'])
            elif target == 'F':
                res = v['W'] / (v['d'] * math.cos(v['theta']))
            elif target == 'd':
                if abs(math.cos(v['theta'])) < 1e-10:
                    return jsonify({'error': 'Cosine of angle is zero - undefined.'})
                res = v['W'] / (v['F'] * math.cos(v['theta']))
            elif target == 'theta':
                # W = F d cos(θ) → θ = acos(W/(F d))
                arg = v['W'] / (v['F'] * v['d'])
                if arg < -1 or arg > 1:
                    return jsonify({'error': 'No real angle solution exists.'})
                res = math.acos(arg)
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
                if v['PE'] < 0:
                    return jsonify({'error': 'Potential energy cannot be negative.'})
                res = math.sqrt((2 * v['PE']) / v['k'])
        elif fid == 'power_wt':
            if target == 'P':
                res = v['W'] / v['t']
            elif target == 'W':
                res = v['P'] * v['t']
            elif target == 't':
                if v['P'] == 0:
                    return jsonify({'error': 'Cannot solve for time with zero power.'})
                res = v['W'] / v['P']
        elif fid == 'f_ma':
            if target == 'F':
                res = v['m'] * v['a']
            elif target == 'm':
                res = v['F'] / v['a']
            elif target == 'a':
                res = v['F'] / v['m']
        elif fid == 'centripetal':
            if target == 'Fc':
                res = (v['m'] * v['v'] ** 2) / v['r']
            elif target == 'm':
                res = (v['Fc'] * v['r']) / (v['v'] ** 2)
            elif target == 'v':
                res = math.sqrt((v['Fc'] * v['r']) / v['m'])
            elif target == 'r':
                res = (v['m'] * v['v'] ** 2) / v['Fc']
        elif fid == 'kinetic_e':
            if target == 'KE':
                res = 0.5 * v['m'] * (v['v'] ** 2)
            elif target == 'm':
                res = (2 * v['KE']) / (v['v'] ** 2)
            elif target == 'v':
                res = math.sqrt((2 * v['KE']) / v['m'])
        elif fid == 'momentum':
            if target == 'p':
                res = v['m'] * v['v']
            elif target == 'm':
                res = v['p'] / v['v']
            elif target == 'v':
                res = v['p'] / v['m']
        elif fid == 'ohm':
            if target == 'V':
                res = v['I'] * v['R']
            elif target == 'I':
                res = v['V'] / v['R']
            elif target == 'R':
                res = v['V'] / v['I']
        elif fid == 'wave_v':
            if target == 'v':
                res = v['f'] * v['lam']
            elif target == 'f':
                res = v['v'] / v['lam']
            elif target == 'lam':
                res = v['v'] / v['f']
        elif fid == 'centripetal_acc':
            if target == 'a_c': res = (v['v'] ** 2) / v['r']
            elif target == 'v': res = math.sqrt(v['a_c'] * v['r'])
            elif target == 'r': res = (v['v'] ** 2) / v['a_c']
        elif fid == 'angular_velocity':
            if target == 'omega': res = v['theta'] / v['t']
            elif target == 'theta': res = v['omega'] * v['t']
            elif target == 't': res = v['theta'] / v['omega']
        elif fid == 'linear_velocity_circ':
            if target == 'v': res = v['r'] * v['omega']
            elif target == 'r': res = v['v'] / v['omega']
            elif target == 'omega': res = v['v'] / v['r']
        elif fid == 'power_vi':
            if target == 'P': res = v['V'] * v['I']
            elif target == 'V': res = v['P'] / v['I']
            elif target == 'I': res = v['P'] / v['V']
        elif fid == 'power_i2r':
            if target == 'P': res = (v['I'] ** 2) * v['R']
            elif target == 'I': res = math.sqrt(v['P'] / v['R'])
            elif target == 'R': res = v['P'] / (v['I'] ** 2)
        elif fid == 'power_v2r':
            if target == 'P': res = (v['V'] ** 2) / v['R']
            elif target == 'V': res = math.sqrt(v['P'] * v['R'])
            elif target == 'R': res = (v['V'] ** 2) / v['P']
        elif fid == 'charge_it':
            if target == 'Q': res = v['I'] * v['t']
            elif target == 'I': res = v['Q'] / v['t']
            elif target == 't': res = v['Q'] / v['I']
        elif fid == 'frequency':
            if target == 'f':
                if v['T'] == 0:
                    return jsonify({'error': 'Cannot solve for frequency with zero period.'})
                res = 1 / v['T']
            elif target == 'T':
                if v['f'] == 0:
                    return jsonify({'error': 'Cannot solve for period with zero frequency.'})
                res = 1 / v['f']
        elif fid == 'angular_frequency':
            if target == 'omega':
                res = 2 * math.pi * v['f']
            elif target == 'f':
                res = v['omega'] / (2 * math.pi)
        elif fid == 'period':
            if target == 'T':
                if v['f'] == 0:
                    return jsonify({'error': 'Cannot solve for period with zero frequency.'})
                res = 1 / v['f']
            elif target == 'f':
                if v['T'] == 0:
                    return jsonify({'error': 'Cannot solve for frequency with zero period.'})
                res = 1 / v['T']

        # Denormalize result
        final_res = denormalize(res, units[target])

        # Create display values (denormalized inputs)
        v_display = {k: denormalize(val, units[k]) for k, val in v.items()}

        # Generate detailed steps
        steps = generate_detailed_steps(fid, target, v, v_display, units, res, final_res)

        return jsonify({
            'res': final_res,
            'unit': units[target],
            'steps': steps
        })

        return jsonify({
            'res': final_res,
            'unit': units[target],
            'steps': steps
        })
    except Exception:
        return jsonify({'error': 'Check inputs for zero or negative values.'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
