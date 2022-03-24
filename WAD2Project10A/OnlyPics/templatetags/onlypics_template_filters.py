from django import template

register = template.Library()

@register.filter
def picVoteValue(pictureVotes, picture):
    return pictureVotes.get(picture)
