BOT_NAME = 'hsbc_tr'
SPIDER_MODULES = ['hsbc_tr.spiders']
NEWSPIDER_MODULE = 'hsbc_tr.spiders'
ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'
ITEM_PIPELINES = {
   'hsbc_tr.pipelines.DatabasePipeline': 300,
}
