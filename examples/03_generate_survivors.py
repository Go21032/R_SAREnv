import contextily as cx
import geopandas as gpd
import matplotlib.pyplot as plt
from sarenv import (
    DatasetLoader,
    LostPersonLocationGenerator,
    get_logger,
)
from shapely.geometry import Point

log = get_logger()


def generate_and_visualize_survivors():
    """Main function to generate and visualize survivor locations."""
    log.info("--- Starting Lost Person Location Generation Example ---")

    dataset_dir = "sarenv_dataset"
    size_to_load = "medium"
    num_locations = 100

    try:
        # 1. Load the dataset for a specific size
        log.info(f"Loading data for size: '{size_to_load}'")
        loader = DatasetLoader(dataset_directory=dataset_dir)
        dataset_item = loader.load_environment(size_to_load)

        if not dataset_item:
            log.error(f"Could not load the dataset for size '{size_to_load}'.")
            return

        # 2. Initialize the lost person location generator with the loaded data
        log.info("Initializing the LostPersonLocationGenerator.")
        lost_person_generator = LostPersonLocationGenerator(dataset_item)

        # 3. Generate lost person locations
        log.info(f"Generating {num_locations} lost person locations...")
        locations = lost_person_generator.generate_locations(num_locations, 0)

        if not locations:
            log.error("No lost person locations were generated. Cannot visualize.")
            return

        # 4. Visualize the generated locations
        log.info("Visualizing generated locations...")

        fig, ax = plt.subplots(figsize=(12, 12))
        
        # ▼▼▼ THIS IS THE CORRECTED LINE ▼▼▼
        features_gdf = dataset_item.features
        # ▲▲▲ THE ERROR WAS HERE ▲▲▲

        features_gdf.plot(ax=ax, aspect=1, alpha=0.5, edgecolor="k", legend=True)

        points = [Point(loc) for loc in locations]
        locations_gdf = gpd.GeoDataFrame(geometry=points, crs=features_gdf.crs)

        locations_gdf.plot(ax=ax, marker='o', color='red', markersize=50, label="Lost Persons")

        cx.add_basemap(ax, crs=features_gdf.crs.to_string(), source=cx.providers.OpenStreetMap.Mapnik)

        ax.set_title(f"{num_locations} Generated Lost Person Locations", fontsize=16)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        plt.legend()
        plt.tight_layout()

        output_filename = "survivor_locations.png"
        plt.savefig(output_filename)
        log.info(f"Visualization saved to {output_filename}")

    except FileNotFoundError:
        log.error(
            f"Error: The dataset directory '{dataset_dir}' or its master files were not found."
        )
        log.error(
            "Please run the `export_dataset()` method from the DataGenerator first."
        )
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    generate_and_visualize_survivors()
    
#元のコード
# import contextily as cx
# import geopandas as gpd
# import matplotlib.pyplot as plt
# from matplotlib.patches import Patch, Circle
# from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
# from sarenv import (
#     DatasetLoader,
#     LostPersonLocationGenerator,
#     get_logger,
# )
# from sarenv.utils.plot import DEFAULT_COLOR, FEATURE_COLOR_MAP
# from shapely.geometry import Point

# log = get_logger()

# if __name__ == "__main__":
#     log.info("--- Starting lost_person Location Generation Example ---")

#     dataset_dir = "sarenv_dataset/16"
#     size_to_load = "xlarge"
#     num_locations = 100

#     try:
#         # 1. Load the dataset for a specific size
#         log.info(f"Loading data for size: '{size_to_load}'")
#         loader = DatasetLoader(dataset_directory=dataset_dir)
#         dataset_item = loader.load_environment(size_to_load)

#         if not dataset_item:
#             log.error(f"Could not load the dataset for size '{size_to_load}'.")

#         # 2. Initialize the lost_person location generator with the loaded data
#         log.info("Initializing the lost_personLocationGenerator.")
#         lost_person_generator = LostPersonLocationGenerator(dataset_item)

#         # 3. Generate lost_person locations
#         log.info(f"Generating {num_locations} lost_person locations...")
#         locations = lost_person_generator.generate_locations(num_locations, 0) # 0% random samples

#         if not locations:
#             log.error("No lost_person locations were generated. Cannot visualize.")

#     except FileNotFoundError:
#         log.error(
#             f"Error: The dataset directory '{dataset_dir}' or its master files were not found."
#         )
#         log.error(
#             "Please run the `export_dataset()` method from the DataGenerator first."
#         )
#     except Exception as e:
#         log.error(f"An unexpected error occurred: {e}", exc_info=True)
