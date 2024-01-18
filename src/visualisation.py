import os
import warnings
import matplotlib.pyplot as plt
import geopandas as gpd
import imageio.v2 as imageio
import json
from shapely.geometry import Polygon, MultiPolygon

class Visualisation:
    def __init__(self, config):
        self.group_color_mapping = None
        with open(config.data_path + config.species_mapping_file, 'r', encoding='utf-8') as f:
            self.group_name_mapping = json.load(f)
        self.group_name_mapping_reversed = {v: k for k, v in self.group_name_mapping.items()}
        self.bounding_box = config.bounding_box

    def set_group_color_mapping(self, col):
        unique_values = sorted(list(set(col)))
        unique_values = [key for key, value in self.group_name_mapping.items() if value in unique_values]
        # print(f'uniq value ', unique_values)
        num_unique_values = len(unique_values)
        # Use a colormap with a specific number of colors
        cmap = plt.get_cmap("tab20", num_unique_values)
        # Assign a color to each unique value
        colors = [cmap(i) for i in range(num_unique_values)]
        # Map each original value to its corresponding color
        self.group_color_mapping = {value: color for value, color in zip(unique_values, colors)}


    def map_col2color(self, col):
        assigned_colors = [self.group_color_mapping[x] for x in col]
        return assigned_colors


    def create_tree_map(self, pop, year, save_path=None):
        warnings.filterwarnings('ignore', message='.*argument looks like a single numeric RGB*.', )
        plt.figure(figsize=(10, 8))

        x = [x._long for x in pop._trees_alive]
        y = [y._lat for y in pop._trees_alive]
        groups = [self.group_name_mapping_reversed.get(x._species, str(x._species)) for x in pop._trees_alive]

        colors = self.map_col2color(groups)

        plt.scatter(x=x, y=y, color=colors, alpha=0.75,  linewidth=0, s=2)

        # add custom legend
        plt.fill([], [], c='lightblue', label='Danube')
        for group in self.group_color_mapping:
            if group in groups:
                plt.scatter([], [], c=self.group_color_mapping[group], alpha=0.75, s=5, label=group)

        # Add background (Vienna and Danube)
        self.draw_danube()
        self.draw_vienna()

        plt.xlim(self.bounding_box[0][1],self.bounding_box[1][1])
        plt.ylim(self.bounding_box[0][0],self.bounding_box[1][0])

        # Adjust legend position and marker size
        plt.legend(loc='upper left', title="Group Labels", title_fontsize='12', markerscale=5)

        # Add a main title
        plt.suptitle(f"Tree Population {year}", fontsize=20)

        if save_path is not None:
            plt.savefig(save_path)
        plt.show()

    def draw_vienna(self, file_path='../data/export.geojson'):
        gdf = gpd.read_file(file_path)
        coordinates = gdf.geometry.unary_union.exterior.xy
        plt.plot(coordinates[0], coordinates[1], linewidth=2, color='blue', label='Vienna')

    def draw_danube(self, dir_path='../data/'):
        for file in os.listdir(dir_path):
            if file.startswith('danube'):
                gdf = gpd.read_file(dir_path+file)
                obj = gdf['geometry'][0]

                if type(obj) == Polygon:
                    x, y = obj.exterior.xy
                    plt.fill(x, y, linewidth=2, color='lightblue')
                elif type(obj) == MultiPolygon:
                    for polygon in list(obj.geoms):
                        x, y = polygon.exterior.xy
                        plt.fill(x, y, linewidth=2, color='lightblue')

    def create_visualisation_step(self, pop, iteration, path='../results/'):
        if not os.path.isdir(path):
            os.mkdir(path)
        self.create_tree_map(pop, pop._starting_year+iteration, save_path=path + f"step_{iteration}.png")

    def make_gif(self, path='../results/', output_path='../results/gif/'):
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        images_name = []
        images = []
        for filename in os.listdir(path):
            if filename.endswith('.png'):
                images_name.append((filename, int(filename.split('_')[1].split('.')[0])))
        for image_file, order in sorted(images_name, key=lambda x: x[1]):
            images.append(imageio.imread(path + image_file))
        imageio.mimsave(output_path + 'simulation.gif', images, fps=2)

if __name__ == '__main__':
    vis = Visualisation()
    vis.make_gif()