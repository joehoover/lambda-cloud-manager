import typer
import requests
import os
import json
import logging

from dotenv import load_dotenv

from typing import Optional

from .api_adapters import InstanceManager
from .config_generator import generate_config

logging.basicConfig(encoding='utf-8', level=logging.INFO)

load_dotenv()
app = typer.Typer()


@app.command()
def get_instance_types(
        available: bool = False,
) -> dict:
    """

    Parameters
    ----------
    verbose: bool
        If True, returned instance types are printed
    available: bool
        If True, only information for available instance types is returned

    Returns
    -------
    dict
        A dictionary of dictionaries containing information about each instance type


    """

    instance_types = InstanceManager().get_instance_types(available=available)
    logging.info(json.dumps(instance_types, indent=4))

    return instance_types



@app.command()
def get_instances(verbose=True):
    instances = InstanceManager().get_instances()
    logging.info(json.dumps(instances, indent=4))
    return instances

@app.command()
def ssh_keys():
    ssh_keys = InstanceManager().ssh_keys()
    logging.info(json.dumps(ssh_keys, indent=4))

@app.command()
def launch(
        config: str,
        name: str = None,
        verbose: bool = True,
):

    instance_data = InstanceManager().launch(config=config, name=name)
    logging.info(json.dumps(instance_data, indent=4))

    return instance_data

@app.command()
def terminate(
        config: str = None,
        name: Optional[str] = None,
        all: bool = False,
        verbose: bool = True
) -> dict:

    termination_data = InstanceManager().terminate(
        config=config,
        name=name,
        all=all
    )

    logging.info(json.dumps(termination_data, indent=4))

    return termination_data

@app.command()
def write_config(
        path: str,
        instance_type: str = "gpu_1x_a10",
        region: str = "us-west-1",

) -> None:

    config = generate_config(instance_type, region)
    config = json.dumps(config)
    with open(path, 'w') as f:
        f.write(json.dumps(config))

    logging.info(f"Wrote the following config to `{path}`...")
    logging.info(config)
if __name__ == "__main__":
    app()
