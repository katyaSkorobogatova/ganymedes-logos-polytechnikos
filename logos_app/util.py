def is_author(user):
    return user.groups.filter(name='author').exists()