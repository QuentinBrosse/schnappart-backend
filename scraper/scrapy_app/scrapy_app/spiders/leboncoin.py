import json
from datetime import datetime
import pytz
import scrapy
from scrapy.exceptions import CloseSpider


class LeboncoinSpider(scrapy.Spider):
    """
    Spider for a leboncoin search.
    Args:
        - url(string): The url of the search.
    """

    name = "leboncoin"

    search_id = None
    search_url = None
    start_urls = []

    nbr_of_pages = 2

    DEBUG_max_items = None

    def __init__(self, search_url=None, search_id=None, *args, **kwargs):
        super(LeboncoinSpider, self).__init__(*args, **kwargs)
        if not search_url:
            raise CloseSpider(reason='`search_url` argument is required.')
        if not search_id:
            raise CloseSpider(reason='`search_id` argument is required.')
        self.search_id = int(search_id)
        self.start_urls = [search_url]

    def parse(self, response):
        # Follow articles links
        for article_href in response.css('.tabsContent ul > li a::attr(href)'):
            if self.DEBUG_max_items:
                self.DEBUG_max_items -= 1
                if self.DEBUG_max_items <= 0:
                    break
            yield response.follow(article_href, self.parse_article)

        # Follow pagination (max=2)
        if self.nbr_of_pages <= 0:
            for pagination_href in response.css('#next::attr(href)'):
                self.nbr_of_pages -= 1
                yield response.follow(pagination_href, self.parse)

    def parse_article(self, response):
        flux_state_script = response \
            .xpath("//script[contains(., 'window.FLUX_STATE')]/text()")

        if not flux_state_script:
            raise CloseSpider(reason='FLUX_STATE not found')

        flux_state_json = flux_state_script.extract_first()[20:]
        flux_state = json.loads(flux_state_json)
        article = flux_state['adview']

        yield {
            'search': self.search_id,
            'url': article['url'],
            'original_id': article['list_id'],
            'title': article['subject'],
            'description': article['body'],
            'price': article['price'][0],
            'charges_included': LeboncoinSpider.get_attribute(
                article, 'charges_included', lambda x: bool(int(x))),
            'publication_date': self.get_publication_date(article),
            'real_estate_type': LeboncoinSpider.get_attribute(
                article, 'real_estate_type', None, None, True),
            'rooms': LeboncoinSpider.get_attribute(
                article, 'rooms', int),
            'furnished': LeboncoinSpider.get_attribute(
                article, 'furnished', lambda x: bool(int(x))),
            'surface': LeboncoinSpider.get_attribute(
                article, 'square', int),
            'images': LeboncoinSpider.get_images(article),
            'zipcode': article['location']['zipcode'],
            'city': article['location']['city'],
            'ges': LeboncoinSpider.get_attribute(
                article, 'ges'),
            'energy_rate': LeboncoinSpider.get_attribute(
                article, 'energy_rate'),
        }

    @staticmethod
    def get_attribute(article, attribute_key, transformator=None,
                      default=None, attribute_label=False):
        attributes = article.get('attributes', {})
        attribute = list(filter(
            lambda x: x['key'] == attribute_key,
            attributes,
        ))
        if not attribute:
            return default
        value = attribute[0]['value_label' if attribute_label else 'value']
        if transformator:
            return transformator(value)
        return value

    @staticmethod
    def get_images(article):
        images = article['images']
        if images['nb_images'] > 0:
            return images['urls_large']
        return []
    
    @staticmethod
    def get_publication_date(article):
        date = datetime.strptime(
            article['first_publication_date'],
            '%Y-%m-%d %H:%M:%S'
        )
        return pytz.timezone('Europe/Paris').localize(date, is_dst=None)
