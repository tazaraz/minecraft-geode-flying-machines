import numpy as np
from draw import Render
from flyingMachines import FlyingMachine
from voxel import Block, BlockId, VoxelMap

def liking_scale(value):
    if value == 0 or value == 1:
        return BlockId.extremely
    elif value == 2:
        return BlockId.moderately
    elif value == 3:
        return BlockId.slightly
    else:
        return BlockId.air

if __name__ == "__main__":
    size = 20
    v = VoxelMap(size=size)
    v.add_block(Block(10, 10, 10, BlockId.amethyst))
    v.add_block(Block(13, 13, 12, BlockId.amethyst))
    v.add_block(Block(14, 14, 16, BlockId.amethyst))
    v.add_block(Block(15, 17, 16, BlockId.amethyst))
    fm = FlyingMachine(v, 2, 2, 2)

    side = v.flatten_side("x", show_hidden=True)

    print(side)

    # scores = np.zeros((size, size, size), dtype=np.int64)
    # for x in range(size):
    #     for y in range(size):
    #         for z in range(size):
    #             closest = None
    #             for block in v.blocks:
    #                 if closest is None:
    #                     closest = VoxelMap.distance_3d(Block(x, y, z, 0), block)
    #                 else:
    #                     closest = min(closest, VoxelMap.distance_3d(Block(x, y, z, 0), block))
    #             scores[x][y][z] = closest
    #             if v.voxels[x][y][z] == BlockId.air:
    #                 v.voxels[x][y][z] = liking_scale(closest)

    v.render()