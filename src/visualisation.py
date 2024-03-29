import os
import warnings

import geopandas as gpd
import imageio.v2 as imageio
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon


class Visualisation:
    """
    Visualisation class
    Deals with the maps and Gif
    """

    def __init__(self, config):
        self.species_label_map = config.species_label_map
        self.species_label_map_reversed = {v: k for k, v in self.species_label_map.items()}
        self.bounding_box = config.bounding_box
        self.show_plot_on_the_fly = config.show_plot_on_the_fly
        self.tree_size_visualization_max = config.tree_size_visualization_max
        self.tree_size_visualization_min = config.tree_size_visualization_min

    def set_group_color_mapping(self, col):
        """
        This function assert that each species has the same color over time even if some species
        disappear during the simulation
        """
        unique_values = sorted(list(set(col)))
        unique_values = [key for key, value in self.species_label_map_reversed.items() if value in unique_values]
        num_unique_values = len(unique_values)
        cmap = plt.get_cmap("tab20", num_unique_values) #If only 2 trees use tab10
        # Assign a color to each unique value
        colors = [cmap(i) for i in range(num_unique_values)]
        # Map each original value to its corresponding color
        self.group_color_mapping = {value: color for value, color in zip(unique_values, colors)}

    def map_col2color(self, col):
        """
        Getter function making sur that each species has the same color over representations
        """
        assigned_colors = [self.group_color_mapping[x] for x in col]
        return assigned_colors

    def create_tree_map(self, pop, year, save_path=None):
        """
        Create and save a map with the trees
        """
        warnings.filterwarnings('ignore', message='.*argument looks like a single numeric RGB*.', )
        fig, ax = plt.subplots(figsize=(10, 8))

        plt.xlim(self.bounding_box[0][1], self.bounding_box[1][1])
        plt.ylim(self.bounding_box[0][0], self.bounding_box[1][0])

        x = [x._long for x in pop._trees_alive]
        y = [y._lat for y in pop._trees_alive]
        # circle size depends on the tree age
        ages = [x._age for x in pop._trees_alive]
        # Scale in 5 steps between 0 and 25 (Max size over 25)
        scale = [int(self.tree_size_visualization_min + i * (self.tree_size_visualization_max - self.tree_size_visualization_min)/5) for i in range(5)]
        dot_size = [scale[(x // 5)] for x in ages]
        groups = [self.species_label_map.get(x._species, str(x._species)) for x in pop._trees_alive]
        colors = self.map_col2color(groups)

        plt.scatter(x=x, y=y, color=colors, alpha=0.75, linewidth=0, s=dot_size)

        # add custom legend
        plt.fill([], [], c='lightblue', label='Danube')
        for group in self.group_color_mapping:
            if group in groups:
                plt.scatter([], [], c=self.group_color_mapping[group], alpha=0.75, s=5, label=group)

        # Add background (Vienna and Danube)
        self.draw_danube()
        self.draw_vienna()

        # Adjust legend position and marker size
        plt.legend(loc='upper left', title="Group Labels", title_fontsize='12', markerscale=5)

        # Add a main title
        plt.suptitle(f"Tree Population {year}", fontsize=20)

        ax.set_xticks([])  # Remove x-axis ticks
        ax.set_yticks([])  # Remove y-axis ticks

        if save_path is not None:
            plt.savefig(save_path)
        if self.show_plot_on_the_fly:
            plt.show()
        plt.close()

    def draw_vienna(self, file_path='../data/export.geojson'):
        """
        Add Vienna boundaries
        """
        gdf = gpd.read_file(file_path)
        coordinates = gdf.geometry.unary_union.exterior.xy
        plt.plot(coordinates[0], coordinates[1], linewidth=1, color='black', label='Vienna')

    def draw_danube(self, dir_path='../data/'):
        """
        The danube visualisation
        """
        for file in os.listdir(dir_path):
            if file.startswith('danube'):
                gdf = gpd.read_file(dir_path + file)
                obj = gdf['geometry'][0]

                if type(obj) == Polygon:
                    x, y = obj.exterior.xy
                    plt.fill(x, y, linewidth=1, color='lightblue')
                elif type(obj) == MultiPolygon:
                    for polygon in list(obj.geoms):
                        x, y = polygon.exterior.xy
                        plt.fill(x, y, linewidth=2, color='lightblue')

    def create_visualisation_step(self, pop, iteration, path='../results/'):
        """
        Create a visualisation step and make sur plt will be able to save it
        """
        if not os.path.isdir(path):
            os.mkdir(path)
        self.create_tree_map(pop, pop._starting_year + iteration, save_path=path + f"step_{iteration}.png")

    def make_gif(self, img_path='../results/', output_path='../results/gif/'):
        """
        Generate a gif with all the simulation steps
        """
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        images_name = []
        images = []
        for filename in os.listdir(img_path):
            if filename.endswith('.png') and filename.startswith('step'):
                images_name.append((filename, int(filename.split('_')[1].split('.')[0])))
        for image_file, order in sorted(images_name, key=lambda x: x[1]):
            images.append(imageio.imread(img_path + image_file))
        imageio.mimsave(output_path + 'simulation.gif', images, fps=2)
