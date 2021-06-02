import argparse
import pathlib

import confuse

def get_valid_config():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", type=str, required=True,
        help="yaml configuration file")
    args = ap.parse_args()

    source = confuse.YamlSource(args.config)
    config = confuse.RootView([source])

    # build templates
    sumo_template = {
        'dir': confuse.Path(cwd=pathlib.Path(__file__).parent.absolute()),
        'model': confuse.Filename(relative_to="dir"),
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
    return valid_config

if __name__ == "__main__":
    pass