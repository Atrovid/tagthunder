const fs         = require('fs')
const express    = require('express')
const bodyParser = require('body-parser')
const logger     = require('simple-node-logger').createSimpleLogger();
const cors       = require('cors')

const index      = require('./index')


async function main() {
    let router = express.Router();
    let app = express()
    app.enable("proxy-trust")

//    app.use(bodyParser.urlencoded({ extended: false }))
    app.use(bodyParser.json({limit: '50mb'}))
    app.use(bodyParser.urlencoded({limit: '50mb', extended: true}))
    app.use(cors())

    app.set('view engine', 'ejs')

    app.use('/assets', express.static('public'))

    router.get('/', (request, response) => {
        response.send({status: 'Ok'});
    });

    router.post('/',(req, res) => {
        let url = req.body.url;
        let force = ("force" in req.body) ? req.body.force : false;
        if ( ! url.includes("moz-extension://")){
            console.log("URL = "+ url);
            var html = ""; // = req.body.html;
            function runPuppeteer(callback) {
                index.runPuppeteer(url, force).then(function(finalHTML){
                    html = finalHTML;
                    callback();
                });
            }
            runPuppeteer(function() {
                console.log("HTML = "+ html.length);
                res.send({status: 'Ok', "html": html, "url": url});
            });
        }
    });
	
    app.use('/', router)

    app.listen(8080, "127.0.0.1")
}

main()

