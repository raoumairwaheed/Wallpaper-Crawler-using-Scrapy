import scrapy
import json


class WallpaperSpider(scrapy.Spider):
    name = "wallpaper"
    allowed_domains = ["wallpaper.mob.org"]
    start_urls = ["https://wallpaper.mob.org/"]

    def __init__(self, *args, **kwargs):
        super(WallpaperSpider, self).__init__(*args, **kwargs)
        self.categories_data = {}

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
                self.categories_data.setdefault(category, [])
                for page in range(1, 200):
                    category_url = "https://wallpaper.mob.org/gallery/tag={}/{}/".format(category.lower(), page)
                    yield scrapy.Request(url=category_url, method='POST', callback=self.parse_categories,
                                         meta={"category": category, "page": page})

    def parse_categories(self, response):
        crawled_category = response.meta['category']
        page = response.meta['page']
        image_listing = response.css('.image-gallery-image');
        images_urls = []
        for img in image_listing:
            images_url = img.css(".image-gallery-image__inner .image-gallery-image__image::attr(src)").extract()
            images_tags =img.css('.image-gallery-image__tags li a::text').extract();

            print(crawled_category, images_url, images_tags)
            images_urls.append({"image":images_url[0], "tags":images_tags})

        self.categories_data[crawled_category].extend(images_urls)
        new_categories_tags = response.css(".tag-mini-widget__title-wrap::text").extract()
        for category in new_categories_tags:
            category = category.strip()
            self.categories_data.setdefault(category, [])
            for page in range(1, 200):
                category_url = "https://wallpaper.mob.org/gallery/tag={}/{}/".format(category.lower(), page)
                yield scrapy.Request(url=category_url, method='POST', callback=self.parse_categories,
                                     meta={"category": category, "page": page})

    def closed(self, reason):
        output_data = json.dumps(self.categories_data, indent=4)

        with open("categories_data.json", "w") as file:
            file.write(output_data)


# image-gallery-image__tags_hidden