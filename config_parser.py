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

    job_template = {
        "job": {
            "name": str,
            "dir": confuse.Optional(
                FilenameValidate(cwd=pathlib.Path(__file__).parent.absolute()),
                default=pathlib.Path(__file__).parent.absolute()
            )            
        }
    }
    job_config = config.get(job_template)

    uppaal_template = {
        'dir': FilenameValidate(cwd=job_config.job.dir),
        'model': FilenameValidate(relative_to="dir"),
        'interface': FilenameValidate(relative_to="dir"),
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
        'dir': FilenameValidate(cwd=job_config.job.dir),
        'model': FilenameValidate(relative_to="dir"),
        'nogui': False,
        'tls': confuse.MappingTemplate({
            'id': str,
            'phase_map': dict,
            'phase_var': str,
            'duration_var': confuse.Optional(str)
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
            confuse.MappingTemplate({
               'metrics': confuse.Sequence(confuse.Choice(['objective', 'state', 'signals']))
            })
        )

    full_template = {
        'uppaal': uppaal_template,
        'sumo': sumo_template,
        'mpc': mpc_template,
        'logging': logging_template
    }
    full_template.update(job_template)
    valid_config = config.get(full_template)

    # add debug and output folders if they are required
    if valid_config.uppaal.debug:
        debug_dir = os.path.join(valid_config.job.dir, "debug")
        os.makedirs(debug_dir, exist_ok=True)
        debug_model = os.path.join(
            debug_dir, 
            f"{valid_config.job.name}_{os.path.basename(valid_config.uppaal.model)}"
            )
        valid_config.uppaal.update({
            "debug_dir": debug_dir,
            "debug_model": debug_model
            })

    if valid_config.logging:
        output_dir = os.path.join(valid_config.job.dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        valid_config.logging.update({"dir": output_dir})

    return valid_config

if __name__ == "__main__":
    pass