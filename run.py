import streamlit
import pandas as pd
import streamlit.web.cli as stcli
import os, sys
import networkx as nx
from datetime import datetime
import streamlit.runtime.scriptrunner.magic_funcs


def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path


if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("script.py"),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())