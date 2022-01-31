import numpy as np

from draw import Render

# The values here also indicate wich blocks are less important,
# with slime and honey only needing to render for visuals, and amethyst being the most important
class BlockId:
    air = 0
    amethyst_cluster = 1
    amethyst = 2
    # These values map directly to VoxelMap.block_config,
    # so a value of -1 translates to block_config[-1]
    # How much the algorithm likes this spot
    slime = -5
    honey = -4
    slightly = -3
    moderately = -2
    extremely = -1

class Block:
    x: int
    y: int
    z: int
    id: BlockId

    def __init__(self, x, y, z, id, color_multiplier=1) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.id = id

class VoxelMap:
    size: int
    voxels: np.ndarray
    blocks: list[Block] = []

    # Lowest point of the working space
    min = None
    # Highest point of the working space
    max = None

    # Corresponds to every BlockId
    block_config = [
        {'color': [0, 0, 0, 0]},
        {'color': [0.58, 0, 0.83, 0.3]},
        {'color': [0.29, 0, 0.51, 1]},
        {'color': 'lime'},
        {'color': 'yellow'},
        {'color': [1, 1, 0, 0.03]},
        {'color': [1, 0.5, 0, 0.07]},
        {'color': [1, 0, 0, 0.1]},
    ]

    def __init__(self, file=None, amethyst_positions: list[tuple[int, int, int]] = None, size=10) -> None:
        # TODO: implement file loading in
        # preferably directly from a litematic file
        if file is not None:
            pass

        elif amethyst_positions is not None:
            # Load amethyst positions from a list
            for position in amethyst_positions:
                block = Block(*position, BlockId.amethyst)
                if self.min is None:
                    self.min, self.max = block, block
                elif block.x < self.min.x or block.y < self.min.y or block.z < self.min.z:
                    self.min = block
                elif block.x > self.max.x or block.y > self.max.y or block.z > self.max.z:
                    self.max = block

                self.add_block(block)

        else:
            self.size = size
            self.voxels = np.zeros((size, size, size), dtype=np.int64)

    def add_block(self, block: Block) -> None:
        # Append if not already filled up
        # Allow overwriting air blocks and amethyst clusters
        if 0 <= block.x < self.size and 0 <= block.y < self.size and 0 <= block.z < self.size and \
               (self.voxels[block.x][block.y][block.z] == BlockId.air or \
                self.voxels[block.x][block.y][block.z] == BlockId.amethyst_cluster):
            self.voxels[block.x][block.y][block.z] = block.id
            self.blocks.append(Block(block.x, block.y, block.z, block.id))

            # Add surrounding blocks which would contain clusters
            if block.id == BlockId.amethyst:
                self.add_block(Block(block.x - 1, block.y, block.z, BlockId.amethyst_cluster))
                self.add_block(Block(block.x + 1, block.y, block.z, BlockId.amethyst_cluster))
                self.add_block(Block(block.x, block.y - 1, block.z, BlockId.amethyst_cluster))
                self.add_block(Block(block.x, block.y + 1, block.z, BlockId.amethyst_cluster))
                self.add_block(Block(block.x, block.y, block.z - 1, BlockId.amethyst_cluster))
                self.add_block(Block(block.x, block.y, block.z + 1, BlockId.amethyst_cluster))

    def flatten_side(self, axis="x") -> np.ndarray:
        side = np.zeros((self.size, self.size), dtype=np.int64)

        # Config for how to extract the correct data
        if axis == "x":
            i1, i2 = "x", "z"
        elif axis == "y":
            i1, i2 = "y", "z"
        else:
            i1, i2, = "x", "y"

        for block in self.blocks:
            b = side[getattr(block, i1)][getattr(block, i2)]

            # Here becomes apparent why the BlockId of honey and slime are less than air:
            # We don't want it rendered in the flattening
            if b < block.id:
                side[getattr(block, i1)][getattr(block, i2)] = block.id

        return np.rot90(np.fliplr(side))


    @staticmethod
    def distance_2d(block1: Block, block2: Block, axis="x") -> int:
        if axis == "x":
            return np.abs(block1.x - block2.x) + np.abs(block1.z - block2.z)
        elif axis == "y":
            return np.abs(block1.y - block2.y) + np.abs(block1.z - block2.z)
        else:
            return np.abs(block1.x - block2.x) + np.abs(block1.y - block2.y)

    @staticmethod
    def distance_3d(block1: Block, block2: Block) -> int:
        """ Returns the distance from block 1 to block 2 """
        return np.abs(block1.x - block2.x) + np.abs(block1.y - block2.y) + np.abs(block1.z - block2.z)
