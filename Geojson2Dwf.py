import geopandas as gpd
import ezdxf
from pathlib import Path

def geojson_to_dxf(geojson_path: Path):
    """
        geojson2dxf.py

        This script converts all GeoJSON (.geojson) files in the current directory into DXF (.dxf) format
        using the ezdxf library. It supports common geometry types such as LineString, Polygon, MultiPolygon,
        and Point.

        DXF (Drawing Exchange Format) is widely supported by CAD software like AutoCAD, LibreCAD, and DraftSight.
        Although DWG (AutoCAD's native format) is not directly supported for writing via open-source tools, the 
        resulting DXF files can be opened and saved as DWG using AutoCAD or compatible software.

        Dependencies:
        - geopandas
        - shapely
        - ezdxf

        Usage:
            Run the script in a directory containing GeoJSON files:

                python geojson2dxf.py

        Output:
            For each `filename.geojson`, a corresponding `filename.dxf` file will be created in the same directory.
    """

    gdf = gpd.read_file(geojson_path)
    dxf_path = geojson_path.with_suffix('.dxf')

    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()

    for geom in gdf.geometry:
        if geom is None:
            continue
        if geom.geom_type == 'LineString':
            msp.add_lwpolyline(list(geom.coords))
        elif geom.geom_type == 'Polygon':
            exterior = list(geom.exterior.coords)
            msp.add_lwpolyline(exterior, close=True)
            for interior in geom.interiors:
                msp.add_lwpolyline(list(interior.coords), close=True)
        elif geom.geom_type == 'MultiPolygon':
            for poly in geom.geoms:
                msp.add_lwpolyline(list(poly.exterior.coords), close=True)
        elif geom.geom_type == 'Point':
            x, y = geom.x, geom.y
            msp.add_circle((x, y), radius=0.5)
        # Add more geometry types if needed

    doc.saveas(dxf_path)
    print(f"✅ Saved DXF: {dxf_path.name}")

def main():
    script_dir = Path(__file__).parent
    for geojson_file in script_dir.glob("*.geojson"):
        geojson_to_dxf(geojson_file)

if __name__ == "__main__":
    main()