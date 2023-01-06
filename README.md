<div align="center">
<h2>
  Norfair-Pip: Packaged version of the Norfair Tracker Module  
</h2>
<h4>
    <img width="500" alt="teaser" src="docs/demo.gif">
</h4>
<div>
    <a href="https://pepy.tech/project/norfair-tracker"><img src="https://pepy.tech/badge/norfair-tracker" alt="downloads"></a>
    <a href="https://badge.fury.io/py/norfair-tracker"><img src="https://badge.fury.io/py/norfair-tracker.svg" alt="pypi version"></a>
</div>
</div>

## <div align="center">Overview</div>

This repo is a packaged version of the [NorFair](https://github.com/tryolabs/norfair/) tracker module.
### Installation
```
pip install norfair-tracker
```

### Detection Model + Norfair 
```python
from norfair_tracker.norfair import NorFair

tracker = NorFair(args)
for image in images:
   dets = detector(image)
   online_targets = tracker.update(dets)
```
