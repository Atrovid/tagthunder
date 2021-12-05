"use strict"

const puppeteer = require('puppeteer');



async function goto(browser, url, w, h){
    let page = await browser.newPage();
    await page.setViewport({width: w, height: h});
    await page.setCacheEnabled(false);
    await page.goto(url, {waitUntil: "domcontentloaded"});
    console.log(`[*] ${url} opened`);
    return page;
}




exports.goto = goto;
