BOT_NAME = 'web_standards_watch'
SPIDER_MODULES = ['standards_watch.spiders']
NEWSPIDER_MODULE = 'standards_watch.spiders'
ROBOTSTXT_OBEY = True
USER_AGENT = 'WebStandardsWatch/1.0 (educational catalog reader)'
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
FEED_EXPORT_ENCODING = 'utf-8'
TELNETCONSOLE_ENABLED = False
ITEM_PIPELINES = {'standards_watch.pipelines.StatusSummaryPipeline': 300}
FEEDS = {
    'results/standards_%(time)s.csv': {
        'format': 'csv',
        'fields': ['identifier', 'name', 'status', 'url', 'published'],
        'overwrite': True,
    },
}
