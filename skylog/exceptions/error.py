import random


def random_error():
    """Errors to choose from

    :return: string
    """

    e = []
    e.append('Help! Something went wrong')
    e.append('No.')
    e.append('No')
    e.append('...')
    e.append('. . .')
    e.append('um')
    e.append('hm')
    e.append('Stackoverflow it is')
    e.append('um....')
    e.append('Wow, how did you break this?')
    e.append("Uhm, that's interesting")
    e.append("Hm, that's interesting")
    e.append('Something broke')
    e.append("Let's see what Google has")
    e.append("We might need to look on Google to see what happened")

    rand = random.choice(range(0, len(e)))
    choice = e[rand]

    return choice


def really_bad_error():
    """Errors to choose from

    :return: string
    """

    e = []
    e.append('You really smoked the pan on this')
    e.append("This is the worst I've ever seen")
    e.append("You've screwed the pooch")

    rand = random.choice(range(0, len(e)))
    choice = e[rand]

    return choice
