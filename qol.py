'''My Quality of Life changes.  Includes:
* an improved repr that prints help on callables.
* * Usage: set 'sys.displayhook = qol.repr'
* 'pwd', 'cd', and 'ls' functionality.
* Includes decorators:
* * @twyn "take what you need": selective **kwargs usage
* * @implicit and @explicit for casting / type checking using
    annotations.

Because decorators mask the inspect signature, they must be called
first, before other decorators.

Both @implicit and @explicit are somewhat counter to the Python
philosophy, but were useful in teaching myself about decorators.

'''

import os
import sys
import inspect
from pprint import pprint
from functools import wraps

#####
# A better repr; repr(callable) calls help(callable)
def repr(x):
    if x == None:
        return None
    if hasattr(x, "__call__"):
        help(x)
        print("-----\n")
    pprint(x)

#####
# 'cd', 'pwd', and 'ls' functionality.
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

#####
# Decorators:
def twyn(f):
    '''Take What You Need **kwargs handler.  Ignores those items passed
    via **kwargs that do not fit a functions signature.

    '''
   
    f_args, keywords = inspect.getfullargspec(f)[0:3:2]
    ## If you accept **kwargs, pass everything
    if not (keywords is None):
       return f
    # Otherwise, only pass those that are needed
    @wraps(f)
    def wrapper(*args, **kwargs):
        r = f(*args, **{k : kwargs[k] for k in kwargs if k in f_args})
        return r
    return wrapper
        

class ExplicitError(Exception):
    pass

def explicit(f):
    '''Enforces strong typing, according to function's annotation.  *args
    and **kwargs ignored.'''
    # (f_args, f_vargs, f_kwargs, defaults,
    #  kwonlyargs, kwonlydefs, annotations) = inspect.getfullargspec(f)
    arg_names, req_type = inspect.getfullargspec(f)[0:7:6]
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Check required arguments
        for i in range(min(len(args), len(arg_names))):
            name = arg_names[i]
            if not name in req_type:
                continue
            required = req_type[name]
            is_match = isinstance(args[i], required)
            actual = type(args[i])
            if not is_match:
                raise ExplicitError("Argument '{}' of type '{}'; type '{}'"
                                    " required by @explicit.".format(
                                        name,
                                        actual.__name__, required.__name__))
        # Check if arguments were passed via **kwargs
        for name, value in kwargs.items():
            if not name in req_type:
                continue
            required = req_type[name]
            is_match = isinstance(value, required)
            actual = type(value)
            if not is_match:
                raise ExplicitError("Argument '{}' of type '{}'; type '{}'"
                                    " required by @explicit.".format(
                                        name,
                                        actual.__name__, required.__name__))
        r = f(*args, **kwargs)
        # Check return value
        if "return" in req_type and not isinstance(r, req_type["return"]):
            raise ExplicitError("Return value of type '{}'; type '{}'"
                                " required by @explicit.".format(
                                    actual.__name__, required.__name__))
        return r
    wrapper.__doc__ += (
        "\n\nThis function requires explicit aderence to the annotated typing.")
    return wrapper


# This needs updating
def implicit(f):
   @wraps(f)
   def wrapper(*args, **kwargs):
        arg_names = list(inspect.signature(f).parameters)
        reqs = f.__annotations__
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
        r = f(**new_kwargs)
        if "return" in reqs:
            assert type(r) == reqs["return"], (
               "Return value of type {}; type {}"
               " required by @explicit.".format(
                  type(r), reqs["return"] ) )
        return r
   wrapper.__doc__ += (
      "\n\nThis function casts to aderence to the annotated typing.")
   return wrapper


#####
# Some test functions

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


#@twyn
def test3(a:int, b, c, d=4, **kwargs):
    '''A docstring!'''
    print("Got some args!")
    print(a, b, c, d)
    print(kwargs)
