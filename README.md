

# Wallpaper Scraper using Scrapy

This is a Scrapy project designed to scrape wallpapers and their associated tags from the website "https://wallpaper.mob.org/". The spider crawls through different categories of wallpapers, collects image URLs and their corresponding tags, and then stores the data in a JSON file.

## Installation

1. Make sure you have Python installed (https://www.python.org/downloads/).
2. Install Scrapy using pip:

```bash
pip install scrapy
```

## Usage

1. Clone the repository or download the source code:

```bash
git clone https://github.com/raoumairwaheed/Wallpaper-Crawler-using-Scrapy
```
2. Run the Spider:

```bash
scrapy crawl wallpaper
```

3. The spider will start crawling the website and gather wallpapers with their tags. The progress and logs will be displayed in the terminal.

4. Once the spider completes the crawling process, the data will be saved to a JSON file named "categories_data.json" in the same directory as the spider.

## Spider Explanation

The Spider `WallpaperSpider` is defined in the `wallpaper.py` file.

### Configuration

- `name`: The name of the spider. In this case, it is set to "wallpaper".
- `allowed_domains`: A list of domain names that the spider is allowed to crawl. The spider will only crawl URLs from these domains.
- `start_urls`: A list of URLs where the spider will begin crawling.

### Spider Logic

1. The spider starts by making requests to the URLs in the `start_urls` list and initiates the parsing process by calling the `parse` method.

2. The `parse` method extracts different wallpaper categories from the website and then iterates through each category to gather images and tags.

3. For each category, the spider sends requests to the category URLs with increasing page numbers to gather more images and tags. The `parse_categories` method handles the response from these requests.

4. The collected data is stored in the `self.categories_data` dictionary, where the keys are the categories, and the values are lists of dictionaries containing the image URL and tags.

5. Once the spider has finished crawling all the categories and pages, the `closed` method is called. This method writes the collected data to the "categories_data.json" file in JSON format.

## Customization

- To adjust the number of categories or pages to scrape, you can modify the `range` parameters in the `start_requests` and `parse_categories` methods.
- You can customize the output filename or file format by modifying the `closed` method.
- If the website structure or CSS selectors change, you may need to update the parsing logic accordingly.
