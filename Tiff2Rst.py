import sys
from osgeo import gdal

def convert_tiff_to_rst(input_file, output_file):
    """Convert a TIFF raster to Idrisi RST format.

    Args:
        input_file (str): The path to the input TIFF raster file.
        output_file (str): The path to the output Idrisi RST file.
    """
    gdal.Translate(output_file, input_file, format = 'RST')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py input_tiff_file output_rst_file")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        convert_tiff_to_rst(input_file, output_file)