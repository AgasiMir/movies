from uuid import uuid4
from unidecode import unidecode
from django.utils.text import slugify


def unique_slugify(instance, name):
    """
    Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
    """

    model = instance.__class__
    unique_slug = slugify(unidecode(name))

    while model.objects.filter(url=unique_slug).exists():
        unique_slug = f"{unique_slug} - {uuid4().hex[:8]}"

    return unique_slug
