"use strict"

exports.PROXY = ('http_proxy' in process.env ? process.env["http_proxy"] : "");
exports.HOST = "0.0.0.0";
exports.PORT = 8080;

exports.dir_cache_path = ("puppeteer_crawler_data" in process.env ? process.env["puppeteer_crawler_data"] : "/tmp/");
exports.cookieIgnorePath = `${process.cwd()}/extensions/cookieconsent`

