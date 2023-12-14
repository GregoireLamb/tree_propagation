import matplotlib.pyplot as plt

def map_col2color(col):
    unique_values = sorted(list(set(col)))
    num_unique_values = len(unique_values)

    # Use a colormap with a specific number of colors
    cmap = plt.get_cmap("tab20", num_unique_values)

    # Assign a color to each unique value
    colors = [cmap(i) for i in range(num_unique_values)]

    # Map each original value to its corresponding color
    color_mapping = {value: color for value, color in zip(unique_values, colors)}
    assigned_colors = [color_mapping[x] for x in col]

    return assigned_colors, unique_values

def plot_tree_population(pop):
    # Set a larger figure size
    plt.figure(figsize=(10, 8))

    x = [x._gps[0] for x in pop._trees_alive]
    y = [y._gps[1] for y in pop._trees_alive]
    col = [x._grouppe for x in pop._trees_alive]

    colors, labels = map_col2color(col)

    for label, color in zip(labels, colors):
        indices = [i for i, x in enumerate(col) if x == label]
        plt.scatter(x=[x[i] for i in indices], y=[y[i] for i in indices], color=color, alpha=0.75, label=label, linewidth=0, s=2)

    # Adjust legend position and marker size
    plt.legend(loc='upper left', title="Group Labels", title_fontsize='12', markerscale=5)

    # Add a main title
    plt.suptitle("Tree Population", fontsize=20)

    plt.show()
