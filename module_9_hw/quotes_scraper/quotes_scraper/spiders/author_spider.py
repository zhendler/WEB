import scrapy

class AuthorsSpider(scrapy.Spider):
    name = "authors"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css('div.quote'):
            author_url = quote.css('span a::attr(href)').get()
            yield response.follow(author_url, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        yield {
            'name': response.css('h3.author-title::text').get().strip(),
            'birthdate': response.css('span.author-born-date::text').get(),
            'location': response.css('span.author-born-location::text').get().replace('in ', ''),
        }
