import config

def is_owner(user):
    return user.id == config.OWNER_ID
