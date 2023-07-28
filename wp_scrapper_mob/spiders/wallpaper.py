# pipelines.py
# Remove the JsonWriterPipeline class

# settings.py


# spider.py
import scrapy

class WallpaperItem(scrapy.Item):
    category = scrapy.Field()
    image_url = scrapy.Field()
    tags = scrapy.Field()

class WallpaperSpider(scrapy.Spider):
    name = "wallpaper"
    allowed_domains = ["wallpaper.mob.org"]
    start_urls = ["https://wallpaper.mob.org/"]

    def start_requests(self):
        for i in range(200):
            url = "https://wallpaper.mob.org/best/{}/".format(i)
            yield scrapy.Request(url=url, method='POST', callback=self.parse)

    def parse(self, response):
        wallpaper_header = response.css(".tag-mini-widgets")

        for single_widget in wallpaper_header:
            categories = single_widget.css(".tag-mini-widget__title .tag-mini-widget__title-wrap::text").extract()
            for category in categories:
                category = category.strip()

                for page in range(1, 200):
                    category_url = "https://wallpaper.mob.org/gallery/tag={}/{}/".format(category.lower(), page)
                    yield scrapy.Request(url=category_url, method='POST', callback=self.parse_categories,
                                         meta={"category": category, "page": page})

    def parse_categories(self, response):
        crawled_category = response.meta['category']
        image_listing = response.css('.image-gallery-image')

        for img in image_listing:
            images_url = img.css(".image-gallery-image__inner .image-gallery-image__image::attr(src)").get()
            images_tags = img.css('.image-gallery-image__tags li a::text').getall()

            wallpaper_item = WallpaperItem(category=crawled_category, image_url=images_url, tags=images_tags)
            yield wallpaper_item
