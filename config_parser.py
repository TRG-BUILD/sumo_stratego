import argparse
import pathlib
import os
import confuse
from confuse.exceptions import NotFoundError

class FilenameValidate(confuse.Filename):
    """
    Extend confuse.Filename to check existence of files and folders
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def value(self, view, template=None):
        path = super().value(view, template)
        if os.path.exists(path):
            return path
        else:
            raise NotFoundError(f"No such file or directory: {path} ")


def get_valid_config():
    """
    Get a config dict for CLI and valdate all parameters
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", type=str, required=True,
        help="yaml configuration file")
    args = ap.parse_args()

    source = confuse.YamlSource(args.config)
    config = confuse.RootView([source])

    # build templates
    sumo_template = {
        'dir': FilenameValidate(cwd=pathlib.Path(__file__).parent.absolute()),
        'model': FilenameValidate(relative_to="dir"),
        'nogui': False,
        'tls': confuse.MappingTemplate({
            'id': str,
            'phase_map': dict
            }),
        'extract': confuse.Sequence({
            'feature': confuse.Choice(["queue", "speed"]),
            'lanes': dict
            })
    }

    template = {
        'name': str,
        'sumo': sumo_template
    }

    valid_config = config.get(template)

    #check files exist
    return valid_config

if __name__ == "__main__":
    pass