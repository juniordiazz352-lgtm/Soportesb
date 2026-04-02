def is_staff(member, staff_role_id):
    return any(role.id == staff_role_id for role in member.roles)
