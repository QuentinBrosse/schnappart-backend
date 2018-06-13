from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start a scraping of all projects or of a specified one.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--project',
            dest='specific_project',
            nargs='?',
            type=int,
            help=(
                'The ID of a specific project to scrape.'
            )
        )

    def handle(self, *args, **options):
        self.stdout.write(str(options['specific_project'] or 'All'))
