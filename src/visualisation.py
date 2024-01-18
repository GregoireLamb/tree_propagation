import matplotlib.pyplot as plt
import geopandas as gpd

def map_col2color(col):
    unique_values = list(set(col))
    num_unique_values = len(unique_values)

    # Use a colormap with a specific number of colors
    cmap = plt.get_cmap("tab20", num_unique_values)

    # Assign a color to each unique value
    colors = [cmap(i) for i in range(num_unique_values)]

    # Map each original value to its corresponding color
    color_mapping = {value: color for value, color in zip(unique_values, colors)}
    assigned_colors = [color_mapping[x] for x in col]

    return assigned_colors, unique_values

def create_tree_map(pop):
    # Set a larger figure size
    plt.figure(figsize=(10, 8))

    x = [x._long for x in pop._trees_alive]
    y = [y._lat for y in pop._trees_alive]

    print(x[0],y[0])

    col = [x._species for x in pop._trees_alive]

    colors, labels = map_col2color(col)

    for label, color in zip(labels, colors):
        indices = [i for i, x in enumerate(col) if x == label]
        plt.scatter(x=[x[i] for i in indices], y=[y[i] for i in indices], color=color, alpha=0.75, label=label, linewidth=0, s=2)

    # Add background (Vienna)
    draw_background()

    # Adjust legend position and marker size
    plt.legend(loc='upper left', title="Group Labels", title_fontsize='12', markerscale=5)

    # Add a main title
    plt.suptitle("Tree Population", fontsize=20)

    plt.show()

def draw_background(file_path='../data/export.geojson'):
    gdf = gpd.read_file(file_path)
    coordinates = gdf.geometry.unary_union.exterior.xy
    plt.plot(coordinates[0], coordinates[1], linewidth=2, color='blue', label='Vienna')


if __name__ == '__main__':
    draw_background()
    pass
