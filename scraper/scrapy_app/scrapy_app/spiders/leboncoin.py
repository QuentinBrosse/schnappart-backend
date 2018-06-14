import json
from datetime import datetime
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

    current_page = 1
    max_page = 2

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
            yield response.follow(article_href, self.parse_article)

        # Follow pagination (max=2)
        if self.current_page <= self.max_page:
            for pagination_href in response.css('#next::attr(href)'):
                self.current_page += 1
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
            'price': article['price'][0],
            'charges_included': LeboncoinSpider.get_attribute(
                article, 'charges_included', lambda x: bool(int(x))),
            'publication_date': datetime.strptime(
                article['first_publication_date'], '%Y-%m-%d %H:%M:%S'),
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
