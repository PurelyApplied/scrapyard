#!/usr/bin/env python3

"""My solution to the problem discussed in:
https://www.reddit.com/r/learnpython/comments/6mv1qv/how_can_memoization_be_applied_to_this_problem/
and originally proposed in:
https://www.hackerrank.com/challenges/password-cracker/problem"""


# Tests could themselves ju
from functools import lru_cache


def get_example():
    return ((("because", "can", "do", "must", "we", "what"), "wedowhatwemustbecausewecan"),
            (("hello", "planet"), "helloworld"),
            (("ab", "abcd",  "cd"), "abcd"))


def condescendingly_get_input():
    input("Enter anything.  This line is ignored. >> ")
    input("This, too, will be ignored.  See if I care. >> ")
    things = []
    try:
        while True:
            passwords = input("Space separated passwords: ").split()
            attempt = input("Something to attempt: ")
            things.append((passwords, attempt))
    except Exception:
        return things

def main(tests):
    solutions = [check_password(*t) for t in tests]
    print("Begin solutions:\n\n    ")
    for s in solutions:
        if not s:
            print("WRONG PASSWORD")
        else:
            print(" ".join(s))


def check_password(password_list, password):
    """Returns a list of strings $R contained in $password_list such that "".join($R) = $password.
    If no such list exists, returns an empty list."""
    print("Password list: {}".format(password_list))
    print("Attempt: {}".format(password))
    attempt = recursive_step(password_list, password, [])
    return attempt if attempt is not None else []


# @lru_cache(maxsize=None)
def recursive_step(password_list, password, current):
    candidates = [p for p in password_list if password.startswith(p)]
    if not candidates:
        return None
    if candidates[0] == password:
        return current + [candidates[0]]
    for c in candidates:
        attempt = recursive_step(password_list, password[len(c):], current + [c])
        if attempt is not None:
            return attempt
    return None


if __name__ == "__main__":
    main(get_example())
