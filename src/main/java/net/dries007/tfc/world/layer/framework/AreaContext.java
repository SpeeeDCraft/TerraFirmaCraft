/*
 * Licensed under the EUPL, Version 1.2.
 * You may obtain a copy of the Licence at:
 * https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
 */

package net.dries007.tfc.world.layer.framework;

import net.minecraft.world.level.levelgen.SimpleRandomSource;

import it.unimi.dsi.fastutil.HashCommon;

public class AreaContext extends SimpleRandomSource
{
    private final long seed;

    public AreaContext(long seed)
    {
        super(seed);
        this.seed = HashCommon.murmurHash3(seed);
    }

    public void setSeed(long x, long z)
    {
        setSeed(((x * 501125321L) ^ (z * 1136930381L) ^ seed) * 0x27d4eb2d);
    }

    public int choose(int first, int second)
    {
        return nextBoolean() ? first : second;
    }

    public int choose(int first, int second, int third, int fourth)
    {
        return switch (nextInt(4))
            {
                case 0 -> first;
                case 1 -> second;
                case 2 -> third;
                default -> fourth;
            };
    }

    public <A> A choose(A first, A second)
    {
        return nextBoolean() ? first : second;
    }

    public <A> A choose(A first, A second, A third, A fourth)
    {
        return switch (nextInt(4))
            {
                case 0 -> first;
                case 1 -> second;
                case 2 -> third;
                default -> fourth;
            };
    }
}