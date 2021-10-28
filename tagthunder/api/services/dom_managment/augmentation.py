import webcrawler.wrapper
import api.configurations.api as api_settings

get_augmented_html = webcrawler.wrapper.HTMLAugmentedRequester(api_settings.settings.crawler_address)