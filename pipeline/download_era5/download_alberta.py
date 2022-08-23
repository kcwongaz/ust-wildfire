import cdsapi

year_start = 1979
year_end = 2020

outdir = "../data/era5_alberta"

# -------------------------------------------------------------------------- #

cds = cdsapi.Client()

dataset = "reanalysis-era5-single-levels"


for yr in range(year_start, year_end + 1):
    fout = f"{outdir}/alberta_{yr}.nc"

    print()
    print(f"... Now working on {yr}")
    print()

    params = {
        "product_type": "reanalysis",
        "format": "netcdf",
        "variable": "2m_temperature",
        "date": f"{yr}-01-01/{yr}-12-31",
        "time": ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", 
                 "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", 
                 "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", 
                 "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
        "area": [60.0, -120.0, 48.99, -109.99],
        "grid": [0.25, 0.25]
    }

    try:
        cds.retrieve(dataset, params, fout)
    except:
        print(f"Year {yr} failed.")

