def set_all_states(state):
    if "input_file" not in state:
        state.input_file = None
    if "file_path" not in state:
        state.file_path = None
    if "current_earth_model" not in state:
        state.current_earth_model = None
    if "current_layer" not in state:
        state.current_layer = None
    if "current_interface" not in state:
        state.current_interface = None
    if "current_fluid" not in state:
        state.current_fluid = None
    if "current_model" not in state:
        state.current_model = None
    if "current_parameters" not in state:
        state.current_parameters = None
    if "file_uploaded" not in state:
        state.file_uploaded = False
    if "layer_modelled" not in state:
        state.layer_modelled = False
    if "AVO_modelled" not in state:
        state.AVO_modelled = False
    if "wavefield_modelled" not in state:
        state.wavefield_modelled = False
    if "complete_simulation" not in state:
        state.complete_simulation = False
    return state


def state_upload_file_none(state):
    state.process_select = None
    state.process_select_confirmed = False
    state.method_one_df = None
    state.query_method_one = None
    state.prompt_method_one = None
    state.get_response_method_one = None
    state.response_method_one = None
    state.save_query = False
    state.que_response_gen = False

    return state


def state_upload_file_3_none(state):
    state.file_3 = None
    state.file_path_3 = None
    state.query_method_three = None
    state.save_query_three = False
    state.prompt_method_three = None
    state.que_response_gen_three = False
    state.response_method_three = None

    return state
