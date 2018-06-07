from django.db import models
from django.conf import settings


class ImmoSource(models.Model):
    name = models.CharField(max_length=100)
    host_regex = models.CharField(
        max_length=100,
        help_text=(
            'The regex of the host who will be used to deduct '
            'the `ImmoSource` from the `Search.url`.'
        )
    )
    order_query_string = models.CharField(
        max_length=50,
        help_text=(
            'The query string to add to the `Search.url` '
            'to sort ascendingly the results by date.'
        )
    )

    def __str__(self):
        return self.name


class Search(models.Model):
    url = models.CharField(max_length=255)
    immo_source = models.ForeignKey(ImmoSource, on_delete=models.PROTECT)

    def __str__(self):
        return '{}: {}'.format(self.immo_source, self.url)


class Project(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '{} (by {})'.format(self.name, self.user)

