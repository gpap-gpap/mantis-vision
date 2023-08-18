import streamlit as st
import subprocess
import sys
import os
import time

try:
    # replace "yourpackage" with the package you want to import
    import mantis.rock_physics.fluid as manFL

# This block executes only on the first run when your package isn't installed
except ModuleNotFoundError as e:
    st.write(f"worked to module not found {os.environ['git_token']}")
    subprocess.Popen(
        [
            f"{sys.executable} -m pip install git+https://${os.environ['git_token']}@github.com/gpap-gpap/anisotroPY.git"
        ],
        shell=True,
    )
    # wait for subprocess to install package before running your actual code below
    time.sleep(90)

# Rest of your code goes here
import mantis.rock_physics as manRP
import mantis.rock_physics.fluid as manFL

st.write(
    "Has environment variables been set:",
    os.environ["git_token"] == st.secrets["git_token"],
)
water = manFL.Fluid.from_presets(name="Water", temperature=52.0, pressure=16.0)
model = manRP.models(
    identifier="hudson",
    Vp=2.3,
    Vs=1.8,
    Rho=1.3,
    crack_density=0.01,
    aspect_ratio=1e-3,
    fluid=water,
)
st.write(model.Cij())
