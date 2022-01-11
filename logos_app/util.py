def is_author(user):
    return user.groups.filter(name='author').exists()


def is_editor(user):
    return user.groups.filter(name='editor').exists()


def is_reviewer(user):
    return user.groups.filter(name='reviewer').exists()
