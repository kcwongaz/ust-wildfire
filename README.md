# Overview
The goal of this project is to find out if there is any causal relation between the upward trend of wildfire activities and global climate change. 

Wildfires are becoming both larger and more in number. In California, [12 out of 20 of the historical largest wildfires occurred after 2017](https://en.wikipedia.org/wiki/List_of_California_wildfires). When you look at the number of wildfires per year around the world, you often see an increasing trend very similar to the increasing average temperature. These observations, and many others, unavoidably make us question if there is a causal connection.

One way to address this question is to look at the size distribution of wildfires. The sizes of wildfires often follow a power-law distribution (at least approximately), so naturally, we want to investigate how the effect of climate enters the wildfire power law.

I started this project with Prof. Sai-Ping Li during my MPhil at HKUST. This project is essentially a continuation of his paper [*H.-I. Lee, S.-L. Wang, and S.-P. Li, “Climate effect on wildfire burned area in Alberta (1961-2010)”, Int. J. Mod. Phys. C 24, 1350053 (2013).*](https://arxiv.org/abs/1909.11934) The work in this repo is only the initial phase of this project, rather than the full story, and we are still actively working on it.

If you just want to see the data analysis results, you can find them in the [notebooks](https://nbviewer.org/github/kcwongaz/ust_wildfire/tree/master/notebooks/). You can also find a detailed scholarly write-up of this project in Chapter 5 of my [MPhil thesis](https://drive.google.com/file/d/1wgr3l9psxnW8qiUr-FL-vXN2wRbjcxAC/view?usp=sharing).

<br>

# Getting Started

### 1 - Data
The dataset can be downloaded [here](https://drive.google.com/file/d/10Ff7UBt1Fg68EvGE-uMLrt5f4aQGI6RW/view?usp=sharing).

The dataset contains two .csv files holding the wildfire data in California, US and Alberta, Canada. Each row contains the location (lat, lon) of the fire, total burn area in ha, the start- and end-time of the fire in Unix timestamp, and four temperature measures of the wildfire (see the notebooks for definitions). There are also two .csv files containing the monthly average temperature in the two locations.

The raw data were obtained from:
- California Department of Forestry and Fire Protection, which release their data on the [California State Geoportal](https://gis.data.ca.gov/datasets/CALFIRE-Forestry::california-fire-perimeters-1950/explore?location=37.442493%2C-118.992700%2C6.86). Several data formats are available for download; I used the .geojson format because the .csv format doesn't have the lat, lon variables.
- [Alberta Ministry of Agriculture, Forestry and Rural Economic Development](https://wildfire.alberta.ca/resources/historical-data/historical-wildfire-database.aspx).
- Temperature / climate data is obtained from [ECMWF's ERA5 reanalysis](https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5). The two specific datasets I used are [ERA5 hourly data on single levels from 1959 to present](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview) and [ERA5 hourly data on single levels from 1950 to 1978 (preliminary version)](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels-preliminary-back-extension?tab=overview). See below for a small guide on how to download them
- The monthly average temperature in California and Alberta can be obtained from [World Bank Open Data](https://data.worldbank.org/). 

<br>

### 2 - Setting up

I suggest installing the code locally, e.g.

```bash
git clone https://github.com/kcwongaz/ust-wildfire
cd ust-wildfire
pip -e install .  # -e flag for editable mode
```

This project requires the standard scientific packages, `numpy`, `scipy`, `matplotlib`, and `pandas`. Optionally, `cdsapi` and `netCDF4` are needed if you want to download and process the ERA5 raw data.

Downloading the [processed dataset](https://drive.google.com/file/d/10Ff7UBt1Fg68EvGE-uMLrt5f4aQGI6RW/view?usp=sharing) and decompressing it to `data/` at the project root is enough to get the notebooks running.

<br>

If you want to start from the raw data, `pipeline/` has some scripts for reproducing the data processing. Just download the wildfire raw data from the links I provided above and place them in `data/raw/`, then run 

```bash
. ./pipeline/start.sh 
```

You may need to rename your raw data files to have the names `start.sh` looks for. See comments inside the script for more details.


<br>

### 3 - Dealing with ERA5

ERA5 climate data needed to be accessed through the CDS API, see the [official documentation](https://cds.climate.copernicus.eu/api-how-to) for how to set up an account. After you have an account, you can use the [`cdsapi`](https://pypi.org/project/cdsapi/) Python package to make your request.

`pipline/download_era5/` has some example scripts for requesting data through the CDS API. Historical climate datasets are large; typically you may want to work with them on a computing server. The script `pipeline/slrum_download_era5.sh` is an example script of how to do that in a SLRUM system, which is used by HKUST's HPC3.
