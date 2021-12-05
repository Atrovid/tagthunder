"use strict";

let acceptKeywords = "(Accepter|Je comprends|Fermer|Close|Accept|I understand|Agree|Okay|D\'accord|J\'accepte|Oui|Ok)";

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

function xcc_contains(elements, acceptKeywords) {
    const text2 = `^(.*\s)?${acceptKeywords}(\s.*)?$`;
    const text = `^${acceptKeywords}$`;
    return Array.prototype.filter.call(elements, function(element){
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

function getCookiesContainers(){
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

    return elements;
}


function acceptCookies(){
    elements = getCookiesContainers()

    var _xcc = xcc_contains(elements, acceptKeywords);
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

    //Interaction with cookie consent pop-ups can cause code to break if the page reloads (page navigation error).
    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
    delay(3500);
}

exports.acceptCookies = acceptCookies