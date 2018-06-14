import time
import random
import requests
from django.core.management.base import BaseCommand
from api.models import SearchResult


class Command(BaseCommand):
    help = 'The the health of the scraped results.'

    def handle(self, *args, **options):
        search_results = SearchResult.objects.filter(alive=True)
        dead_count = 0

        self.stdout.write(
            '{} search results found. \n'
            .format(len(search_results)))

        for search_result in search_results:
            result = requests.get(search_result.url)
            if result.status_code != 200:
                dead_count += 1
                self.stdout.write(
                    'Search result #{} is dead 😢.'
                    .format(search_result.id))
                search_result.alive = False
                search_result.save()
            else:
                self.stdout.write(
                    'Search result #{} is alive 😀.'
                    .format(search_result.id))
            time.sleep(0.25 * random.uniform(0.3, 1.2))

        self.stdout.write(
            '\n{} search resuts are dead.'
            .format(dead_count))
