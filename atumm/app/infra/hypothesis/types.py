from string import ascii_lowercase, ascii_uppercase, digits

from hypothesis.strategies import composite, integers, text


@composite
def passwords(draw):
    length = draw(integers(min_value=8, max_value=20))
    password = draw(
        text(
            alphabet=ascii_uppercase + ascii_lowercase + digits,
            min_size=length,
            max_size=length,
        )
    )
    return password
