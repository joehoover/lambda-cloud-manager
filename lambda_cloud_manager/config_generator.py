from lambda_cloud_manager.api_adapters import InstanceManager


def generate_config(
        instance_type: str = "gpu_1x_a10",
        region: str = "us-west-1",
):
    """

    Parameters
    ----------
    instance_type: str
        Type of instance to generate config for. Currently supported:
    region: str
        Instance region.
    Returns
    -------
        dict
    """

    config = {
        "region_name": region,
        "instance_type_name": instance_type,
        "ssh_key_names": [
            ""
        ],
        "file_system_names": [],
        "quantity": 1
    }

    return config

