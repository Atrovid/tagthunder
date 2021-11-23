# The project

## About

The tag thunder project is a research work conducted within the [GREYC](https://www.greyc.fr/) research lab at the [University of Caen Normandie](http://www.unicaen.fr/).

This research work was funded by the ’Region Normandie’ with the CPER NUMNIE project.

This project aims to provide new ways to access web page  content for blind users in order to enable a faster skimming of content.

Skimming and scanning are two strategies for *speed reading*. Skimming allows a reader to get a first glance of a document, while scanning is the process of searching for a specific piece  of information in a document. While both techniques are available in visual reading mode, it is rather difficult to use them in non visual environments. We introduce the concept of *tag thunder*, to provide  speed reading non-visual techniques similar to skimming and scanning. A *tag thunder* is the oral transposition of the  tag cloud idea. Tag cloud key terms are presented with typographic effects  depending on their relevance and number of occurrences. Within a tag thunder, the relevance of a given key term is  translated into  specific speech effects and its position on the page is reflected in the position of the corresponding sound on a 2D stereo  space. All key terms of a tag thunder are played together, following a  concurrent speech strategy, exploiting the *cocktail party effect*.

## Repository's structure

This repository contains three packages : 

- `algorithms` contains TagThunder pipeline's blocks : 
  - `cleaning` to build `HTML++`;
  - `segementation` to split the page into different parts, *i.e.* areas ; 
  - `extraction` to obtain area's textual descriptors ; 
  - `spatialization` to spell a description of each area for modelling *cocktail party effect*.
- `api` contains TagThunder API build with [`FastAPI`](https://fastapi.tiangolo.com/) ([One of the fastest Python frameworks available](https://fastapi.tiangolo.com/#performance)) 
  - `configuration` contains :
    - API configuration ;
    - Algorithms requests, *i.e.* if the algorithm is enable, which parameters are available and their defaults values.   

<!--command line to make the tree :tree tagthunder -L 3 -I '__*|*.egg*' | xclip -selection c-->

```shell
tagthunder
├── algorithms 
│   ├── cleaning
│   │   ├── _abstract.py
│   │   └── vision_based.py
│   ├── extraction
│   │   ├── _abstract.py
│   │   ├── mots_blancs.py
│   │   └── yake.py
│   ├── models
│   │   ├── responses.py
│   │   └── web_elements.py
│   ├── segmentation
│   │   ├── _abstract.py
│   │   ├── clustering
│   │   ├── guided_expansion.py
│   │   ├── k_means.py
│   │   └── tdbu.py
│   └── spatialization
│       └── _abstract.py
├── api
│   ├── configurations
│   │   ├── algorithms
│   │   └── api.py
│   ├── main.py
│   ├── models
│   │   ├── domains.py
│   │   └── schemas.py
│   ├── routers
│   │   ├── queries.py
│   │   └── routes.py
│   └── services
│       ├── algorithms.py
│       └── dom_managment
└── webcrawler
    ├── express_app_js
    │   ├── content_script.js
    │   ├── index.js
    │   ├── node_modules
    │   ├── package.json
    │   ├── package-lock.json
    │   └── server.js
    └── wrapper.py
```

## Install and 
