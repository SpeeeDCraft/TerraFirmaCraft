package net.dries007.tfc.world.layer;

import net.minecraft.world.gen.INoiseRandom;
import net.minecraft.world.gen.layer.traits.ICastleTransformer;

import static net.dries007.tfc.world.layer.TFCLayerUtil.LAKE;
import static net.dries007.tfc.world.layer.TFCLayerUtil.LARGE_LAKE_MARKER;

public enum LargeLakeLayer implements ICastleTransformer
{
    INSTANCE;

    @Override
    public int apply(INoiseRandom context, int north, int west, int south, int east, int center)
    {
        if (center == LARGE_LAKE_MARKER)
        {
            return LAKE;
        }
        if (TFCLayerUtil.isLakeCompatible(center) && (north == LARGE_LAKE_MARKER || west == LARGE_LAKE_MARKER || south == LARGE_LAKE_MARKER || east == LARGE_LAKE_MARKER) && context.nextRandom(4) != 0)
        {
            return LAKE;
        }
        return center;
    }
}