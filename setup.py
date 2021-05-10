from setuptools import setup, find_packages
setup(
    name="fakegaussian",
    version="0.0.3",
    install_requires=["numpy", "ase"],
    entry_points={
        'console_scripts': ['g16=fakegaussian.cli:main']
    },
    packages=find_packages(),
)
