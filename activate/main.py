import time
import json
from gpu_data import get_available_gpus
from config_topology import generate_topology_from_config
from file_writer import write_output

def main():
    # Define the path to your Neox YAML configuration file.
    config_filepath = "20B.yml"
    
    while True:
        # Retrieve GPU info from the GPU data library.
        gpu_info = get_available_gpus()
        
        # Generate the topology using the configuration and GPU data.
        topology, parallel_settings, config = generate_topology_from_config(config_filepath, gpu_info, total_gpus=96)
        
        # (Optional) Print out the updated data to the console.
        print("Updating GPU Topology Data...")
        
        # Write the output to a JSON file in the same directory.
        write_output(parallel_settings, topology, config)
        
        # Wait 5 seconds before updating again.
        time.sleep(5)

if __name__ == "__main__":
    main()
