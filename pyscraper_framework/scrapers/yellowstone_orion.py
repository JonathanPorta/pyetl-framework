from lib import Scraper as Scraper

class YellowstoneOrion(Scraper):
    def __init__(self, scraper_manager, name, job_class):
        print("YellowstoneOrion::init()")

        super().__init__(scraper_manager, name, job_class)
        self.scraper_manager = scraper_manager
        self.name = name

    def start(self, queue):
        print("YellowstoneOrion::start()",queue)
        super().start(queue)
        print("Init a new job")
        scrape_job = self.init_job(url='http://google.com')
        print("Made a scrape_job, son: ", scrape_job)
        print("scrape_job has url: {}".format(scrape_job.url))
        queued_job = queue.enqueue_call(
            func=scrape_job.execute, result_ttl=5000
        )
        job_id = queued_job.get_id()
        print("Job was fucking queued, asshole", job_id)
