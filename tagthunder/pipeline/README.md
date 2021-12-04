# Pipeline module

## Module structure

- `blocks` contains TagThunder pipeline's blocks (*i.e.* algorithms) :
  - `augmentation` to create `HTML+` 
  - `cleaning` to build `HTML++`;
  - `segementation` to split the page into different parts, *i.e.* areas ; 
  - `extraction` to obtain area's textual descriptors ;
  - `vocalization` to spell extracted keywords ; 
  - `spatialization` to spell a description of each area for modeling *cocktail party effect*.
- `experimentations` contains tools to make algorithms experimentations. For instances, measures for web segmentation, visualization functions, *etc.*
- `models` contains blocks' responses data structures.

## How to add a pipeline Block

Each block need to implement the abstract class of his family contained in `blocks/<block type>/_abstract.py`. 

Once the `class` (*i.e* block) is implemented it's necessary to `import`  it in `blocks/<block type>/__init__.py` to simplify. 



