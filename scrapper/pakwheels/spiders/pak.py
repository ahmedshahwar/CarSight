import scrapy
import re

class PakSpider(scrapy.Spider):
    name = 'pak'
    allowed_domains = ['pakwheels.com']
    # start_urls = ['https://www.pakwheels.com/used-cars/search/-/direct_1/']  # Managed by PakWheels
    start_urls = ['https://www.pakwheels.com/used-cars/search/-/']

    def parse(self, response):
        urls = response.xpath('//div[@class="search-title"]/a/@href').extract()
        for url in urls:
            comp_url = 'https://www.pakwheels.com' + url
            yield scrapy.Request(comp_url, callback=self.parse_car)

        # Next Page
        next_page = response.xpath('//li[@class="next_page"]/a/@href').extract_first()
        if next_page:
            comp_url = 'https://www.pakwheels.com' + next_page
            yield scrapy.Request(comp_url, callback=self.parse)

    def parse_car(self, response):
        # # Check if the page is managed by PakWheels
        # managed_by_pakwheels = response.xpath('//*[@id="scrollToFixed"]/div[2]/div[1]/div[1]/div/span/text()').extract_first()
        # if managed_by_pakwheels != 'Managed by PakWheels':
        #     return  # Skip processing this page if not managed by PakWheels
        
        # Assembly
        assembly = response.xpath('//*[@id="scroll_car_detail"]/li[6]/text()').extract_first()
        
        # Model Year
        year = int(response.xpath('//span[@class="engine-icon year"]/../p/a/text()').extract_first())
    
        # Check Assembly and Year
        if assembly.lower() == 'local' and year > 2012:
            # Ad Ref #
            ad_ref = response.xpath("//*[contains(text(),'Ad Ref #')]/following-sibling::li/text()").extract_first()
            
            # Last Updated
            last_updated = response.xpath("//*[contains(text(),'Last Updated')]/following-sibling::li/text()").extract_first()

            # Name tag of AD
            name = response.xpath('//h1/text()').extract_first()  

            # Mileage
            mileage_text = response.xpath('//span[@class="engine-icon millage"]/../p/text()').extract_first()
            mileage = int(mileage_text.replace('km','').replace(',','')) if mileage_text else None

            # Engine Capacity 
            capacity = response.xpath("//*[contains(text(),'Engine Capacity')]/following-sibling::li/text()").extract_first() 

            # Engine Type
            engine_type = response.xpath('//span[@class="engine-icon type"]/../p/a/text()').extract_first()

            # Registered City
            register_city = response.xpath('//*[@id="scroll_car_detail"]/li[2]/text()').extract_first() 

            # Transmission
            transmission = response.xpath('//span[@class="engine-icon transmission"]/../p/a/text()').extract_first()
            if not transmission:
                transmission = response.xpath('//span[@class="engine-icon transmission"]/../p/text()').extract_first()

            # Price
            price = response.xpath('//div[@class="price-box"]/strong/text()').extract_first()
            unit = response.xpath('//div[@class="price-box"]/strong/span/text()').extract_first()
            if unit == 'lacs':
                price = float(price.strip().split('PKR')[1]) * 100000 
            elif unit == 'crore':
                price = float(price.strip().split('PKR')[1]) * 10000000
            
            # Images
            # img_src_list = response.xpath('//*[@id="myCarousel"]//img/@data-original').extract()
            # imgs = ['\t'.join(re.match(r'(.*?\.webp)', img_src).group(1) for img_src in img_src_list if re.match(r'(.*?\.webp)',img_src))]

            yield {
                "Ad No": ad_ref,
                "Assembly": assembly,
                "Name": name,
                "Model Year": year,
                "Mileage": mileage,
                "Engine Capacity": capacity,
                "Engine Type": engine_type,
                "Registered City": register_city,
                "Transmission": transmission,
                "Price": price,
                "Last Updated": last_updated,
                # "Images": imgs
            }