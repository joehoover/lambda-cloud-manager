from dotenv import load_dotenv
import pytest

from lambda_cloud_manager.api_adapters import (
    InstanceManager
)


@pytest.fixture()
def example_instance_config():
    config = {
        "region_name": "us-west-1",
        "instance_type_name": "gpu_1x_a10",
        "ssh_key_names": [
            "joehoover-mb"
        ],
        "file_system_names": [],
        "quantity": 1
    }

    return config

def test_get_instances():
    instances = InstanceManager().get_instances()
    assert isinstance(instances, list)


def test_get_instance_types():
    instance_types = InstanceManager().get_instance_types()
    assert isinstance(instance_types, dict)


def test_get_instance_types_available():
    instance_types = InstanceManager().get_instance_types(available=True)

    print(instance_types)
    for instance_type in instance_types.values():
        assert len(instance_type['regions_with_capacity_available']) > 0


def test_launch_from_config_file():
    name = 'test_instance'
    instance_data = InstanceManager().launch('./test_config.json', name=name)
    assert isinstance(instance_data, dict)
    assert isinstance(instance_data["instance_ids"], list)
    assert len(instance_data["instance_ids"]) > 0


def test_terminate_by_name():
    name = 'test_instance'
    instance_data = InstanceManager().launch('./test_config.json', name=name)
    assert isinstance(instance_data, dict)
    assert isinstance(instance_data["instance_ids"], list)
    assert len(instance_data["instance_ids"]) > 0

    termination_data = InstanceManager().terminate(name=name)
    assert isinstance(termination_data, dict)

    instances = InstanceManager().get_instances()
    assert len(instances) == 0
