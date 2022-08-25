from setuptools import setup, find_packages

setup(
    name="ust_wildfire",
    version="1.0.0",
    packages=find_packages("ust_wildfire"),
    install_requires=[
        "numpy",
        "scipy",
        "pandas"
    ],
    extras_requires={
        "ERA5": ["netCDF4"]
    }
)
