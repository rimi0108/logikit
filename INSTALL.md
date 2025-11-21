# Logikit Installation Guide

## Local Installation (Development)

From the project root:

```bash
cd logikit
pip install -e .
```

Or directly from the project root:

```bash
pip install -e ./logikit
```

## PyPI Distribution (Future)

```bash
cd logikit
python -m build
twine upload dist/*
```

## Usage

After installation:

```python
from logikit import logikit

@logikit(condition_map={
    "_fails_regulated_area_rules": "Check regulated area requirements",
})
def is_eligible(self):
    if self._fails_regulated_area_rules():
        return False
    return True
```
