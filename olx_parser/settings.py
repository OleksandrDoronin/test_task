BOT_NAME = 'olx_parser'

SPIDER_MODULES = ['olx_parser.spiders']
NEWSPIDER_MODULE = 'olx_parser.spiders'


USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/110.0.0.0 Safari/537.36'
)

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'

DOWNLOAD_DELAY = 2
LOG_ENABLED = False
