# -*- coding: utf-8 -*-

import os
import os.path

try:
    import pyotherside
except:
    print("no pyotherside module loaded")

def get_level_desc(path):
    return {"name": os.path.basename(path),
     "path": path,
    }

def get_levels(qtPath, documents):

    pyotherside.send('log', documents)

    #level_path = os.path.join(qtPath, "../content", "sgf")
    level_path = os.path.join(qtPath, "", "sgf")
    provided_levels = [get_level_desc(os.path.join(level_path, f)) for f in os.listdir(level_path)]

    return provided_levels

