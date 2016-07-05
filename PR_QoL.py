print("Quality of life loading...")

import os
import sys
from pprint import pprint
import inspect

def my_repr(x):
    if x == None:
        return None
    if hasattr(x, "__call__"):
        help(x)
        print("-----\n")
    pprint(x)
sys.displayhook = my_repr

cd = os.chdir

class PWD:
    def __init__(self):
        pass
    def __repr__(self):
        return os.getcwd()
pwd = PWD()

class LS:
    def __init__(self):
        pass
    def __repr__(self):
        return "\n".join(sorted(os.listdir()))
ls = LS()

def _get_signature_as_string(f):
    sig = inspect.signature(f)
    params = sig.parameters
    name = f.__name__
    indent = len(name) + 1
    sig_str = "{}({})".format(
        name,
        (",\n" + " " * indent).join(
            "{}{}{}".format(p.name,
                            " : {}".format(p.annotation) if p.annotation != inspect._empty else "",
                            " = {}".format(p.default) if p.default != inspect._empty else "")
            for p in params.values())
        )
    return sig_str

def explicit(f):
    '''Enforces strong typing, using a function's __annotation__'''
    def wrapper(*args, **kwargs):
        arg_names = list(inspect.signature(f).parameters)
        reqs = f.__annotations__
        for i in range(len(args)):
            name = arg_names[i]
            #print("Arg name:", name)
            #print("Name in req? ", name in reqs)
            #print("Type of arg:", type(args[i]))
            #print("Required:", reqs.get(arg_names[i], None))
            assert not name in reqs or type(args[i]) == reqs[arg_names[i]], (
                "Argument {} of type {}; type {} required by @explicit.".format(
                    name, type(args[i]), reqs[arg_names[i]])
            )
        for name, value in kwargs.items():
            assert not name in reqs or type(value) == reqs[name], (
                "Argument {} of type {}; type {} required by @explicit.".format(
                    name, type(value), reqs[name])
            )
        r = f(*args, **kwargs)
        if "return" in reqs:
            assert type(r) == reqs["return"], (
                "Return value of type {}; type {} required by @explicit.".format(
                    type(r), reqs["return"] ) )
        return r
    wrapper.__name__ = f.__name__
    wrapper.__doc__ = "This function enforces explicit adherance to this signature:\n\n"
    wrapper.__doc__ += _get_signature_as_string(f) + "\n\n"
    if f.__doc__:
        wrapper.__doc__ += "Function docstring:\n" + f.__doc__
    return wrapper

def implicit(f):
    '''Enforces implicit casting to type provided by a function's annotation'''
    def wrapper(*args, **kwargs):
        arg_names = list(inspect.signature(f).parameters)
        reqs = f.__annotations__
        new_kwargs = {}
        #print("Arg name:", name)
        #print("Name in req? ", name in reqs)
        #print("Type of arg:", type(args[i]))
        #print("Required:", reqs.get(arg_names[i], None))
        print("A:", args, "K:", kwargs)
        new_kwargs = {
            arg_names[i] : args[i]
            if not arg_names[i] in reqs
            else reqs[arg_names[i]](args[i])
            for i in range(len(args))
        }
        new_kwargs.update({
            name : value
            if not name in reqs
            else reqs[name](value)
            for name, value in kwargs.items()
        })
        print("NK:", new_kwargs)
        r = f(**new_kwargs)
        if "return" in reqs:
            assert type(r) == reqs["return"], (
                "Return value of type {}; type {} required by @explicit.".format(
                    type(r), reqs["return"] ) )
        return r

    wrapper.__name__ = f.__name__
    wrapper.__doc__ = "This function enforces explicit adherance to this signature:\n\n"
    wrapper.__doc__ += _get_signature_as_string(f) + "\n\n"
    if f.__doc__:
        wrapper.__doc__ += "Function docstring:\n" + f.__doc__
    return wrapper

# This fails with *Args
@explicit
def test(w, x:int, y:str = "butts", z=10, *args, **kwargs) -> str:
    '''This is test's docstring'''
    print("In test: x", x, "y", y, "z", z)
    print("args:", args)
    print("kwargs:", kwargs)
    return "returned value"

# This fails with the args:
@implicit
def test2(x:int, *args):
    '''You're a butt'''
    print("Type:", type(x))
    print("Test A:", args)
    pass
