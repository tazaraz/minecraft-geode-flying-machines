

import numpy as np
from voxel import Block, BlockId, VoxelMap

class FMDirection:
    x = 1
    y = 2
    z = 4

class FlyingMachineBase:
    """
    This class contains all data to allow the algorithm to create a flying machine which feeds it needs
    The setup, consisting out of blocks is not descriptive of its appearance
    """
    x: int
    y: int
    z: int

    attach_points: list[tuple[int, int, int]] = []
    blocks: list[Block] = []
    direction: FMDirection

    size: int
    weight: int

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x, self.y, self.z = x, y, z

    def register(self, voxelmap: VoxelMap):
        for block in self.blocks:
            voxelmap.add_block(block)

class FlyingMachine1(FlyingMachineBase):
    def __init__(self, voxelmap: VoxelMap, x: int, y: int, z: int) -> None:
        super().__init__(x, y, z)
        self.attach_points = [
            Block(self.x - 1, self.y,     self.z,     BlockId.amethyst_cluster),
            Block(self.x,     self.y,     self.z - 1, BlockId.amethyst_cluster),
            Block(self.x,     self.y - 1, self.z,     BlockId.amethyst_cluster),

            Block(self.x + 2, self.y,     self.z + 1, BlockId.amethyst_cluster),
            Block(self.x + 1, self.y,     self.z + 2, BlockId.amethyst_cluster),
            Block(self.x + 1, self.y - 1, self.z + 1, BlockId.amethyst_cluster),
        ]

        self.blocks = [
            Block(self.x,     self.y,     self.z,     BlockId.slime),
            Block(self.x + 1, self.y,     self.z + 1, BlockId.slime),
            Block(self.x + 1, self.y,     self.z,     BlockId.piston),
            Block(self.x,     self.y,     self.z + 1, BlockId.piston),
            Block(self.x + 1, self.y + 1, self.z + 1, BlockId.observer),
            Block(self.x,     self.y + 1, self.z,     BlockId.observer),
        ]

        # Weight is the (total block count / 2) of the flying machine
        # as it actually consists of two parts
        self.weight = 3
        self.size = (2, 2, 2)
        self.direction = FMDirection.x | FMDirection.y

        self.register(voxelmap)

class FlyingMachine2(FlyingMachineBase):
    def __init__(self, voxelmap: VoxelMap, x: int, y: int, z: int) -> None:
        super().__init__(x, y, z)
        self.attach_points = [
            Block(self.x - 1, self.y + 1, self.z,     BlockId.amethyst_cluster),
            Block(self.x,     self.y + 1, self.z - 1, BlockId.amethyst_cluster),
            Block(self.x,     self.y + 2, self.z,     BlockId.amethyst_cluster),

            Block(self.x + 2, self.y + 1, self.z + 1, BlockId.amethyst_cluster),
            Block(self.x + 1, self.y + 1, self.z + 2, BlockId.amethyst_cluster),
            Block(self.x + 1, self.y + 2, self.z + 1, BlockId.amethyst_cluster),
        ]

        self.blocks = [
            Block(self.x,     self.y + 1, self.z + 1, BlockId.piston),
            Block(self.x + 1, self.y + 1, self.z,     BlockId.piston),
            Block(self.x,     self.y + 1, self.z,     BlockId.slime),
            Block(self.x + 1, self.y + 1, self.z + 1, BlockId.slime),
            Block(self.x,     self.y,     self.z,     BlockId.observer),
            Block(self.x + 1, self.y,     self.z + 1, BlockId.observer),
        ]

        # Weight is the (total block count / 2) of the flying machine
        # as it actually consists of two parts
        self.weight = 3
        self.size = (2, 2, 2)
        self.direction = FMDirection.x | FMDirection.y

        self.register(voxelmap)
