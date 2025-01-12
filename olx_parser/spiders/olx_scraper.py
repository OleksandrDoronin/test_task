import scrapy

from core.repositories.postgres_base import init_db
from core.repositories.products import get_olx_data_repository
from core.schemas.products import OlxDataBase


class OlxSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ['olx.ua']
    start_urls = ['https://www.olx.ua/uk/list/']
    page = 1

    def __init__(self, *args, **kwargs):
        super(OlxSpider, self).__init__(*args, **kwargs)
        init_db()
        self.olx_data_repository = get_olx_data_repository()

    def parse(self, response):  # noqa
        links = response.xpath('//a[contains(@class, "css-qo0cxu")]/@href').getall()

        for link in links:
            absolute_url = response.urljoin(link)
            yield response.follow(
                absolute_url,
                callback=self.parse_product_details,
                meta={'product_url': absolute_url},
            )

        if self.page < 5:
            next_page = self.get_next_page_url()
            yield response.follow(next_page, callback=self.parse)

    def get_next_page_url(self):
        """Returns the URL of the next page."""

        self.page += 1
        return f'https://www.olx.ua/uk/list/?page={self.page}'

    def parse_product_details(self, response):
        """Retrieves data from the ad page."""

        product_data = self.extract_product_data(response=response)

        olx_data = self.create_olx_data(product_data=product_data)

        self.olx_data_repository.add_product(product_data=olx_data)

        yield product_data

    def extract_product_data(self, response):
        """Extracts data from the HTML page of the ad."""

        title = response.css('h4.css-1kc83jo::text').get()
        image_urls = response.xpath(
            '//div[contains(@class, "swiper-zoom-container")]/img/@src'
        ).getall()
        created_at = response.css('span.css-1ycin span.css-19yf5ek::text').get()
        price = self.extract_price(response)
        details = response.css('ul.css-rn93um li.css-1r0si1e p::text').getall()
        description = '\n'.join(
            response.css('div[data-cy="ad_description"] div.css-1o924a9::text').getall()
        )
        product_id = response.css('span.css-12hdxwj::text').re_first(r'\d+')
        username = response.css('h4.css-1lcz6o7::text').get()
        registration_date = response.css('p.css-23d1vy span::text').get()
        last_seen = response.css('p.css-r1ai8x span::text').get()
        product_url = response.meta.get('product_url')

        return {
            'title': title,
            'image_urls': image_urls,
            'created_at': created_at,
            'price': price,
            'details': details,
            'description': description,
            'product_id': product_id,
            'username': username,
            'registration_date': registration_date,
            'last_seen': last_seen,
            'url': product_url,
        }

    @staticmethod
    def extract_price(response):
        """Retrieves the price from the ad page."""

        price = response.css('h3.css-90xrc0::text').get()
        if not price:
            price = response.css('p[data-testid="ad-price"]::text').get()
        if not price:
            price = 'Не вказано'
        elif price.strip().lower() == 'безкоштовно':
            price = 'Безкоштовно'
        return price

    @staticmethod
    def create_olx_data(product_data):
        """Creates an OlxDataBase object from the extracted data."""

        return OlxDataBase(
            seller_name=product_data['username'],
            registration_date=product_data['registration_date'],
            last_login=product_data['last_seen'],
            url=product_data['url'],
            title=product_data['title'],
            image_urls=product_data['image_urls'],
            price=product_data['price'],
            created_at=product_data['created_at'],
            attributes=product_data['details'],
            description=product_data['description'],
            product_id=product_data['product_id'],
        )
