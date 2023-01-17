# The TagThunder project

## About

The tag thunder project is a research work conducted within the [GREYC](https://www.greyc.fr/) research lab at the [University of Caen Normandie](http://www.unicaen.fr/).

This research work was funded by the ’Region Normandie’ with the CPER NUMNIE project.

This project aims to provide new ways to access web page  content for blind users in order to enable a faster skimming of content.

Skimming and scanning are two strategies for *speed reading*. Skimming allows a reader to get a first glance of a document, while scanning is the process of searching for a specific piece  of information in a document. While both techniques are available in visual reading mode, it is rather difficult to use them in non visual environments. We introduce the concept of *tag thunder*, to provide  speed reading non-visual techniques similar to skimming and scanning. A *tag thunder* is the oral transposition of the  tag cloud idea. Tag cloud key terms are presented with typographic effects  depending on their relevance and number of occurrences. Within a tag thunder, the relevance of a given key term is  translated into  specific speech effects and its position on the page is reflected in the position of the corresponding sound on a 2D stereo  space. All key terms of a tag thunder are played together, following a  concurrent speech strategy, exploiting the *cocktail party effect*.

## Repository's structure

<!--command line to make the tree :tree tagthunder -L 3 -I '__*|*.egg*' | xclip -selection c-->

- `pipeline` contains TagThunder pipeline's blocks : 
  - `cleaning` to build `HTML++`;
  - `segementation` to split the page into different parts, *i.e.* areas ; 
  - `extraction` to obtain area's textual descriptors ; 
  - `spatialization` to spell a description of each area for modelling *cocktail party effect*.
  - `experimentations` contains tools to make algorithms experimentations.
- `api` contains TagThunder API : 
  - `configuration` contains :
    - API configuration ;
    - Algorithms requests, *i.e.* if the algorithm is enable, which parameters are available and their defaults values.
  - `routers` contains routes to call algorithms and TagThunder pipeline ;
  - `models` contains : 
    - request responses ;
    - response factories.
    <!-- - `data` contains webpage corpus and tools to build them.-->

## Installation

**Requirements**

+ `python 3.9`
+ `poetry`
+ `make`
+ `screen`

#### Step 1 : clone this repository
```sh
git clone https://git.unicaen.fr/francois.ledoyen/tagthunder.git
```

#### Step 2 : Enter in the folder
```sh
cd tagthunder
```

#### Step 3 : Install app
```sh
make install
```

### Run App
Run API and crawler in two screen sessions
```sh
make run
```
to attach session :
```sh
screen -r tagthunder-<api | crawler>
```

Run API or crawler separately
```sh
make run-api
#or
make run-crawler
```






