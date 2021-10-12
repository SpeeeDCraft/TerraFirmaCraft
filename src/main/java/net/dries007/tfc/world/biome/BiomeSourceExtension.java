/*
 * Licensed under the EUPL, Version 1.2.
 * You may obtain a copy of the Licence at:
 * https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
 */

package net.dries007.tfc.world.biome;

import java.util.Random;
import java.util.function.Predicate;
import javax.annotation.Nullable;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.BiomeSource;

import net.dries007.tfc.world.chunkdata.ChunkDataProvider;
import net.dries007.tfc.world.settings.ClimateSettings;
import net.dries007.tfc.world.settings.RockLayerSettings;

public interface BiomeSourceExtension
{
    int getSpawnDistance();

    int getSpawnCenterX();

    int getSpawnCenterZ();

    ChunkDataProvider getChunkDataProvider();

    RockLayerSettings getRockLayerSettings();

    ClimateSettings getTemperatureSettings();

    /**
     * An optional implementation, see {@link TFCBiomeSource}
     */
    @Nullable
    default BlockPos findBiomeIgnoreClimate(int x, int y, int z, int radius, int increment, Predicate<Biome> predicate, Random rand)
    {
        return self().findBiomeHorizontal(x, y, z, radius, increment, predicate, rand, false);
    }

    /**
     * @return itself, or the underlying biome provider / source
     */
    default BiomeSource self()
    {
        return (BiomeSource) this;
    }
}