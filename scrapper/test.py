from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Import your spider class
from pakwheels.spiders.pak import PakSpider

# Create a Scrapy process
process = CrawlerProcess(get_project_settings())

# Add your spider to the process
process.crawl(PakSpider)

# Start the process (blocking)
process.start()
