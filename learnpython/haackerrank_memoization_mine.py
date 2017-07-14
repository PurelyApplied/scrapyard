#!/usr/bin/env python3

"""My solution to the problem discussed in:
https://www.reddit.com/r/learnpython/comments/6mv1qv/how_can_memoization_be_applied_to_this_problem/
and originally proposed in:
https://www.hackerrank.com/challenges/password-cracker/problem"""


# Tests could themselves ju
def get_example():
    return ((("because", "can", "do", "must", "we", "what"), "wedowhatwemustbecausewecan"),
            (("hello", "planet"), "helloworld"),
            (("ab", "abcd", "cd"), "abcd"))


def main(tests):
    solutions = [check_password(*t) for t in tests]
    print("Begin solutions:\n\n    ")
    print("\n".join(" ".join(s) for s in solutions))


def check_password(password_list, password):
    """Returns a list of strings $R contained in $password_list such that "".join($R) = $password.
    If no such list exists, returns an empty list."""
    print("Password list: {}".format(password_list))
    print("Attempt: {}".format(password))
    return password_list


if __name__ == "__main__":
    main(get_example())
