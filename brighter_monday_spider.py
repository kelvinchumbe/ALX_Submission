import scrapy
from scrapy.http import HtmlResponse

class BrighterMonday(scrapy.Spider):
    name = "brighter_monday_spider"
    # allowed_domains = ['https://brightermonday.co.ke']
    start_urls = ['https://brightermonday.co.ke/jobs']


    def parse(self, response):
        # Get the no. of jobs currently posted
        no_of_jobs = response.css('div.customer-card-edit-wrapper.card--compact > div > div > h2 > span > strong::text').get()

        # Get all job cards so we can loop through each card individually
        jobs = response.css('article').getall()

        # Loop through each job card to extract the title, url, organization, function and description
        for job in jobs:
            new_response = HtmlResponse(url=response.url, body=job, encoding='utf-8')
            job_title = new_response.css('header > div > div:nth-child(1) > div:nth-child(1) > a > h3::text').get()

            job_url = new_response.css('header > div > div:nth-child(1) > div:nth-child(1) > a::attr(href)').get()

            organization = new_response.css('header > div > div:nth-child(2) > a::text').get() if new_response.css('header > div > div:nth-child(2)::text').get() is None else new_response.css('header > div > div:nth-child(2)::text').get()

            job_function = new_response.css('header > div > div:nth-child(4) > div > div > div > div:nth-child(1) > span::text').get()

            job_description = new_response.css('div > a > div:nth-child(1) > p::text').get()

            # Store the information in a dictionary
            yield dict(title=job_title, organization=organization, function=job_function, description=job_description, url=job_url)

        # Get the url of the next page 
        next_page = response.css('ul.pagination > li:nth-child(15) > a::attr(href)').get()

        # Follow the url of the next page
        yield scrapy.Request(url=next_page, callback=self.parse)
        
# Run the script with the command below to scrap the brighter monday website and store jobs in a csv file:
#    > scrapy crawl brighter_monday_spider -o brighter_monday_jobs.csv 
    
