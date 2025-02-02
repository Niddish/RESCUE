import yaml

def load_config(filepath):
    """
    Load the YAML configuration file.
    """
    with open(filepath, 'r') as f:
        config = yaml.safe_load(f)
    return config

def extract_parallel_settings(config, total_gpus=96):
    """
    Extract parallelism settings from the configuration and compute data parallel size.
    """
    pipe_parallel_size = config.get("pipe_parallel_size", 1)
    model_parallel_size = config.get("model_parallel_size", 1)
    # Compute data parallel size dynamically.
    data_parallel_size = total_gpus // (pipe_parallel_size * model_parallel_size)
    
    return {
        "pipe_parallel_size": pipe_parallel_size,
        "model_parallel_size": model_parallel_size,
        "data_parallel_size": data_parallel_size,
    }

def construct_3d_topology(parallel_settings, gpu_info):
    """
    Construct a 3D topology representation based on parallel settings and GPU info.
    
    The topology is organized as:
      - Data Parallel groups (outer list)
      - Pipeline Parallel groups (middle list)
      - Model Parallel units (inner list)
    """
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
                if gpu_id < len(gpu_info):
                    gpu_data = gpu_info[gpu_id]
                    gpu_str = (
                        f"GPU {gpu_data['id']} ({gpu_data['name']}) | "
                        f"Mem: {gpu_data['memory_used_MB']}MB/{gpu_data['memory_total_MB']}MB | "
                        f"Util: {gpu_data['utilization_pct']}% | "
                        f"Temp: {gpu_data['temperature_C']}°C"
                    )
                else:
                    gpu_str = f"GPU {gpu_id} (Placeholder)"
                pipe_group.append(gpu_str)
                gpu_id += 1
            data_group.append(pipe_group)
        topology.append(data_group)
    
    return topology

def generate_topology_from_config(config_filepath, gpu_info, total_gpus=96):
    """
    Generate the 3D topology from a given YAML configuration file and GPU info.
    
    Returns a tuple:
      (topology, parallel_settings, full_config)
    """
    config = load_config(config_filepath)
    parallel_settings = extract_parallel_settings(config, total_gpus=total_gpus)
    topology = construct_3d_topology(parallel_settings, gpu_info)
    return topology, parallel_settings, config
