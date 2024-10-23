import xkcdpass.xkcd_password as xp

words = xp.locate_wordfile()
mywords = xp.generate_wordlist(wordfile=words, min_length=3, max_length=8)


def generate_unique_id():
    return xp.generate_xkcdpassword(mywords, numwords=4, delimiter="-")
