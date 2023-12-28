import os
import warnings
import matplotlib.pyplot as plt
import geopandas as gpd
import imageio.v2 as imageio

class Visualisation:
    def __init__(self):
        self.group_color_mapping = None

    def set_group_color_mapping(self, col):
        unique_values = sorted(list(set(col)))
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


    def create_tree_map(self, pop, save_path=None):
        warnings.filterwarnings('ignore', message='.*argument looks like a single numeric RGB*.', )
        plt.figure(figsize=(10, 8))

        x = [x._gps[0] for x in pop._trees_alive]
        y = [y._gps[1] for y in pop._trees_alive]
        groups = [x._grouppe for x in pop._trees_alive]

        colors = self.map_col2color(groups)
        plt.scatter(x=x, y=y, color=colors, alpha=0.75,  linewidth=0, s=2)

        # add custom legend
        for group in self.group_color_mapping:
            if group in groups:
                plt.scatter([], [], c=self.group_color_mapping[group], alpha=0.75, s=5, label=group)

        # Add background (Vienna)
        self.draw_background()

        # Adjust legend position and marker size
        plt.legend(loc='upper left', title="Group Labels", title_fontsize='12', markerscale=5)

        # Add a main title
        plt.suptitle("Tree Population", fontsize=20)

        if save_path is not None:
            plt.savefig(save_path)
        plt.show()

    def draw_background(self, file_path='../data/export.geojson'):
        gdf = gpd.read_file(file_path)
        coordinates = gdf.geometry.unary_union.exterior.xy
        plt.plot(coordinates[0], coordinates[1], linewidth=2, color='blue', label='Vienna')

    def create_visualisation_step(self, pop, iteration, path='../results/'):
        if not os.path.isdir(path):
            os.mkdir(path)
        self.create_tree_map(pop, save_path=path + f"step_{iteration}.png")

    def make_gif(self, path='../results/', output_path='../results/gif/'):
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        images = []
        for filename in os.listdir(path):
            if filename.endswith('.png'):
                images.append(imageio.imread(path + filename))
        imageio.mimsave(output_path + 'simulation.gif', images, fps=2)

if __name__ == '__main__':
    vis = Visualisation()
    vis.make_gif()
    """
    rel in https://overpass-turbo.eu/
    32484
    18444
    65901
    75
    30218
    """