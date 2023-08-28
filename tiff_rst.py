import os
import sys
from osgeo import gdal, osr

def convert_tiff_to_rst(input_file, output_file):
    """Convert a TIFF raster to Idrisi RST format.

    Args:
        input_file (str): The path to the input TIFF raster file.
        output_file (str): The path to the output Idrisi RST file.
    """
    
    if input_file is None:
        print("Failed to open the IDRISI file:", input_file)
        return
    if output_ds is not None:
        gdal.Translate(output_file, input_file, format = 'RST')
        print("Conversion from IDRISI to TIFF successful:", output_file)

def rst_to_tiff(input_rst_file, output_tiff_file, epsg_code = 32631):
    """
  Converts an RST file to a TIFF file with the specified coordinate system.

  Args:
    input_rst_file: The path to the RST file.
    output_tiff_file: The path to the output TIFF file.
    epsg_code: The EPSG code of the coordinate system.
  """
    input_rst = gdal.Open(input_rst_file)

    if input_rst is None:
        print("Failed to open the IDRISI file:", input_rst_file)
        return

    geotransform = input_rst.GetGeoTransform()
    data = input_rst.GetRasterBand(1).ReadAsArray()

    driver = gdal.GetDriverByName("GTiff")
    output_tiff = driver.Create(output_tiff_file, input_rst.RasterXSize, input_rst.RasterYSize, 1, gdal.GDT_Float32)

    if output_tiff is not None:
        output_tiff.SetGeoTransform(geotransform)
        output_tiff.GetRasterBand(1).WriteArray(data)

        srs = osr.SpatialReference()
        srs.ImportFromEPSG(epsg_code)
        output_tiff.SetProjection(srs.ExportToWkt())

        output_tiff = None
        print("Conversion from IDRISI to TIFF successful:", input_rst_file)
    else:
        print("Failed to create the output TIFF file.")

    input_rst = None

if len(sys.argv) != 4:
    print("Usage: python tiff_rst.py <input_file> <output_file> <epsg_code>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
epsg_code = int(sys.argv[3])

if input_file.lower().endswith(".tif") or input_file.lower().endswith(".tiff"):
    convert_tiff_to_rst(input_file, output_file)  # Use the new function for TIFF to IDRISI conversion
elif input_file.lower().endswith(".rst"):
    rst_to_tiff(input_file, output_file, epsg_code)  # Use the original function for IDRISI to TIFF conversion
else:
    print("Unsupported input file format.")
