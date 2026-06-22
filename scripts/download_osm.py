import osmnx as ox
import argparse
import os

def download_city_graph(location_name: str, output_file: str):
    """
    Downloads the street network for a given location using osmnx 
    and saves it as a .graphml file for offline use.
    """
    print(f"Downloading street network for: {location_name}...")
    try:
        # Fetch drive network (roads suitable for cars/ambulances)
        graph = ox.graph_from_place(location_name, network_type='drive')
        
        # Save to file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        ox.save_graphml(graph, output_file)
        print(f"✅ Successfully saved graph to {output_file}")
        
    except Exception as e:
        print(f"❌ Error downloading data: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download OSM maps for offline Aegis simulation.")
    parser.add_argument("--location", type=str, default="Piedmont, California, USA", help="City or neighborhood name")
    parser.add_argument("--output", type=str, default="data/osm/piedmont.graphml", help="Output file path")
    
    args = parser.parse_args()
    download_city_graph(args.location, args.output)
