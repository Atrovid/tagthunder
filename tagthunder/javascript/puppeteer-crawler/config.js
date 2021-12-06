"use strict"

exports.proxy_address = ('http_proxy' in process.env ? process.env["http_proxy"] : "");
exports.dir_cache_path = ("puppeteer_crawler_data" in process.env ? process.env["puppeteer_crawler_data"] : "/tmp/");

