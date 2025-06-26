from pathlib import Path
from ruamel.yaml import YAML
from GUI.utils.popup.popup import ParamPopup 

def set_sim_params(window, _widget):
    yaml_rt = YAML()                         
    CFG     = Path("cpp_gui/files/sim_args.yaml") 

    with CFG.open("r") as f:
        init_cfg = yaml_rt.load(f)       

    def write_and_close():
        with CFG.open("w") as f:
            yaml_rt.dump(init_cfg, f)     
        window.pop_handlers()             
        window.current_popup = None
        window.invalid = True            

    popup = ParamPopup(
        window,
        title="Simulation parameters",
        params=init_cfg,                    
        on_ok=write_and_close
    )

    window.push_handlers(popup)           
    window.current_popup = popup
    window.invalid = True
