"use strict";

const computedStyleToInlineStyle = require("computed-style-to-inline-style");
const getXPath = require('get-xpath');

function addBoundingBox(el){

    let rectangle = node.getBoundingClientRect();
    value = `${rectangle.x} ${rectangle.y} ${rectangle.width} ${rectangle.height}`
    node.setAttribute("bbox", value);
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

function addXpath(el){
    el.setAttribute("xpath", getXPath(el));
}

function getElementByXpath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

exports.getElementByXpath = getElementByXpath;
exports.addComputedStyles = addComputedStyles;
exports.addBoundingBox = addBoundingBox;
exports.addXpath = addXpath;
