from dotenv import load_dotenv

from lambda_cloud_manager.main import (
    get_instances,
    get_instance_types
)


def test_get_instances():
    instances = get_instances()
    assert isinstance(instances, list)

def test_get_instance_types():
    instance_types = get_instance_types()
    assert isinstance(instance_types, dict)

def test_launch():
    assert False
