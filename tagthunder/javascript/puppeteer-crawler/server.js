"use strict"

const express = require('express')
const cors = require('cors')
const bodyParser = require('body-parser');
const crawler = require("./crawler")
const config = require("./config");

const browser = crawler.init();


const app = express()
app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.status(200).send('Puppeteer crawler server is running')
})

app.post('/', (req, res) => {
    console.log("[*] request received")
    let body = req.body;

    let pageBody = browser.then((browser) => {
            let page = crawler.goto(browser, body.url, body.width, body.height)
            return page.then((page) => {
                return crawler.processPage(page, body.styles).then(() => {
                    return crawler.getBody(page).then((html) => {
                    page.close();
                    return html;
                    });
                })
            })

    })

    res.setHeader('Content-Type', 'text/html');
    pageBody.then((html) =>
        res.status(200).send(html)
    )
})


app.listen(config.PORT, config.HOST);
console.log(`[*] Running on http:\/\/${config.HOST}:${config.PORT}`)