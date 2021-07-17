/*
 * Licensed under the EUPL, Version 1.2.
 * You may obtain a copy of the Licence at:
 * https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
 */

package net.dries007.tfc.common.tileentity;

import javax.annotation.Nullable;

import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.inventory.InventoryHelper;
import net.minecraft.inventory.container.Container;
import net.minecraft.item.ItemStack;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.TranslationTextComponent;
import net.minecraftforge.fluids.FluidStack;
import net.minecraftforge.fluids.capability.CapabilityFluidHandler;
import net.minecraftforge.fluids.capability.IFluidHandler;
import net.minecraftforge.items.ItemStackHandler;

import net.dries007.tfc.common.capabilities.heat.HeatCapability;
import net.dries007.tfc.common.container.FirepitContainer;
import net.dries007.tfc.common.recipes.HeatingRecipe;
import net.dries007.tfc.common.recipes.ItemStackRecipeWrapper;

import static net.dries007.tfc.TerraFirmaCraft.MOD_ID;

public class FirePitTileEntity extends AbstractFirepitTileEntity<ItemStackHandler>
{
    private static final ITextComponent NAME = new TranslationTextComponent(MOD_ID + ".tile_entity.firepit");

    public FirePitTileEntity()
    {
        super(TFCTileEntities.FIREPIT.get(), defaultInventory(7), NAME);
    }

    @Override
    protected void handleCooking()
    {
        if (temperature > 0)
        {
            final ItemStack inputStack = inventory.getStackInSlot(SLOT_ITEM_INPUT);
            inputStack.getCapability(HeatCapability.CAPABILITY).ifPresent(cap -> {
                float itemTemp = cap.getTemperature();
                HeatCapability.addTemp(cap, temperature);

                if (cachedRecipe != null && cachedRecipe.isValidTemperature(itemTemp))
                {
                    HeatingRecipe recipe = cachedRecipe;
                    ItemStackRecipeWrapper wrapper = new ItemStackRecipeWrapper(inputStack);

                    // Clear input
                    inventory.setStackInSlot(SLOT_ITEM_INPUT, ItemStack.EMPTY);

                    // Handle outputs
                    mergeOutputStack(recipe.assemble(wrapper));
                    mergeOutputFluids(recipe.getOutputFluid(wrapper), cap.getTemperature());
                }
            });
        }
    }

    protected void coolInstantly()
    {
        inventory.getStackInSlot(SLOT_ITEM_INPUT).getCapability(HeatCapability.CAPABILITY).ifPresent(cap -> cap.setTemperature(0f));
    }

    @Nullable
    @Override
    public Container createMenu(int windowID, PlayerInventory playerInv, PlayerEntity player)
    {
        return new FirepitContainer(this, playerInv, windowID);
    }

    /**
     * Merge an item stack into the two output slots
     */
    private void mergeOutputStack(ItemStack outputStack)
    {
        outputStack = inventory.insertItem(SLOT_OUTPUT_1, outputStack, false);
        if (outputStack.isEmpty())
        {
            return;
        }
        outputStack = inventory.insertItem(SLOT_OUTPUT_2, outputStack, false);
        if (outputStack.isEmpty())
        {
            return;
        }

        assert level != null;
        InventoryHelper.dropItemStack(level, worldPosition.getX(), worldPosition.getY(), worldPosition.getZ(), outputStack);
    }

    /**
     * Merge a fluid stack into the two output slots, treating them as fluid containers, and optionally heat containers
     */
    private void mergeOutputFluids(FluidStack fluidStack, float temperature)
    {
        fluidStack = mergeOutputFluidIntoSlot(fluidStack, temperature, SLOT_OUTPUT_1);
        if (fluidStack.isEmpty())
        {
            return;
        }
        mergeOutputFluidIntoSlot(fluidStack, temperature, SLOT_OUTPUT_2);
        // Any remaining fluid is lost at this point
    }

    private FluidStack mergeOutputFluidIntoSlot(FluidStack fluidStack, float temperature, int slot)
    {
        final ItemStack mergeStack = inventory.getStackInSlot(slot);
        return mergeStack.getCapability(CapabilityFluidHandler.FLUID_HANDLER_CAPABILITY).map(fluidCap -> {
            int filled = fluidCap.fill(fluidStack, IFluidHandler.FluidAction.EXECUTE);
            if (filled > 0)
            {
                mergeStack.getCapability(HeatCapability.CAPABILITY).ifPresent(heatCap -> heatCap.setTemperature(temperature));
            }
            FluidStack remainder = fluidStack.copy();
            remainder.shrink(filled);
            return remainder;
        }).orElse(FluidStack.EMPTY);
    }
}
