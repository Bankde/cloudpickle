from cloudpickle.cloudpickle import *  # noqa
from cloudpickle.cloudpickle_fast import CloudPickler, dumps, dump  # noqa

# Conform to the convention used by python serialization libraries, which
# expose their Pickler subclass at top-level under the  "Pickler" name.
Pickler = CloudPickler

__version__ = '2.2.1'

import builtins
import types
builtin_exec = builtins.exec
def new_exec(*args, **kwargs):
    glob = None
    loc = None
    src = args[0]
    if "locals" in kwargs:
        loc = kwargs["locals"]
    elif len(args) >= 3:
        loc = args[2]
    if "globals" in kwargs:
        glob = kwargs["globals"]
    elif len(args) >= 2:
        glob = args[1]

    if isinstance(src, types.CodeType) or (glob == None and loc == None):
        # nothing is provided, this case won't be a problem
        builtin_exec(*args, **kwargs)
        return None
    elif glob and (loc == None):
        # locals is not provided
        # save pre-exec glob, exec, put code-cache on any new glob variables.
        pre_glob = glob.copy()
        builtin_exec(*args, **kwargs)
        for v in glob:
            if v not in pre_glob:
                # It just an improvement caching, if we fail, just skip.
                try:
                    glob[v].__codepickle_src__ = src
                except:
                    pass
        return None
    else:
        # locals is provided
        # save pre-exec loc, exec, put code-cache on any new loc variables.
        pre_loc = loc.copy()
        builtin_exec(*args, **kwargs)
        for v in loc:
            if v not in pre_loc:
                try:
                    loc[v].__codepickle_src__ = src
                except:
                    pass
        return None
builtins.exec = new_exec
