import typer
import requests
import os
import json

from dotenv import load_dotenv

from typing import Optional

URL = "https://cloud.lambdalabs.com/api/v1/"

load_dotenv()

app = typer.Typer()


def _base_get(url: str = URL, endpoint=None):
    response = requests.get(
        os.path.join(url, endpoint),
        auth=(os.getenv('LAMBDA_API_KEY', ''), '')
    )
    return response


def _base_post(url: str = URL, endpoint: str = None, data: str = None, json: dict = None):
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
def instance_types():
    """
    Returns information on available instance types.
    :return: None
    """
    response = _base_get(endpoint='instance-types')
    data = json.loads(response.text).get("data")
    print(json.dumps(data, indent=4))


@app.command()
def instances(verbose=True):
    """
    Returns information on running instances
    :return:
    """
    response = _base_get(endpoint='instances')
    data = json.loads(response.text).get("data")
    if verbose:
        print(json.dumps(data, indent=4))
    return (data)


@app.command()
def ssh_keys():
    """
    Lists SSH keys.
    :return:
    """
    response = _base_get(endpoint='ssh-keys')
    data = json.loads(response.text).get("data")
    print(json.dumps(data, indent=4))


@app.command()
def launch(config_path: str, name: Optional[str] = None):
    """
    Lists SSH keys.
    :return:
    """

    with open(config_path, 'r') as f:
        config = f.read().replace('\n', '').replace('\r', '').encode()

    response = _base_post(endpoint='instance-operations/launch', data=config)
    print(response)

    data = json.loads(response.text).get("data")
    print(json.dumps(data, indent=4))


@app.command()
def terminate(config_path: str = None, name: Optional[str] = None, all: bool = False):
    """
    Lists SSH keys.
    :return:
    """

    if name and config_path:
        raise Exception("Specify either `config_path` or name, not both.")

    if (name or config_path) and all:
        raise Exception("To terminate all instances, you must not set name or config_path.")


    if config_path:
        with open(config_path, 'r') as f:
            config = json.loads(f.read())
        if 'name' not in config:
            raise Exception("""
            You can only use a config to terminate an 
            instance if the config specifies an instance name.
            """)

        name = config.get("name")

    instance_data = instances(verbose=False)

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

    # curl -u secret_joe-mbp_498ab6f0ecf64ab0a4a7edfaa8d03906.eOQACoj1eUBfKDDxp6cuwYPeCibk9YTY: https://cloud.lambdalabs.com/api/v1/instance-operations/launch -d @request.json -H "Content-Type: application/json" | jq .
