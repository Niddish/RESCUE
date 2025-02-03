import json
import os
from flask import Flask

app = Flask(__name__)

# Path to the JSON file produced by main.py
FILE_PATH = "gpu_topology.json"

@app.route("/")
def index():
    # Check if the file exists
    if not os.path.exists(FILE_PATH):
        return ("<h2>Data file not found.</h2>"
                "<p>Please run the main script to generate the data.</p>")
    
    try:
        # Read the JSON data from the file
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
        # Format the JSON data as a pretty-printed string
        formatted_data = json.dumps(data, indent=4)
    except Exception as e:
        return f"<h2>Error reading file:</h2><p>{e}</p>"

    # Return HTML that includes a meta refresh tag to reload every 5 seconds
    html_content = f"""
    <html>
      <head>
        <meta http-equiv="refresh" content="5">
        <title>GPU Topology Monitor</title>
      </head>
      <body>
        <h2>GPU Topology Data (updated every 5 seconds):</h2>
        <pre>{formatted_data}</pre>
      </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    # Run the Flask app on all interfaces so that it is accessible via SSH tunneling
    app.run(host="0.0.0.0", port=8080)
