# lambda-cloud-manager

Lambda-cloud-manager is a lightweight command line tool and Python SDK that helps manage Lambda Cloud Instances via the Cloud API. 

## Installation

Currently, poetry is easiest way to install the package. Just run:

```bash
poetry add git+https://github.com/joehoover/lambda-cloud-manager.git
```

## CLI Usage

1. Store your Lambda Cloud API Key as an environmental variable: 

    ```bash
    export LAMBDA_API_KEY="<your-key-here>"
    ```
2. Interact with the Lambda Cloud API via your CLI using the lcm tool. The following commands are supported:

   * `get-instance-types`
   * `get-instances`
   * `ssh-keys`
   * `write-config`
   * `launch`       
   * `terminate`

### Example: Launch a single a10 instance

#### Instance Selection
First, let's see what instances are available. 

```bash
lcm get-instance-types
```

This logs Lambda Cloud instance types to the console. And, when we find the `gpu_1x_a10` instance, we see:

```json
"gpu_1x_a10": {
        "instance_type": {
            "name": "gpu_1x_a10",
            "price_cents_per_hour": 60,
            "description": "1x A10 (24 GB PCIe)",
            "specs": {
                "vcpus": 30,
                "memory_gib": 200,
                "storage_gib": 1400
            }
        },
        "regions_with_capacity_available": [
            {
                "name": "us-west-1",
                "description": "California, USA"
            }
        ]
    },
```

#### Config Specification 

Let's go ahead and generate a config for this instance. We just need to specify the path for our config:

```bash
lcm generate-config ./configs/a10.json
```

This will log the following to your console:

```bash
INFO:root:Wrote the following config to `configs/test.json`...
INFO:root:{
    "region_name": "us-west-1",
    "instance_type_name": "gpu_1x_a10",
    "ssh_key_names": [
        ""
    ],
    "file_system_names": [],
    "quantity": 1
}

```

Now, you need to add your Lambda Cloud ssh key name to the config. If you haven't created one, do that now. Or if you do have one, but you can't remember the name, you can just run:

```bash
lcm ssh-keys
```

which will return information about your configured SSH keys. 

#### Launching your instance

To launch your instance, you can just run:

```bash
lcm launch ./configs/a10.json --name test-instance
```

This will log a response like: 

```json
{
    "instance_ids": [
        "bd7cb0ccfb574f6c876f6c9b1ba5ad38"
    ]
}
```

### Checking for live instances

Let's see if it's running:

```bash
lcm get-instances
```

### Terminating instances

You can terminate instances by name:

```bash
lcm terminate --name test-instance
```

or in bulk:

```bash
lcm terminate --all
```
