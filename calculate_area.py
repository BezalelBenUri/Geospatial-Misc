#!/usr/bin/env python3

import geopandas as gpd
import os

# EPSG code for UTM Zone 31N
TARGET_CRS = "EPSG:32631"
OUTPUT_FOLDER = "processed"

def process_shapefile(filepath, filename, output_folder):
    """
        Processes a single shapefile: reprojects to EPSG:32631, calculates area in hectares,
        adds the area as a new column, and saves to the output folder.

        Args:
            filepath (str): Full path to the input shapefile.
            filename (str): Name of the shapefile (used for output name).
            output_folder (str): Directory where the processed file will be saved.

        Returns:
            dict: Summary statistics (filename, feature count, total/min/max area in ha).
    """
    gdf = gpd.read_file(filepath)

    # Reproject if needed
    if gdf.crs.to_string() != TARGET_CRS:
        gdf = gdf.to_crs(TARGET_CRS)

    # Calculate area in hectares
    gdf["area_ha"] = gdf.geometry.area / 10000

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok = True)

    # Save to output folder
    output_path = os.path.join(output_folder, f"{filename[:-4]}_with_area.shp")
    gdf.to_file(output_path)

    return {
        "filename": filename,
        "count": len(gdf),
        "min_area": round(gdf["area_ha"].min(), 2),
        "max_area": round(gdf["area_ha"].max(), 2),
        "total_area": round(gdf["area_ha"].sum(), 2)
    }

def print_report(report_data):
    """
        Prints a formatted summary report of processed shapefiles.

        Args:
            report_data (list): List of summary dictionaries from process_shapefile().
    """
    print("\n📋 Wetlands Area Report (in hectares)")
    print("-" * 60)
    print(f"{'Shapefile':30} {'Count':>6} {'Min':>10} {'Max':>10} {'Total':>10}")
    print("-" * 60)
    for entry in report_data:
        print(f"{entry['filename'][:30]:30} {entry['count']:>6} {entry['min_area']:>10} {entry['max_area']:>10} {entry['total_area']:>10}")
    print("\n✅ All processing complete. Files saved to 'processed/' folder.")

def main():
    """
        Main routine: processes all shapefiles in the current folder and reports results.
    """
    folder_path = os.path.dirname(os.path.abspath(__file__))
    report_data = []

    print("🔍 Starting area calculation for all shapefiles...\n")

    for filename in os.listdir(folder_path):
        if filename.endswith(".shp") and not filename.endswith("_with_area.shp"):
            filepath = os.path.join(folder_path, filename)
            print(f"📂 Processing: {filename}")
            try:
                summary = process_shapefile(filepath, filename, os.path.join(folder_path, OUTPUT_FOLDER))
                print(f"✅ Saved to: {OUTPUT_FOLDER}/{filename[:-4]}_with_area.shp\n")
                report_data.append(summary)
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}\n")

    if report_data:
        print_report(report_data)
    else:
        print("⚠️ No shapefiles processed.")

if __name__ == "__main__":
    main()