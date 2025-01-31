from django.utils.crypto import get_random_string


def generate_slug(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + get_random_string(length=6)
    return unique_slug
