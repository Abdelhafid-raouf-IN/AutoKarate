import os
import subprocess
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Utiliser des chaînes brutes pour les chemins
SCENARIO_DIR = r'C:\Users\RAOUF Abdelhafid\Desktop\ScenarioGen\unibank.service-testing'
KARATE_JAR = r'C:\Users\RAOUF Abdelhafid\Desktop\ScenarioGen\karate-1.5.0.jar'

@app.route('/')
def index():
    scenarios = [f for f in os.listdir(SCENARIO_DIR) if f.endswith('.feature')]
    return render_template('index.html', scenarios=scenarios)

@app.route('/execute-scenario', methods=['POST'])
def execute_scenario():
    data = request.get_json()
    scenario = data['scenario']
    scenario_path = os.path.join(SCENARIO_DIR, scenario)

    if not os.path.isfile(scenario_path):
        return jsonify({"error": "Scenario file not found"}), 404

    if not os.path.isfile(KARATE_JAR):
        return jsonify({"error": "Karate JAR file not found"}), 404

    try:
        result = subprocess.run(['java', '-jar', KARATE_JAR, 'test', scenario_path],
                                capture_output=True, text=True)
        output = result.stdout
        error = result.stderr
        if error:
            return jsonify({"error": error}), 500
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/execute-all-scenarios', methods=['POST'])
def execute_all_scenarios():
    scenarios = [f for f in os.listdir(SCENARIO_DIR) if f.endswith('.feature')]
    results = []

    if not os.path.isfile(KARATE_JAR):
        return jsonify({"error": "Karate JAR file not found"}), 404

    for scenario in scenarios:
        scenario_path = os.path.join(SCENARIO_DIR, scenario)
        try:
            result = subprocess.run(['java', '-jar', KARATE_JAR, 'test', scenario_path],
                                    capture_output=True, text=True)
            output = result.stdout
            error = result.stderr
            if error:
                results.append({"scenario": scenario, "status": "error", "message": error})
            else:
                results.append({"scenario": scenario, "status": "success", "output": output})
        except Exception as e:
            results.append({"scenario": scenario, "status": "error", "message": str(e)})

    return jsonify({"results": results})


if __name__ == '__main__':
    app.run(debug=True)
