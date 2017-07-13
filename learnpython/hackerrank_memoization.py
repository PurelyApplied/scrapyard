#!/usr/bin/env python3

"""PEP-8 refactoring of code, original post:
https://www.reddit.com/r/learnpython/comments/6mv1qv/how_can_memoization_be_applied_to_this_problem/"""


def password_cracker(attempt, lst, dct, result_list, memo_list):
    if dct == {}:
        for l in lst:
            # ex: convert ["because", "can", "do", "must", "we", "what"] to dictionary
            if l not in dct:
                dct[l] = 1
    # ex: check if "wedowhatwemustbecausewecan" and then if ex: "dowhatwemustbecausewecan" is in dct
    if attempt in dct:
        result_list.append(attempt)
        return result_list

    # go through each char in "attempt" and see if the substring is in dct
    # ex: start with "w", then "we". Since "we" is in dct, start with "d" then "do", ...
    res = attempt[0]
    for i in range(0, len(attempt)):
        if res in dct:
            # since "we" is in dct, start with "d"
            attempt = attempt[i + 1:]
            result_list.append(res)
            # every char in "attempt" was in dct, so return
            if attempt == "":
                return result_list
            else:
                return password_cracker(attempt, lst, dct, result_list, memo_list)
        # start with "w". "w" is not in dct, so append "e" to it
        else:
            if i < len(attempt) - 1:
                res += attempt[i + 1]
    # check if substring with last char is in dct.
    # ex: check if "can" (last substring in "attempt") is in dct
    if res in dct:
        result_list.append(res)
    else:
        return ["WRONG", "PASSWORD"]


if __name__ == "__main__":
    T = int(input("Enter a number of tests: >> ").strip())
    attempts = []
    word_lists = []
    for ti in range(0, T):
        N = int(input("Enter a number of words that you're about to fill out.  Use forethought!  >> ").strip())
        # ex: ["because", "can", "do", "must", "we", "what"]
        word_lists.append(input("Enter a list of words, separated by spaces: >> ").split(" "))
        # ex: "wedowhatwemustbecausewecan"
        login_attempt = input("Enter an attempted password: >> ").strip()
        # ex: ["wedowhatwemustbecausewecan", "helloworld", "abcd"]
        attempts.append(login_attempt)

    for i in range(0, len(attempts)):
        result_list = []
        memo_list = []
        password_dict = {}
        w = ""

        for word in password_cracker(attempts[i], word_lists[i], password_dict, result_list, memo_list):
            w += word
            w += " "
        print(w)
