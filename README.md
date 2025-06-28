"This repository is for modular geospatial analysis etc" 


# Tiff2Rst: TIFF to Idrisi RST Converter

This is a simple Python script that converts TIFF raster files to Idrisi RST format using the GDAL library. It provides an easy way to convert raster data for use in Idrisi software.

## Prerequisites

- Python 3.x
- GDAL library (Python bindings)

- Run the script with the following command:
	- python Tiff2Rst.py input_tiff_file.tif output_rst_file.rst


# tiff_rst: TIFF to Idrisi RST and RST to TIFF Converter

This is a simple Python script that converts TIFF raster files to Idrisi RST format and RST to TIFF using the GDAL library.

## Prerequisites

- Python 3.x
- GDAL library (Python bindings)

- Run the script with the following command
   - for conversion of rst to tif
   	- python tiff_rst.py input_tiff_file.tif output_rst_file.rst
   - conversion of tif to rst
   	- python tiff_rst.py input_tiff_file.tif output_rst_file.rst

# road_cleaner: Geospatial Data Cleanup Script
This is a Python script that performs an "AutoCAD-style" cleanup on GeoJSON files. It's designed to remove duplicate geometries, explode complex polygons and linestrings into individual segments, 
and filter out short, potentially noisy segments.
- Python 3.x
- Geopandas
- Shapely
- Run the script with the following command:
    	python road_cleaner.py
