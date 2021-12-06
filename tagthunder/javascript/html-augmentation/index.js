"use strict";

const computedStyleToInlineStyle = require("computed-style-to-inline-style");
const getXPath = require('get-xpath');

function addBoundingBox(el){

    let rectangle = el.getBoundingClientRect();
    value = `${rectangle.x} ${rectangle.y} ${rectangle.width} ${rectangle.height}`
    el.setAttribute("bbox", value);
}

function addComputedStyles(el, styles){
    computedStyleToInlineStyle(
        el,
        {
            recursive: false,
            properties: styles
        }
    );
}

function addXPath(el){
    el.setAttribute("xpath", getXPath(el));
}

function getElementByXPath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

exports.getElementByXPath = getElementByXPath;
exports.addComputedStyles = addComputedStyles;
exports.addBoundingBox = addBoundingBox;
exports.addXPath = addXPath;
