import argparse
import pathlib
import os
import shutil
import confuse
from confuse.exceptions import NotFoundError
from confuse.templates import Filename

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
            self.fail(f"No such file or directory: {path}", view, True)

class ExecutableValidate(confuse.Template):
    """
    Check existence of executables using "which" command
    """
    def value(self, view, template=None):
        path = view.get()
        abs_path = shutil.which(path)
        if abs_path is not None:
            return path
        else:
            self.fail(f"No such executable: {path}", view, True)

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

    uppaal_template = {
        'dir': FilenameValidate(cwd=pathlib.Path(__file__).parent.absolute()),
        'model': FilenameValidate(relative_to="dir"),
        'query': FilenameValidate(relative_to="dir"),
        'verifyta': ExecutableValidate(),
        'debug': False,
        'variables': confuse.MappingValues(
            confuse.OneOf([
                confuse.Number(),
                confuse.TypeTemplate(list)
                ])
            )
    }

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

    mpc_template = {
        'step': 5,
        'warmup': 1
    }
    
    logging_template = confuse.Optional(
            confuse.Sequence({
               'metric': confuse.Choice(['objective', 'state', 'signals']),
               'dir': FilenameValidate(cwd=pathlib.Path(__file__).parent.absolute())
            })
        )

    template = {
        'name': str,
        'uppaal': uppaal_template,
        'sumo': sumo_template,
        'mpc': mpc_template,
        'logging': logging_template
    }

    valid_config = config.get(template)

    #check files exist
    return valid_config

if __name__ == "__main__":
    pass