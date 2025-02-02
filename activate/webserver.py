from flask import Flask
import json
from gpu_data import get_available_gpus
from config_topology import generate_topology_from_config

class TopologyWebServer:
    def __init__(self, config_filepath, total_gpus=96, host='0.0.0.0', port=5000):
        """
        Initialize the web server with a given configuration file, total GPU count,
        and the host/port to bind the Flask app.
        """
        self.config_filepath = config_filepath
        self.total_gpus = total_gpus
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        """
        Define the Flask route(s). In this example, the root URL ("/") will generate
        the current 3D topology and display it as formatted text.
        """
        @self.app.route("/")
        def topology():
            # Retrieve current GPU information.
            gpu_info = get_available_gpus()

            # Generate the topology, parallel settings, and full config using the provided YAML.
            topology, parallel_settings, config = generate_topology_from_config(
                self.config_filepath, gpu_info, self.total_gpus
            )

            # Build a multi-line string representing the topology.
            output_lines = []
            output_lines.append("Parallel Settings:")
            output_lines.append(json.dumps(parallel_settings, indent=4))
            output_lines.append("\nGenerated 3D Topology:")

            for dp_idx, data_group in enumerate(topology):
                output_lines.append(f"Data Parallel Group {dp_idx}:")
                for pp_idx, pipe_group in enumerate(data_group):
                    output_lines.append(f"  Pipeline Stage {pp_idx}:")
                    for gpu_str in pipe_group:
                        output_lines.append(f"    {gpu_str}")

            output_lines.append("\nFull Configuration:")
            output_lines.append(json.dumps(config, indent=4))
            output_text = "\n".join(output_lines)

            # Return the output wrapped in <pre> tags to preserve formatting.
            return f"<pre>{output_text}</pre>"

    def run(self):
        """
        Run the Flask web server.
        """
        self.app.run(host=self.host, port=self.port)
