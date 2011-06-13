from game import constants


def lighten(color):
    """Extremely simple color lightening algorithm that I guessed would work alright"""
    return tuple(min(c + 128, 255) for c in color)

def center(surf):
    return (constants.SCREEN_WIDTH / 2 - surf.get_width() / 2,
            constants.SCREEN_HEIGHT / 2 - surf.get_height() / 2)
