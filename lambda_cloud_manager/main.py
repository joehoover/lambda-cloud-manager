import typer
import requests
import os
import json

from dotenv import load_dotenv

from typing import Optional

load_dotenv()
app = typer.Typer()


def _base_get(url: str = "https://cloud.lambdalabs.com/api/v1/", endpoint=None):

    response = requests.get(
        os.path.join(url, endpoint),
        auth=(os.getenv('LAMBDA_API_KEY', ''), '')
    )
    return response


def _base_post(url: str = "https://cloud.lambdalabs.com/api/v1/", endpoint: str = None, data: str = None, json: dict = None):

    headers = {
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(
            os.path.join(url, endpoint),
            auth=(os.getenv('LAMBDA_API_KEY', ''), ''),
            data=data,
            json=json,
        )

        response.raise_for_status()

    except requests.exceptions.HTTPError as errh:
        print("HTTP Error")
        print(errh.args[0])

    return response


@app.command()
def get_instance_types(
        verbose: bool =True,
        available: bool=True
):

    response = _base_get(endpoint='instance-types')
    data = json.loads(response.text).get("data")
    instance_types = json.dumps(data, indent=4)
    if verbose:
        print(instance_types)
    return


@app.command()
def get_instances(verbose=True):

    response = _base_get(endpoint='instances')
    data = json.loads(response.text).get('data')
    if verbose:
        print(json.dumps(data, indent=4))
    return data


@app.command()
def ssh_keys():

    response = _base_get(endpoint='ssh-keys')
    data = json.loads(response.text).get("data")
    print(json.dumps(data, indent=4))


@app.command()
def launch(config_path: str, name: str = None):

    with open(config_path, 'r') as f:
        config = f.read().replace('\n', '').replace('\r', '').encode()

    response = _base_post(endpoint='instance-operations/launch', data=config)
    print(response)

    data = json.loads(response.text).get("data")
    print(json.dumps(data, indent=4))


@app.command()
def terminate(config_path: str = None, name: Optional[str] = None, all: bool = False):

    if name and config_path:
        raise Exception("Specify either `config_path` or name, not both.")

    if (name or config_path) and all:
        raise Exception("To terminate all get_instances, you must not set name or config_path.")


    if config_path:
        with open(config_path, 'r') as f:
            config = json.loads(f.read())
        if 'name' not in config:
            raise Exception("""
            You can only use a config to terminate an 
            instance if the config specifies an instance name.
            """)

        name = config.get("name")

    instance_data = get_instances(verbose=False)

    if not all:
        ids = [i.get("id") for i in instance_data if i.get("name") == name]

    elif all:
        ids = [i.get("id") for i in instance_data]


    config = {
        "instance_ids": ids
    }

    response = _base_post(endpoint='instance-operations/terminate', json=config)
    print(response)
    #
    data = json.loads(response.text).get("data")
    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    app()

