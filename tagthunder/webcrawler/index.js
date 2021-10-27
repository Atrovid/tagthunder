'use strict';

const puppeteer = require('puppeteer');
const fetch = require('node-fetch');
const https = require('https');
const fs = require('fs')
const request = require('request');
const jsdom = require("jsdom");
const del = require('del');

//const cs      = require('./content_script')

const config = {
    proxy: ('http_proxy' in process.env ? process.env["http_proxy"] : "")

}

const PUBLIC_REP_PATH_RELATIVE = "../public/";
//const PUBLIC_REP_PATH_ABSOLUTE = "/home/condami202/TagThunder/tagt/public/";
//const PUBLIC_REP_PATH_ABSOLUTE = "/www/tagthunder/uwsgi-prod/public/";

// Browser and page instance
async function instance(){
    const browser = await puppeteer.launch({
     headless: true,
     args: [`--proxy-server=${config.proxy}`],
     defaultViewport: null
  });

//    const context = await browser.createIncognitoBrowserContext();
//    const page = await context.newPage();

    const page = await browser.newPage()
//    await page.setViewport({ width: 1920, height: 1080 })
    await page.setViewport({ width: 1600, height: 900 })
    return {page, browser}
}

async function runPuppeteer(baseURL, force=false){
    const url = new URL(baseURL);
    let repName = url.hostname + url.pathname
    let separator = '-' // 'SLASH'
    repName = repName.replace(/\//g, separator)
    const REP_PATH = PUBLIC_REP_PATH_RELATIVE + repName
    const htmlFilename = PUBLIC_REP_PATH_RELATIVE + repName + '/input.html'
    const htmlFilenameWithStyle = PUBLIC_REP_PATH_RELATIVE + repName + '/webpage.html'

    let html = "";

    console.log("Début...")

    try{
        if (force && fs.existsSync(REP_PATH)){
            fs.rmdirSync(REP_PATH, { recursive: true });
        }

        if (!fs.existsSync(REP_PATH)){
            console.log("...First time for this URL...")
            fs.mkdirSync(REP_PATH);
            fs.mkdirSync(REP_PATH + '/img');

            const {page, browser} = await instance()

            try {
                await page.setCacheEnabled(false);

                await page.goto(baseURL, {waitUntil: 'networkidle0'})  // ['load','domcontentloaded','networkidle0','networkidle2']

                // URL given may be a redirection to an actuel (more complex) url of the webpage
                const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
//                await delay(3000); // gives some extra time to load.

                await page.waitForSelector('body')

                // A general way to combat cookie consents with headless puppeteer
                /* approach nowhere near complete, but shows an efficient way to eliminate cookie consent pop-ups.
                using language and generalized selectors to detect consent buttons and links.
                targeting the elements a, button within a container that uses the name cookie within an id, class.
                using regular expressions to identify button text which is commonly used to accept cookies (case-insensitive).*/
                await page.evaluate(_ => {
                    function createXPathFromElement(elm) {
                        var allNodes = document.getElementsByTagName('*');
                        for (var segs = []; elm && elm.nodeType == 1; elm = elm.parentNode)
                        {
                            if (elm.hasAttribute('id')) {
                                    var uniqueIdCount = 0;
                                    for (var n=0;n < allNodes.length;n++) {
                                        if (allNodes[n].hasAttribute('id') && allNodes[n].id == elm.id) uniqueIdCount++;
                                        if (uniqueIdCount > 1) break;
                                    };
                                    if ( uniqueIdCount == 1) {
                                        segs.unshift('id("' + elm.getAttribute('id') + '")');
                                        return segs.join('/');
                                    } else {
                                        segs.unshift(elm.localName.toLowerCase() + '[@id="' + elm.getAttribute('id') + '"]');
                                    }
                            } else if (elm.hasAttribute('class')) {
                                segs.unshift(elm.localName.toLowerCase() + '[@class="' + elm.getAttribute('class') + '"]');
                            } else {
                                for (i = 1, sib = elm.previousSibling; sib; sib = sib.previousSibling) {
                                    if (sib.localName == elm.localName)  i++; };
                                    segs.unshift(elm.localName.toLowerCase() + '[' + i + ']');
                            };
                        };
                        return segs.length ? '/' + segs.join('/') : null;
                    }
                    function lookupElementByXPath(path) {
                        var evaluator = new XPathEvaluator();
                        var result = evaluator.evaluate(path, document.documentElement, null,XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                        return  result.singleNodeValue;
                    }
                    function xcc_contains(elements, text) {
                        return Array.prototype.filter.call(elements, function(element){
                            const text2 = "^(.*\s)?(Accepter|Je comprends|Fermer|Close|Accept|I understand|Agree|Okay|D\'accord|J\'accepte|Oui|Ok)(\s.*)?$";
                            if (RegExp(text, "i").test(element.textContent.trim())){
                                if (RegExp(text2, "i").test(element.textContent.trim())){
                                    return true;
                                }
                            }else if (element.hasAttributes()) {
                                var attrs = element.attributes;
                                for(var i = attrs.length - 1; i >= 0; i--) {
                                    if (RegExp(text, "i").test(attrs[i].value)){
                                        if (RegExp(text2, "i").test(attrs[i].value)){
                                            return true;
                                        }
                                    }
                                }
                            }
                            return false;
                        });
                    }
                    var elements = [];
                    var done_nodes = [];
                    const tags = 'a, button, span';
                    document.querySelectorAll('body *').forEach(function(node) {
                        var xPath = createXPathFromElement(node);
                        if (!done_nodes.includes(xPath)){
                            var cookieHere = false;
                            done_nodes.push(xPath);
                            if (node.textContent.includes("cookie")){
                                cookieHere = true;
                            }else if (node.hasAttributes()) {
                                var attrs = node.attributes;
                                for(var i = attrs.length - 1; i >= 0; i--) {
                                    if (attrs[i].name.includes("cookie") || attrs[i].value.includes("cookie")){
                                        cookieHere = true;
                                        break;
                                    }
                                }
                            }
                            if (cookieHere){
                                if (tags.includes(node.tagName)){
                                    elements.push(node);
                                }
                                node.querySelectorAll('*').forEach(function(subnode) {
                                    done_nodes.push(createXPathFromElement(subnode));
                                    if (tags.includes(subnode.tagName)){
                                        elements.push(subnode);
                                    }
                                });
                            }
                        }
                    });
//                    const text = '^(Accepter les cookies|Tout accepter|Accepter|Je comprends|Fermer|Close|Accept all|Accept|I understand|Agree|Okay|Alle akzeptieren|Akzeptieren|Verstanden|Zustimmen|D\'accord|J\'accepte|Oui|Ok)$';
                    const text = "^(Accepter|Je comprends|Fermer|Close|Accept|I understand|Agree|Okay|D\'accord|J\'accepte|Oui|Ok)$";
                    var _xcc = xcc_contains(elements, text);
                    if (_xcc != null && _xcc.length > 0) {
                        console.log("There is a cookie consent for sure");
                        for (var c = 0; c < _xcc.length; c++) {
                            _xcc[c].click();
                        }
                    }else{
                        elements = document.querySelectorAll(tags);
                        _xcc = xcc_contains(elements, text);
                        if (_xcc != null && _xcc.length != 0) {
                            console.log("There may be a cookie consent (or another kind of popup/banner), click just in case it is");
                            _xcc[0].click();
                        }
                    }
                });

                //Interaction with cookie consent pop-ups can cause code to break if the page reloads (page navigation error).
//                const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
                await delay(3500); // also catches plenty of meta-refreshes, JS redirects and gives some extra time for large resources to load.


                await page.screenshot({ path: PUBLIC_REP_PATH_RELATIVE + repName + '/screenshot.png', fullPage: true});

                const imgURLs = await page.evaluate(() =>
                  Array.from(
                    document.querySelectorAll('img'),
                    ({ src }) => src,
                  )
                );
                console.log(imgURLs);

                // injection des informations dans le DOM du document HTML => HTML+
                await page.evaluate(_ => {
                    function enrichBBox(node){
                        var att = document.createAttribute("data-bbox");
                        var rectangle=node.getBoundingClientRect();
                        var x=rectangle.left>=0?parseInt(rectangle.left):0;
                        var y=rectangle.top>=0?parseInt(rectangle.top):0;
                        var  width=node.offsetWidth ? node.offsetWidth : 0;
                        var  height= node.offsetHeight ? node.offsetHeight : 0;
                        att.value = ""+x+ " " + y + " " + width+ " " + height ;
                        node.setAttributeNode(att);
                    }

                    function enrichStyle(node){
                        var attStyle = document.createAttribute("data-style");
                        var css = window.getComputedStyle(node);
                        var cssAtts="";
                        for (var j=0; j<css.length; j++){
                            var css_attr_name = css[j];
                            var css_attr_val = css.getPropertyValue(""+css[j]);
                            //on corrige l'ajout de guillemets aux extrémité !!?
                            if(node.tagName.toLowerCase() == 'body' && css_attr_name.toLowerCase().startsWith('font')){
                                console.log(css_attr_name);
                                console.log(css_attr_val);
                            }
                            if(typeof(css_attr_val) == "string"){
                                css_attr_val = css_attr_val.replace(/^"|"$/ug,'');
                                if(node.tagName.toLowerCase() == 'body' && css_attr_name.toLowerCase().startsWith('font')){
                                    console.log("Correcting String with quotes 1 : "+css_attr_val);
                                }
                                css_attr_val = css_attr_val.replace('"','\\"');
                                if(node.tagName.toLowerCase() == 'body' && css_attr_name.toLowerCase().startsWith('font')){
                                    console.log("Correcting String with quotes 2 : "+css_attr_val);
                                }
                            }
                            //var val= css[j] + ":" + css.getPropertyValue(""+css[j]);
                            if(css_attr_name.toLowerCase() == "quotes"){
                                continue;
                            }
                            var val = css_attr_name+':'+css_attr_val;
                            cssAtts+=val;
                            if(j!=css.length){
                                cssAtts+=";";
                            }
                        }
                        attStyle.value =cssAtts;
                        if(node.tagName.toLowerCase() == 'body'){
                            console.log("======");
                            console.log(attStyle);
                            console.log("======");
                        }
                        node.setAttributeNode(attStyle);
                    }

                    function injectInfoDOM() {
                        var nodes = document.getElementsByTagName("*");
                        for(var i = 0; i<nodes.length; i++){
                            var node = nodes[i];
                            if (node){
		                    // inject bounding box info
		                    enrichBBox(node);
		                    // inject style info
		                    if(i == 1){
		                        console.log(node);
		                    }
		                    enrichStyle(node);
		            }
                        }
                    }
                    injectInfoDOM();
                });
//                const aHandle = await page.evaluateHandle('document'); // Handle for the 'document'
                let documentHTML = await page.evaluate(() => document.documentElement.innerHTML); // encodeURIComponent(document.documentElement.innerHTML)
//                let dom = new jsdom.JSDOM(documentHTML);
//                let html = cs.injectInformation(dom.window.document);

                await browser.close();

                const { window } = new jsdom.JSDOM(documentHTML, { runScripts: "dangerously" });
                const myLibrary = fs.readFileSync("./content_script.js", { encoding: "utf-8" });
                const scriptEl = window.document.createElement("script");
                scriptEl.textContent = myLibrary;
                window.document.body.appendChild(scriptEl);
                html = window.document.documentElement.outerHTML; // encodeURIComponent(window.document.documentElement.innerHTML);
                console.log("html");
                console.log(html.length);

                for (var i=0; i < imgURLs.length; i++) {
                    let imgURL = imgURLs[i];
                    if (imgURL != ''){
    //                    html = html.split(imgURL.substring(0, imgURL.lastIndexOf('/'))).join(PUBLIC_REP_PATH_ABSOLUTE + repName + '/img');
                        let imgName = imgURL.substring(imgURL.lastIndexOf('/')+1)
                        var stringToGoIntoTheRegex = 'src="[^"]*' + imgName + '"';
                        var regex = new RegExp(stringToGoIntoTheRegex, "g");
                        imgName = imgName.replace(/%/g, 'PERCENTAGE')
                        html = html.split(imgURL).join('./img/' + imgName + '?url=' + repName);
                        html = html.replace(regex, 'src="./img/' + imgName + '?url=' + repName + '"')
    //                    let imgOUTPATH = PUBLIC_REP_PATH_ABSOLUTE + repName + '/img/' + imgName
    //                    html = html.split(imgURL).join(imgOUTPATH);
    //                    html = html.replace(regex, 'src="' + imgOUTPATH + '"')
                    }
                }

                fs.writeFileSync(htmlFilename, html);
                console.log("Successfully Written to " + htmlFilename + " File.");
//                fs.writeFile(htmlFilename, html, (err) => {
//                    if (err) console.log(err);
//                        console.log("Successfully Written to " + htmlFilename + " File.");
//                });

                fs.writeFile(htmlFilenameWithStyle, html.replace(/data-style/g, 'style'), (err) => {
                    if (err) {console.log(err);}
                    else{console.log("Successfully Written to " + htmlFilenameWithStyle + " File.");}
                });

                download(imgURLs, repName, function () { console.log("Image downloaded"); });

            } catch (erro) {
                console.log(erro)
                // si erreur alors suppression du repertoire de resultats, pour recalculer l'XP correctement plus tard, lorsque l'erreur sera corrigée
                try {
			        fs.rmdirSync(REP_PATH, {recursive: true});
			console.log(`${REP_PATH} is deleted!`);
		    } catch (error) {
			console.error(`Error while deleting ${REP_PATH}.`);
		    }
            }
        }else{
            console.log("...URL already processed before...");
//            function getHTMLfromFile(htmlFilename) {
//                return new Promise((resolve, reject) => {
//                    fs.readFile(htmlFilename, "utf-8", (err, buf) => {
//                                        if (err) {
//                                         console.log(err);
//                                        reject(err);
//                                        }else{
//                                            console.log("Successfully Read from File.");
//                                            html = buf.toString();
//                                            resolve(html);
//                                            }
//                                        });
//                });
//            }
//            getHTMLfromFile(htmlFilename).then(result => {
//                console.log("...Fin");
//                console.log(result.length);
//                console.log(html.length);
//                return html;
//            });
            var buf = fs.readFileSync(htmlFilename, "utf-8");
            console.log("Successfully Read from File.");
            html = buf.toString();
        }
    } catch (err) {
        console.log(err)
        // si erreur alors suppression du repertoire de resultats, pour recalculer l'XP correctement plus tard, lorsque l'erreur sera corrigée
        try {
		await del(REP_PATH);
		console.log(`${REP_PATH} is deleted!`);
	    } catch (erro) {
		console.error(`Error while deleting ${REP_PATH}.`);
	    }
    }
    console.log("...Fin");
    console.log(html.length);
    return html;
}

function download(files, repName, callback) {
    let index = 0;
    var data = setInterval(async () => {
        let i = index++
        if (i === files.length)
            clearInterval(data)
        else {
        	let imgURL = files[i % files.length]
        	if (imgURL != ''){
                let imgName = imgURL.substring(imgURL.lastIndexOf('/')+1)
                imgName = imgName.replace(/%/g, 'PERCENTAGE')
                console.log(imgName)
                let imgOUTPATH = PUBLIC_REP_PATH_RELATIVE + repName + '/img/' + imgName // `./images/${i}.${imgURL.slice(-3)}`
                request.head(imgURL, function (err, res, body) {
                    request(imgURL)
                        .pipe(fs.createWriteStream(imgOUTPATH))
                        .on("close", callback);
                });
            }
        }
    }, 4000);
}


module.exports = { runPuppeteer };


// https://www.linkedin.com/ https://www.facebook.com/  https://www.instagram.com/?hl=fr  https://twitter.com/?lang=fr  https://www.reddit.com/
/*runPuppeteer("https://www.facebook.com/").then(function(html){
    console.log("Result: " + html.length);
});*/


