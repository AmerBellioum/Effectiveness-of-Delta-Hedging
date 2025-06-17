import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def surface_plotting(dataframe, x_col, y_col, z_col, title, z_label, cmap='plasma'):
    """
    Plots a 3D surface given a DataFrame with x, y, and z values.

    Parameters:
    - dataframe (pd.DataFrame): The data to plot
    - x_col (str): Column name for the x-axis
    - y_col (str): Column name for the y-axis
    - z_col (str): Column name for the z-axis
    - title (str): Title of the plot
    - z_label (str): Label for the z-axis
    - cmap (str): Matplotlib colormap name (default: 'plasma')
    """

    # Data Manipulation
    pivot_table = dataframe.pivot(index=y_col, columns=x_col, values=z_col)
    X = pivot_table.columns.values
    Y = pivot_table.index.values
    X_grid, Y_grid = np.meshgrid(X, Y)
    Z = pivot_table.values

    # Plotting
    fig = plt.figure(figsize=(20, 12))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X_grid, Y_grid, Z, cmap=cmap, edgecolor='k', linewidth=0.5, antialiased=True)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_zlabel(z_label)
    ax.set_title(title)
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label=z_label)
    plt.tight_layout()
    plt.show()
