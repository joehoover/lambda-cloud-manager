import os
from pathlib import Path

def create_mo_files(setup_kwargs):

    p = os.path.join(
        os.path.expanduser( '~' ),
        '.lambda-cloud-manager'
    )

    Path("p").mkdir(parents=True)

    return setup_kwargs

if __name__ == "__main__":
    create_mo_files({})