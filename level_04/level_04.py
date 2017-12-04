#!/usr/bin/env python

from collections import defaultdict


def list_has_anagrams(toinspect):
    if __debug__:
        print("Gonna inspect the following list: ")
        for iter in range(0, len(toinspect) - 1):
            for other in range(iter + 1, len(toinspect)):
                if __debug__: print("Comparing {} == {}".format(toinspect[iter], toinspect[other]))
                if sorted(toinspect[iter]) == sorted(toinspect[other]):
                    return True
    return False


with open('in.txt', 'r') as f:
    result1 = 0
    result2 = 0

    for line in f:
        skipline = False
        line = line.strip()

        if __debug__: print(line)

        aslist = list(line.split(" "))
        asset = set(aslist)

        if len(aslist) == len(asset):
            result1 += 1
        else:
            continue

        data = defaultdict(list)
        for item in asset:
            data[len(item)].append(item)

        if __debug__: print(data)

        for k, v in data.items():
            if len(data[k]) > 1:
                # find anagrams
                # if any found, continue to next line
                if list_has_anagrams(data[k]):
                    skipline = True
                    break
        if not skipline: result2 += 1

    print("result1: {}".format(result1))
    print("result2: {}".format(result2))

u"""
--- Day 4: High-Entropy Passphrases ---

A new system policy has been put in place that requires all accounts to use a passphrase instead of simply a password. A passphrase consists of a series of words (lowercase letters) separated by spaces.

To ensure security, a valid passphrase must contain no duplicate words.

For example:

    aa bb cc dd ee is valid.
    aa bb cc dd aa is not valid - the word aa appears more than once.
    aa bb cc dd aaa is valid - aa and aaa count as different words.

The system's full passphrase list is available as your puzzle input. How many passphrases are valid?

--- Part Two ---

For added security, yet another system policy has been put in place. Now, a valid passphrase must contain no two words that are anagrams of each other - that is, a passphrase is invalid if any word's letters can be rearranged to form any other word in the passphrase.

For example:

    abcde fghij is a valid passphrase.
    abcde xyz ecdab is not valid - the letters from the third word can be rearranged to form the first word.
    a ab abc abd abf abj is a valid passphrase, because all letters need to be used when forming another word.
    iiii oiii ooii oooi oooo is valid.
    oiii ioii iioi iiio is not valid - any of these words can be rearranged to form any other word.

Under this new system policy, how many passphrases are valid?

"""
