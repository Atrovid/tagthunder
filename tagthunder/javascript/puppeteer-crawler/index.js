"use strict"

const browserManager = require("./src/browser");
const config = require("./src/config");
const puppeteer = require('puppeteer');
const htmlAugmentation = require('html-augmentation');
const cookiesManager = require("./src/manage_cookies");

let url = "https://www.calvados.fr/accueil.html";
let styles = ["font-size", "background-image"];

async function init(){
    let browser = await puppeteer.launch({
        headless: false,
        args: [`--proxy-server=${config.proxy_address}`],
        defaultViewport: null
    });

    return browser;
}

async function run(){
    let browser = await init();
    console.log("[*] Browser loaded");
    let page = await browserManager.goto(browser, url, 1200, 1200);
    await page.exposeFunction("addBBox", async (el) => {
    return new Promise((resolve, reject) => {
        augmentHTML.addBoundingBox(el)
    })
    });
    await processPage(page)
}


async function augmentHTML(page, styles){
    console.log('[**] Start augmentation')
    let elements = await page.$$eval("body *", el => htmlAugmentation.addBoundingBox(el))
//    await page.evaluateHandle(async (styles) => await window.augmentHTML(styles), styles);
    return page;
}


async function processPage(page){
    let augmentedPage = await augmentHTML(page, styles)
    console.log("[*] Augmentation done")
}


//(async () => {
//    let page = await browser.newPage(browser, url, 1200, 1200)
//    browserManager.augmentHTML(page, styles);
//
//})();

run();
