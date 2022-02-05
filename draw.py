from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class Render:
    keybindings = {
        "forward": "8",
        "back": "5",
        "left": "4",
        "right": "6",
        "up": "ctrl+5",
        "down": "ctrl+8",
    }

    def __init__(self, size, voxels, block_config):
        # print keybindings
        print("Keybindings for moving around")
        print("   - right mouse button: zoom")
        print("   - left mouse button: rotate")
        for key, value in self.keybindings.items():
            print(f"   - {key}: {value}")

        # initialize storage
        colors = np.empty(voxels.shape, dtype=object)
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    blocktype = voxels[x][y][z]
                    colors[x][y][z] = block_config[blocktype]['color']

        # Weird magic borrowed from
        # https://matplotlib.org/devdocs/gallery/mplot3d/voxels_numpy_logo.html
        def explode(data):
            size = np.array(data.shape) * 2
            data_e = np.zeros(size - 1, dtype=data.dtype)
            data_e[::2, ::2, ::2] = data
            return data_e

        blocks = explode(voxels)
        facecolors = explode(colors)

        # Adds a small margin between blocks, allowing blocks which are enclosed to still render
        x, y, z = np.indices(np.array(blocks.shape) + 1, dtype=float) // 2
        x[0::2, :, :] += 0.05
        y[:, 0::2, :] += 0.05
        z[:, :, 0::2] += 0.05
        x[1::2, :, :] += 0.95
        y[:, 1::2, :] += 0.95
        z[:, :, 1::2] += 0.95

        # After the voodoo magic, plot everything
        fig = plt.figure()
        self.ax = fig.gca(projection='3d')
        self.ax.voxels(x, y, z, blocks, facecolors=facecolors, edgecolor='k', linewidth=0)
        self.ax.view_init(azim=225)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("z")
        self.ax.set_zlabel("y")
        fig.canvas.mpl_connect("key_press_event", self.move_view)

        plt.show()

    def move_view(self, event):
        # I have no idea, it this line have some effect at all
        self.ax.autoscale(enable=False, axis='both')
        # Set nearly similar speed of motion in dependency on zoom
        koef = 8.  # speed for 3D should be lower
        zkoef = (self.ax.get_zbound()[0] - self.ax.get_zbound()[1]) / koef

        xkoef = (self.ax.get_xbound()[0] - self.ax.get_xbound()[1]) / koef
        ykoef = (self.ax.get_ybound()[0] - self.ax.get_ybound()[1]) / koef

        # Map an motion to keyboard shortcuts
        if event.key == self.keybindings["back"]:
            self.ax.set_ybound(self.ax.get_ybound()[
                               0] + xkoef, self.ax.get_ybound()[1] + xkoef)
        if event.key == self.keybindings["forward"]:
            self.ax.set_ybound(self.ax.get_ybound()[
                               0] - xkoef, self.ax.get_ybound()[1] - xkoef)
        if event.key == self.keybindings["left"]:
            self.ax.set_xbound(self.ax.get_xbound()[
                               0] + ykoef, self.ax.get_xbound()[1] + ykoef)
        if event.key == self.keybindings["right"]:
            self.ax.set_xbound(self.ax.get_xbound()[
                               0] - ykoef, self.ax.get_xbound()[1] - ykoef)
        if event.key == self.keybindings["down"]:
            self.ax.set_zbound(self.ax.get_zbound()[
                               0] - zkoef, self.ax.get_zbound()[1] - zkoef)
        if event.key == self.keybindings["up"]:
            self.ax.set_zbound(self.ax.get_zbound()[
                               0] + zkoef, self.ax.get_zbound()[1] + zkoef)

        # update the figure to apply the movement
        self.ax.figure.canvas.draw()
