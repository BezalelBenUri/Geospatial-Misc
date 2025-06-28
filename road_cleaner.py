import geopandas as gpd
from shapely.geometry import Polygon, LineString
from pathlib import Path
import os

# Parameters
DUPLICATE_TOLERANCE = 1e-6
MIN_SEGMENT_LENGTH_METERS = 3.5
OUTPUT_FOLDER_NAME = "cleaned_output"

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / OUTPUT_FOLDER_NAME
OUTPUT_DIR.mkdir(exist_ok=True)

# Lagos UTM Zone (for metric distance calculations)
WGS84 = "EPSG:4326"
UTM_METRIC = "EPSG:32631"  # UTM Zone 31N (covers Lagos)

def explode_geometry_to_segments(geom):
    """
        Explode Polygon or LineString into its constituent line segments

        Args:
            geom (Shapely.geometry): The input geometry (Polygon or LineString).

        Returns:
            list: A list of LineString segments.
    """
    segments = []
    if isinstance(geom, Polygon):
        coords = list(geom.exterior.coords)
    elif isinstance(geom, LineString):
        coords = list(geom.coords)
    else:
        return []

    for i in range(len(coords) - 1):
        pt1, pt2 = coords[i], coords[i + 1]
        seg = LineString([pt1, pt2])
        segments.append(seg)
    return segments

def find_duplicates(gdf):
    """
        Identifies duplicate geometries within a GeoDataFrame.

        Duplicates are determined based on exact equality within a specified tolerance
        (`DUPLICATE_TOLERANCE`).

        Args:
            gdf (geopandas.GeoDataFrame): The input GeoDataFrame to check for duplicates.

        Returns:
            list: A list of integer indices corresponding to the rows with duplicate geometries.
    """
    print("🔍 Checking for duplicate geometries...")
    seen = []
    duplicates = []
    for i, geom in enumerate(gdf.geometry):
        if any(geom.equals_exact(other, DUPLICATE_TOLERANCE) for other in seen):
            duplicates.append(i)
        else:
            seen.append(geom)
        if i > 0 and i % 500 == 0:
            print(f"   🔄 Processed {i}/{len(gdf)} geometries...")
    print(f"   ⚠️ Found {len(duplicates)} duplicates.")
    return duplicates

def clean_file(file_path: Path):
    """
        Cleans a single GeoJSON file by removing duplicate geometries and short line segments.

        The cleaning process involves:
        1. Reading the GeoJSON file into a GeoDataFrame.
        2. Removing geometries that are exact duplicates based on `DUPLICATE_TOLERANCE`.
        3. Reprojecting the data to a UTM metric CRS (`UTM_METRIC`) for accurate length calculations.
        4. Exploding Polygon and LineString geometries into individual line segments.
        5. Filtering out segments shorter than `MIN_SEGMENT_LENGTH_METERS`.
        6. Reprojecting the cleaned segments back to WGS84 (`WGS84`).
        7. Saving the cleaned segments as a new GeoJSON file in the `cleaned_output` directory.

        Args:
            file_path (Path): The path to the GeoJSON file to be cleaned.
    """
    print(f"\n📂 Processing: {file_path.name}")
    try:
        gdf = gpd.read_file(file_path)
        gdf = gdf[gdf.geometry.notnull()]
        total_before = len(gdf)

        # Remove duplicates
        duplicates = find_duplicates(gdf)
        gdf = gdf.drop(index=duplicates)

        # Reproject to metric CRS
        gdf = gdf.to_crs(UTM_METRIC)

        # Explode into segments
        print("🧨 Exploding and filtering segments...")
        segments = []
        for geom in gdf.geometry:
            segments.extend(explode_geometry_to_segments(geom))

        # Filter out short segments (≤ 3 meters)
        long_segments = [seg for seg in segments if seg.length > MIN_SEGMENT_LENGTH_METERS]

        if not long_segments:
            print("⚠️ No valid segments left after filtering.")
            return

        cleaned_gdf = gpd.GeoDataFrame(geometry=long_segments, crs=UTM_METRIC)
        cleaned_gdf = cleaned_gdf.to_crs(WGS84)  # Convert back to WGS84 for GeoJSON

        # Save
        output_file = OUTPUT_DIR / file_path.name
        cleaned_gdf.to_file(output_file, driver="GeoJSON")

        print(f"✅ Cleaned {file_path.name}:")
        print(f" - Original features: {total_before}")
        print(f" - Duplicates removed: {len(duplicates)}")
        print(f" - Final segments: {len(cleaned_gdf)}")
    except Exception as e:
        print(f"❌ Error processing {file_path.name}: {e}")

def main():
    """
        Main function to orchestrate the cleaning process for all GeoJSON files.

        This function scans the script's directory for GeoJSON files,
        skips files already in the `cleaned_output` folder, and
        applies the `clean_file` function to each found GeoJSON file.
    """
    print("🚀 Exploding & AutoCAD-style cleanup...\n")
    geojson_files = list(SCRIPT_DIR.glob("*.geojson"))
    if not geojson_files:
        print("⚠️ No .geojson files found.")
        return

    for file in geojson_files:
        if file.parent.name == OUTPUT_FOLDER_NAME:
            continue  # Skip already processed
        clean_file(file)

    print("\n✅ Done. Cleaned files in 'cleaned_output/'")

if __name__ == "__main__":
    main()