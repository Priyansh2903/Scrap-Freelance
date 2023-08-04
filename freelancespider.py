import scrapy

class FreelancespiderSpider(scrapy.Spider):
    name = "freelancespider"
    
    def __init__(self, skillset=None, min_price=None, *args, **kwargs):
        super(FreelancespiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            f'https://www.freelancer.com/jobs/{skillset.lower().replace(" ", "-")}/'
        ]
        self.min_price = min_price

    def parse(self, response):
        # Extracting each job card on the page
        job_cards = response.css("div.JobSearchCard-item-inner")

        for job_card in job_cards:
            # Extracting title, description, and price of each job
            title = job_card.css("a.JobSearchCard-primary-heading-link::text").get()
            description = job_card.css("div.JobSearchCard-primary-description::text").get()
            price = job_card.css("div.JobSearchCard-secondary-price span::text").get()

            if title and description and price:
                price = float(price.replace("$", "").replace(",", ""))
                if self.min_price is None or price >= self.min_price:
                    yield {
                        "Title": title.strip(),
                        "Description": description.strip(),
                        "Price": price,
                    }

      