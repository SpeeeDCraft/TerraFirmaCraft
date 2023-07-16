package net.dries007.tfc.client.particle;

import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.particle.CherryParticle;
import net.minecraft.client.particle.Particle;
import net.minecraft.client.particle.ParticleProvider;
import net.minecraft.client.particle.SpriteSet;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.BlockParticleOption;
import net.minecraft.world.level.block.state.BlockState;

import net.dries007.tfc.client.TFCColors;
import net.dries007.tfc.common.TFCTags;
import net.dries007.tfc.common.blocks.plant.fruit.FruitTreeLeavesBlock;
import net.dries007.tfc.util.Helpers;

public class FallingLeafParticle extends CherryParticle
{
    protected FallingLeafParticle(ClientLevel level, double x, double y, double z, SpriteSet set, boolean tinted, BlockState state)
    {
        super(level, x, y, z, set);

        final BlockPos pos = BlockPos.containing(x, y, z);

        int color = -1;
        if (state.getBlock() instanceof FruitTreeLeavesBlock fruit)
        {
            color = fruit.getFlowerColor();
        }
        else if (tinted)
        {
            color = Helpers.isBlock(state, TFCTags.Blocks.SEASONAL_LEAVES) ? TFCColors.getSeasonalFoliageColor(pos, 0) : TFCColors.getFoliageColor(pos, 0);
        }

        if (color != -1)
        {
            setColor(((color >> 16) & 0xFF) / 255F, ((color >> 8) & 0xFF) / 255F, (color & 0xFF) / 255F);
        }
    }

    public record Provider(SpriteSet set, boolean tinted) implements ParticleProvider<BlockParticleOption>
    {
        @Override
        public Particle createParticle(BlockParticleOption type, ClientLevel level, double x, double y, double z, double xSpeed, double ySpeed, double zSpeed)
        {
            return new FallingLeafParticle(level, x, y, z, set, tinted, type.getState());
        }
    }
}