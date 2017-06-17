#!/usr/bin/env python3

# Written for https://www.reddit.com/r/learnpython/comments/6hoo84/writing_a_generator_that_can_be_called_like_a/

from functools import wraps


def every_n_generator(n):
    i = 0
    while True:
        yield True if i % n == 0 else False
        i += 1


def use_a_generator():
    bad_control_pattern = 10
    for x in every_n_generator(3):
        print(x)
        bad_control_pattern -= 1
        if bad_control_pattern == 0:
            break


def generator_functionifier(g):
    @wraps(g)
    def functionized_generator(*args, **kwargs):
        instantiated_generator = g(*args, **kwargs)
        return instantiated_generator.next
    return functionized_generator


@generator_functionifier
def decorated_every_n_generator(n):
    i = 0
    while True:
        yield True if i % n == 0 else False
        i += 1


def use_as_a_function():
    functionized_generator = decorated_every_n_generator(3)
    for _ in range(10):
        print(functionized_generator())


if __name__ == "__main__" or True:
    print("Use case 1:")
    use_a_generator()
    print("Use case 2:")
    use_as_a_function()
