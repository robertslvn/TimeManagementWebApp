from django import template
register = template.Library()


@register.filter
def isFriend(user1, user2):
    return user1.isFriend(user2)

@register.filter
def isAdmin(group, user):
    return group.isAdmin(user)

@register.filter
def isOwner(group, user):
    return group.isOwner(user)

@register.simple_tag
def hasHigherPrivileges(group, user1, user2):
    return group.hasHigherPrivileges(user1, user2)