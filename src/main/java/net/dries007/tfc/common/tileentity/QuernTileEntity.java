package net.dries007.tfc.common.tileentity;

import net.minecraft.block.BlockState;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.inventory.InventoryHelper;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.CompoundNBT;
import net.minecraft.particles.ItemParticleData;
import net.minecraft.particles.ParticleTypes;
import net.minecraft.tileentity.ITickableTileEntity;
import net.minecraft.util.SoundCategory;
import net.minecraft.util.SoundEvents;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.TranslationTextComponent;

import net.dries007.tfc.common.TFCTags;
import net.dries007.tfc.common.items.TFCItems;
import net.dries007.tfc.util.Helpers;

import static net.dries007.tfc.TerraFirmaCraft.MOD_ID;

public class QuernTileEntity extends InventoryTileEntity implements ITickableTileEntity
{
    private static final ITextComponent NAME = new TranslationTextComponent(MOD_ID + ".tile_entity.quern");

    public static final int SLOT_HANDSTONE = 0;
    public static final int SLOT_INPUT = 1;
    public static final int SLOT_OUTPUT = 2;

    private int rotationTimer;
    private boolean hasHandstone;

    public QuernTileEntity()
    {
        super(TFCTileEntities.QUERN.get(), 3, NAME);
        rotationTimer = 0;
    }

    public ItemStack insertOrSwapItem(int slot, ItemStack playerStack)
    {
        ItemStack quernStack = inventory.getStackInSlot(slot);

        if (quernStack.isEmpty() || (playerStack.isStackable() && quernStack.isStackable() && quernStack.getItem() == playerStack.getItem() && ItemStack.tagMatches(playerStack, quernStack)))
        {
            return inventory.insertItem(slot, playerStack, false);
        }
        inventory.setStackInSlot(slot, playerStack);
        return quernStack;
    }

    @Override
    public int getSlotStackLimit(int slot)
    {
        return slot == SLOT_HANDSTONE ? 1 : 64;
    }

    @Override
    public boolean isItemValid(int slot, ItemStack stack)
    {
        switch (slot)
        {
            case SLOT_HANDSTONE:
                return stack.getItem().is(TFCTags.Items.HANDSTONE); // needs to be handstone
            case SLOT_INPUT:
                return true; // recipe must exist
            default:
                return false;
        }
    }

    @Override
    public void setAndUpdateSlots(int slot)
    {
        markForBlockUpdate();
        if (slot == SLOT_HANDSTONE)
        {
            hasHandstone = inventory.getStackInSlot(SLOT_HANDSTONE).getItem().is(TFCTags.Items.HANDSTONE);
        }
        super.setAndUpdateSlots(slot);
    }

    @Override
    public void load(BlockState state, CompoundNBT nbt)
    {
        rotationTimer = nbt.getInt("rotationTimer");
        super.load(state, nbt);
        hasHandstone = inventory.getStackInSlot(SLOT_HANDSTONE).getItem().is(TFCTags.Items.HANDSTONE);
    }

    @Override
    public CompoundNBT save(CompoundNBT nbt)
    {
        nbt.putInt("rotationTimer", rotationTimer);
        return super.save(nbt);
    }

    @Override
    public boolean canInteractWith(PlayerEntity player)
    {
        return super.canInteractWith(player) && rotationTimer == 0;
    }

    public int getRotationTimer()
    {
        return rotationTimer;
    }

    public boolean isGrinding()
    {
        return rotationTimer > 0;
    }

    public boolean hasHandstone()
    {
        return hasHandstone;
    }

    public void grind()
    {
        this.rotationTimer = 90;
        markForBlockUpdate();
    }

    @Override
    public void tick()
    {
        if (rotationTimer > 0)
        {
            rotationTimer--;
            assert level != null;
            if (level.random.nextFloat() < 0.3F)
            {
                addParticle(inventory.getStackInSlot(SLOT_INPUT));
            }
            if (rotationTimer == 0)
            {
                grindItem();
                Helpers.playSound(level, worldPosition, SoundEvents.ARMOR_STAND_FALL);
                Helpers.damageItem(inventory.getStackInSlot(SLOT_HANDSTONE), 1);

                if (inventory.getStackInSlot(SLOT_HANDSTONE).isEmpty())
                {
                    for (int i = 0; i < 15; i++)
                    {
                        if (level.isClientSide)
                        {
                            addParticle(new ItemStack(TFCItems.HANDSTONE.get()));
                        }
                    }
                    Helpers.playSound(level, worldPosition, SoundEvents.STONE_BREAK);
                    Helpers.playSound(level, worldPosition, SoundEvents.ITEM_BREAK);
                }
                setAndUpdateSlots(SLOT_HANDSTONE);
            }
        }
    }

    private void addParticle(ItemStack item)
    {
        assert level != null;
        level.addParticle(new ItemParticleData(ParticleTypes.ITEM, item), worldPosition.getX() + 0.5D, worldPosition.getY() + 0.875D, worldPosition.getZ() + 0.5D, Helpers.fastGaussian(level.random) / 2.0D, level.random.nextDouble() / 4.0D, Helpers.fastGaussian(level.random) / 2.0D);
    }

    private void grindItem()
    {
        ItemStack inputStack = inventory.getStackInSlot(SLOT_INPUT);
        if (!inputStack.isEmpty())
        {
            /*QuernRecipe recipe = QuernRecipe.get(inputStack);
            if (recipe != null && level != null && !level.isClientSide)
            {
                inputStack.shrink(recipe.getIngredients().get(0).getAmount());
                ItemStack outputStack = recipe.getOutputItem(inputStack);
                outputStack = inventory.insertItem(SLOT_OUTPUT, outputStack, false);
                //todo inventory.setStackInSlot(SLOT_OUTPUT, CapabilityFood.mergeItemStacksIgnoreCreationDate(inventory.getStackInSlot(SLOT_OUTPUT), outputStack));
                inventory.setStackInSlot(SLOT_OUTPUT, outputStack);
                if (!outputStack.isEmpty())
                {
                    // Still having leftover items, dumping in world
                    Helpers.spawnItem(level, worldPosition, outputStack);
                }
            }*/
        }
    }
}