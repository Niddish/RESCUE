import json
from gpu_data import get_available_gpus
from config_topology import generate_topology_from_config

def main():
    # Define the path to your Neox YAML configuration file.
    config_filepath = "20B.yml"
    
    # Retrieve GPU info from the GPU data library.
    gpu_info = get_available_gpus()
    
    # Generate the topology using the configuration and GPU data.
    topology, parallel_settings, config = generate_topology_from_config(config_filepath, gpu_info, total_gpus=96)
    
    # Print out the parallel settings.
    print("Parallel Settings:")
    print(json.dumps(parallel_settings, indent=4))
    
    # Print out the generated 3D topology.
    print("\nGenerated 3D Topology:")
    for dp_idx, data_group in enumerate(topology):
        print(f"Data Parallel Group {dp_idx}:")
        for pp_idx, pipe_group in enumerate(data_group):
            print(f"  Pipeline Stage {pp_idx}:")
            for gpu_str in pipe_group:
                print(f"    {gpu_str}")
    
if __name__ == "__main__":
    main()
