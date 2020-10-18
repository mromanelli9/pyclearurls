# pyClearURLs

Python implementation of [ClearURLs](https://gitlab.com/KevinRoebert/ClearUrls) add-on,
based on [pilate's work](https://github.com/pilate/pyclearurls).

Rules can be found here: [ClearURLs Rules](https://gitlab.com/KevinRoebert/ClearUrls/raw/master/data/data.min.json).

## Installation

Git to clone the repository from GitHub to install the latest development version:

```bash
git clone https://github.com/mromanelli9/pyclearurls
cd pyclearurls
pip install .
```

Alternatively, install directly from the GitHub repository:

```bash
pip install git+https://github.com/mromanelli9/pyclearurls
```

## Usage

```python
from pyclearurls import URLCleaner

cleaner = URLCleaner()

print(cleaner.clean("https://www.amazon.com/dp/exampleProduct/ref=sxin_0_pb?__mk_de_DE=dsa"))
```

## License

This source code is licensed under the MIT license found in the [LICENSE](./LICENSE) file.
