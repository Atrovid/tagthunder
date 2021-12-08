"use strict"

const puppeteer = require('puppeteer');
const htmlAugmentation = require('html-augmentation');
const getXPath = require('get-xpath');
const computedStyleToInlineStyle = require("computed-style-to-inline-style");
const config = require('./config');


async function init(){
    let browser = await puppeteer.launch({
        headless: false,
        args: [
            '--no-sandbox', 
            '--disable-setuid-sandbox',
            `--proxy-server=${config.PROXY}`,
            `--disable-extensions-except=${config.cookieIgnorePath}`,
            `--load-extension=${config.cookieIgnorePath}`,
        ],

        defaultViewport: null
    });

    console.log("[*] Browser loaded");
    return browser;
}

async function goto(browser, url, w, h){
    let page = await browser.newPage();
    await page.setViewport({width: w, height: h});
    await page.setCacheEnabled(false);
    await page.goto(url, {waitUntil: "domcontentloaded"});
    console.log(`[*] ${url} opened`);
    return page;
}

async function processPage(page, styles){
    await addStyles(page, styles);
    await addBoundingBox(page)
    await addXPath(page)
    console.log("[*] page is augmented")
}

async function getBody(page){
    let bodyHTML = await page.evaluate(() => window.document.body.outerHTML);
    return bodyHTML.replace(/\s+/g, ' ').trim();
}

async function addStyles(page, styles){
    await page.addScriptTag({ url : "https://unpkg.com/computed-style-to-inline-style"})
    await page.evaluateHandle((styles) => {
        let options = {
            recursive: true,
        }
        if (!!styles.length){options.properties = styles}

        computedStyleToInlineStyle(document.body, options)
    }, styles)
}
async function addBoundingBox(page){
    await page.addScriptTag({content: htmlAugmentation.addBoundingBox.toString()})
    await page.evaluateHandle(() => {
        addBoundingBox(document.querySelector("body"));
        Array.from(document.querySelectorAll("body *")).forEach(addBoundingBox);
    })
}

async function addXPath(page){
    await page.addScriptTag({content: `const getXPath = ${getXPath.toString()}`})
    await page.addScriptTag({content: htmlAugmentation.addXPath.toString()})
    await page.evaluateHandle(() => {
        addXPath(document.querySelector("body"));
        Array.from(document.querySelectorAll("body *")).forEach(addXPath);
    })
}

exports.init = init;
exports.goto = goto;
exports.processPage = processPage;
exports.getBody = getBody;
