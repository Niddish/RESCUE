import os
import pynvml

def get_available_gpus():
    """
    Detect available GPUs using NVML and environment variables.
    
    Returns:
        A list of dictionaries, each containing details for a GPU:
        - id: GPU index
        - name: GPU name
        - memory_used_MB: Memory used in MB
        - memory_total_MB: Total memory in MB
        - utilization_pct: GPU utilization percentage
        - temperature_C: GPU temperature in Celsius
    """
    pynvml.nvmlInit()

    # Check CUDA_VISIBLE_DEVICES first
    cuda_visible_devices = os.getenv("CUDA_VISIBLE_DEVICES")
    if cuda_visible_devices:
        gpu_indices = [int(x) for x in cuda_visible_devices.split(",") if x.strip().isdigit()]
    else:
        gpu_indices = list(range(pynvml.nvmlDeviceGetCount()))

    gpu_info = []
    for i in gpu_indices:
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        name = pynvml.nvmlDeviceGetName(handle)
        # Decode bytes to string if necessary.
        if isinstance(name, bytes):
            name = name.decode("utf-8")
        memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        
        gpu_info.append({
            "id": i,
            "name": name,
            "memory_used_MB": memory.used // (1024 * 1024),
            "memory_total_MB": memory.total // (1024 * 1024),
            "utilization_pct": utilization.gpu,
            "temperature_C": temperature
        })

    pynvml.nvmlShutdown()
    return gpu_info
