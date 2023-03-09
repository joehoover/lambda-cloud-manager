import os
import requests
import logging
import json

from typing import Optional

from dotenv import load_dotenv

logging.basicConfig(encoding='utf-8', level=logging.INFO)


class InstanceManager:
    def __init__(
            self,
            url: str = "https://cloud.lambdalabs.com/api/v1/",
            api_key_var_name: str = 'LAMBDA_API_KEY',
    ):
        load_dotenv()
        self.url = url
        self.api_key_var_name = api_key_var_name

    @staticmethod
    def _handle_config(config: str):
        if isinstance(config, str):
            with open(config, 'r') as f:
                config_data = f.read().replace('\n', '').replace('\r', '').encode()
        else:
            config_data = config

        return config_data


    def _base_get(
            self,
            url: str = None,
            endpoint=None
    ):

        if not url:
            url = self.url

        try:
            response = requests.get(
                os.path.join(url, endpoint),
                auth=(os.getenv(self.api_key_var_name, ''), '')
            )

        except requests.exceptions.HTTPError as errh:
            print("HTTP Error")
            print(errh.args[0])

        return response

    def _base_post(
            self,
            url: str = None,
            endpoint: str = None,
            data: str = None,
            json: dict = None):

        if not url:
            url = self.url

        try:
            response = requests.post(
                os.path.join(url, endpoint),
                auth=(os.getenv(self.api_key_var_name, ''), ''),
                data=data,
                json=json,
            )

            response.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            print("HTTP Error")
            print(errh.args[0])

        return response

    def get_instance_types(
            self,
            verbose: bool = True,
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

        response = self._base_get(endpoint='instance-types')
        instance_types = json.loads(response.text).get("data")

        if available:
            instance_types = {k: v for k, v in instance_types.items() if len(v['regions_with_capacity_available']) > 0}

        return instance_types

    def get_instances(self, verbose=True):
        response = self._base_get(endpoint='instances')
        data = json.loads(response.text).get('data')
        return data

    def ssh_keys(self):
        response = self._base_get(endpoint='ssh-keys')
        data = json.loads(response.text).get("data")
        return data
        # logging.info(json.dumps(data, indent=4))

    def launch(
            self,
            config: str,
            name: str = None,
    ):

        if os.path.isfile(config):
            with open(config, 'r') as f:
                config_data = json.loads(f.read())

        elif isinstance(config, str) and not os.path.isfile(config):
            # Be helpful and check local ./configs directory
            # Also, add a json type to the string, just to be nice :)

            if not config.endswith('.json'):
                config += '.json'

            with open(os.path.join('./configs', config), 'r') as f:
                config_data = json.loads(f.read())

        else:
            config_data = config

        if name:
            config_data['name'] = name

        config_data = json.dumps(config_data).encode()

        response = self._base_post(endpoint='instance-operations/launch', data=config_data)
        instance_data = json.loads(response.text).get("data")

        return instance_data

    def terminate(
            self,
            config: str = None,
            name: Optional[str] = None,
            all: bool = False,
    ) -> dict:
        if name and config:
            raise Exception("Specify either `config_path` or name, not both.")

        if (name or config) and all:
            raise Exception("To terminate all get_instances, you must not set name or config_path.")

        if config:
            config = self._handle_config(config)
            name = config.get("name")

        instance_data = self.get_instances(verbose=False)

        if all:
            logging.info(f'Attempting to terminate all instances...')
            ids = [i.get("id") for i in instance_data]

        else:
            logging.info(f'Attempting to terminate instances associated with the name {name}...')
            ids = [i.get("id") for i in instance_data if i.get("name") == name]

        config = {
            "instance_ids": ids
        }

        response = self._base_post(endpoint='instance-operations/terminate', json=config)
        termination_data = json.loads(response.text).get("data")

        return termination_data