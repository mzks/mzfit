# mzfit
zfit wrapper for lazy analysts [GitHub](https://github.com/mzks/mzfit)

Author: Keita Mizukoshi (Kobe Univ. mzks@stu.kobe-u.ac.jp, @mzks)

## Concept
[`zfit`](https://github.com/zfit/zfit) is a nice fitting tools on python, built on object-oriented interface.
However, I would sometime like to fit easily. I do *not always* want to care minimizers and cost function.
I usually take an approach for good fitting, try-error-retry with visual environment.
For that purpose, raw `zfit` is slightly much.
To prevent tenosynovitis of lazy analysts, I made a wrapper of `zfit`, `mzfit`

## Install via pip
```
pip install mzfit
```

## Simple Usage
See `notebook/simple_example.ipynb`


## Install for developer
```
git clone https://github.com/mzks/mzfit
python -m pip install -e mzfit
```

