import setuptools

with open('requirements.txt') as f:
    requires = [
        r.split('/')[-1] if r.startswith('git+') else r
        for r in f.read().splitlines()]

with open('README.md') as file:
    readme = file.read()


setuptools.setup(
    name='zfitter',
    version='0.1',
    description='zfit wrapper',
    author='Keita Mizukoshi (@mzks)',
    url='https://github.com/mzks/zfitter',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requires,
    python_requires=">=3.6",
    zip_safe=False)
