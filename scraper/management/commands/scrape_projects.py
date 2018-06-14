import os
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from django.core.management.base import BaseCommand
from api.models import Project


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
        projects = self.get_projects(options)
        self.stdout.write('{} projects found.'.format(len(projects)))

        os.environ.setdefault(
            'SCRAPY_SETTINGS_MODULE',
            'scraper.scrapy_app.scrapy_app.settings'
        )

        settings = get_project_settings()
        settings['SPIDER_MODULES'] = ['scraper.scrapy_app.scrapy_app.spiders']
        settings['NEWSPIDER_MODULE'] = 'scraper.scrapy_app.scrapy_app.spiders'

        settings['ITEM_PIPELINES'] = {
            'scraper.scrapy_app.scrapy_app.pipelines.PersistencePipeline': 300,
        }

        process = CrawlerProcess(settings)

        for project in projects:
            for search in project.search_set.all():
                spider = search.immo_source.name.lower()

                self.stdout.write(
                    'Start crawl for project {} | search {}'
                    .format(project.id, search.id)
                )
                process.crawl(
                    spider,
                    search_id=search.id,
                    search_url=search.url
                )

        process.start(stop_after_crawl=True)

        self.stdout.write('All crawls are finished !')

    @staticmethod
    def get_projects(options):
        """
        Get projects in DB.
        """
        if options['specific_project']:
            return [Project.objects.get(pk=options['specific_project'])]
        return Project.objects.all()
