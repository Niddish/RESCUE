import json

def write_output(parallel_settings, topology, configuration, output_file="gpu_topology.json"):
    """
    Write the GPU topology and configuration data to a JSON file.
    
    Args:
        parallel_settings (dict): The extracted parallel settings.
        topology (list): The 3D topology list.
        configuration (dict): The full configuration dictionary.
        output_file (str): The filename to write the JSON output to.
    """
    data = {
        "parallel_settings": parallel_settings,
        "topology": topology,
        "configuration": configuration
    }
    
    try:
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Output successfully written to '{output_file}'")
    except Exception as e:
        print(f"Failed to write output to '{output_file}': {e}")
