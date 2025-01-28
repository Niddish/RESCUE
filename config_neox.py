import json
import yaml

def load_config(filepath):
    """Load the YAML configuration file."""
    with open(filepath, 'r') as f:
        config = yaml.safe_load(f)
    return config

def extract_parallel_settings(config, total_gpus=64):
    """Extract parallelism settings and compute data parallel size."""
    pipe_parallel_size = config.get("pipe_parallel_size", 1)
    model_parallel_size = config.get("model_parallel_size", 1)
    
    # Compute data parallel size
    data_parallel_size = total_gpus // (pipe_parallel_size * model_parallel_size)
    
    return {
        "pipe_parallel_size": pipe_parallel_size,
        "model_parallel_size": model_parallel_size,
        "data_parallel_size": data_parallel_size,
    }

def check_zero_optimization(config):
    """Check for ZeRO optimization settings."""
    zero_config = config.get("zero_optimization", {})
    zero_stage = zero_config.get("stage", 0)
    return zero_stage

def construct_3d_topology(parallel_settings, total_gpus=96):
    """Construct a 3D topology representation."""
    pipe_size = parallel_settings["pipe_parallel_size"]
    model_size = parallel_settings["model_parallel_size"]
    data_size = parallel_settings["data_parallel_size"]
    
    topology = []
    gpu_id = 0
    
    for dp in range(data_size):
        data_group = []
        for pp in range(pipe_size):
            pipe_group = []
            for mp in range(model_size):
                pipe_group.append(f"GPU {gpu_id}")
                gpu_id += 1
            data_group.append(pipe_group)
        topology.append(data_group)
    
    return topology

def main(config_path):
    config = load_config(config_path)
    
    # Extract values
    parallel_settings = extract_parallel_settings(config)
    zero_stage = check_zero_optimization(config)
    topology = construct_3d_topology(parallel_settings)
    
    # Print results
    print("\nParallelism Settings:")
    print(json.dumps(parallel_settings, indent=4))
    print("\nZeRO Optimization Stage:", zero_stage)
    print("\n3D Topology:")
    for dp, data_group in enumerate(topology):
        print(f"Data Parallel Group {dp}:")
        for pp, pipe_group in enumerate(data_group):
            print(f"  Pipeline Stage {pp}: {pipe_group}")

if __name__ == "__main__":
    config_filepath = "20B.yml"  # Change this to your actual file path
    main(config_filepath)
