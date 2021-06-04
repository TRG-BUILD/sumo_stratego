import strategoutil as sutil
from strategoutil import StrategoController

class Controller(StrategoController):
    def __init__(self, templatefile, model_cfg_dict):
        super().__init__(templatefile, model_cfg_dict, interactive_bash=False)
         # tag left in model_template.xml
        self.tagRule = "//TAG_{}"
        self.objective = 0

    def format_state(self, value):
        """
        Lists and scalars are formatted accordingly
        """
        if isinstance(value, list):
            value = sutil.array_to_stratego(value)
        else:
            value = str(value)
        return value

    def get_objective(self):
        return self.objective

    def update_objective(self):
        C = self.states["A"] + self.states["B"]
        for elem in C:
            self.objective += elem * elem

    def update_state(self, new_values):
        super().update_state(new_values)
        self.update_objective()

    def insert_state(self):
        """
        Override insert state method to format arrays and scalars accodingly
        """
        for name, value in self.states.items():
                tag = self.tagRule.format(name)
                value = self.format_state(value)
                sutil.insert_to_modelfile(self.simulationfile, tag, value)

    def run(self, queryfile="", learning_args=None, verifyta_path="verifyta"):
        output = super().run(queryfile, learning_args, verifyta_path)
        tpls = sutil.get_int_tuples(output)
        result = sutil.get_duration_action(tpls, max_time=1000)
        durations, actions = list(zip(*result)) 
        return durations, actions

if __name__ == "__main__":
    pass