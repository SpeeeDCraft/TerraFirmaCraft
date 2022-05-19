#  Work under Copyright. Licensed under the EUPL.
#  See the project README.md and LICENSE.txt for more information.

from enum import Enum

from mcresources import ResourceManager, RecipeContext, utils
from mcresources.type_definitions import ResourceIdentifier, Json

from constants import *


class Rules(Enum):
    hit_any = 'hit_any'
    hit_not_last = 'hit_not_last'
    hit_last = 'hit_last'
    hit_second_last = 'hit_second_last'
    hit_third_last = 'hit_third_last'
    draw_any = 'draw_any'
    draw_last = 'draw_last'
    draw_not_last = 'draw_not_last'
    draw_second_last = 'draw_second_last'
    draw_third_last = 'draw_third_last'
    punch_any = 'punch_any'
    punch_last = 'punch_last'
    punch_not_last = 'punch_not_last'
    punch_second_last = 'punch_second_last'
    punch_third_last = 'punch_third_last'
    bend_any = 'bend_any'
    bend_last = 'bend_last'
    bend_not_last = 'bend_not_last'
    bend_second_last = 'bend_second_last'
    bend_third_last = 'bend_third_last'
    upset_any = 'upset_any'
    upset_last = 'upset_last'
    upset_not_last = 'upset_not_last'
    upset_second_last = 'upset_second_last'
    upset_third_last = 'upset_third_last'
    shrink_any = 'shrink_any'
    shrink_last = 'shrink_last'
    shrink_not_last = 'shrink_not_last'
    shrink_second_last = 'shrink_second_last'
    shrink_third_last = 'shrink_third_last'


def generate(rm: ResourceManager):
    # Rock Things
    for rock in ROCKS.keys():

        cobble = 'tfc:rock/cobble/%s' % rock
        raw = 'tfc:rock/raw/%s' % rock
        loose = 'tfc:rock/loose/%s' % rock
        hardened = 'tfc:rock/hardened/%s' % rock
        bricks = 'tfc:rock/bricks/%s' % rock
        smooth = 'tfc:rock/smooth/%s' % rock
        cracked_bricks = 'tfc:rock/cracked_bricks/%s' % rock
        chiseled = 'tfc:rock/chiseled/%s' % rock

        brick = 'tfc:brick/%s' % rock

        # Cobble <-> Loose Rocks
        rm.crafting_shapeless('crafting/rock/%s_cobble_to_loose_rocks' % rock, cobble, (4, loose)).with_advancement(cobble)
        rm.crafting_shaped('crafting/rock/%s_loose_rocks_to_cobble' % rock, ['XX', 'XX'], loose, cobble).with_advancement(loose)

        # Stairs, Slabs and Walls
        for block_type in CUTTABLE_ROCKS:
            block = 'tfc:rock/%s/%s' % (block_type, rock)

            rm.crafting_shaped('crafting/rock/%s_%s_slab' % (rock, block_type), ['XXX'], block, (6, block + '_slab')).with_advancement(block)
            rm.crafting_shaped('crafting/rock/%s_%s_stairs' % (rock, block_type), ['X  ', 'XX ', 'XXX'], block, (8, block + '_stairs')).with_advancement(block)
            rm.crafting_shaped('crafting/rock/%s_%s_wall' % (rock, block_type), ['XXX', 'XXX'], block, (6, block + '_wall')).with_advancement(block)

            # Vanilla allows stone cutting from any -> any, we only allow stairs/slabs/walls as other variants require mortar / chisel
            stone_cutting(rm, 'rock/%s_%s_slab' % (rock, block_type), block, block + '_slab', 2).with_advancement(block)
            stone_cutting(rm, 'rock/%s_%s_stairs' % (rock, block_type), block, block + '_stairs', 1).with_advancement(block)
            stone_cutting(rm, 'rock/%s_%s_wall' % (rock, block_type), block, block + '_wall', 1).with_advancement(block)

        # Other variants
        damage_shapeless(rm, 'crafting/rock/%s_smooth' % rock, (raw, '#tfc:chisels'), smooth).with_advancement(raw)
        damage_shapeless(rm, 'crafting/rock/%s_brick' % rock, (loose, '#tfc:chisels'), brick).with_advancement(loose)
        damage_shapeless(rm, 'crafting/rock/%s_chiseled' % rock, (smooth, '#tfc:chisels'), chiseled).with_advancement(smooth)
        damage_shapeless(rm, 'crafting/rock/%s_button' % rock, ('#tfc:chisels', brick), 'tfc:rock/button/%s' % rock).with_advancement(brick)
        damage_shapeless(rm, 'crafting/rock/%s_pressure_plate' % rock, ('#tfc:chisels', brick, brick), 'tfc:rock/pressure_plate/%s' % rock).with_advancement(brick)

        rm.crafting_shaped('crafting/rock/%s_hardened' % rock, ['XMX', 'MXM', 'XMX'], {'X': raw, 'M': '#tfc:mortar'}, (2, hardened)).with_advancement(raw)
        rm.crafting_shaped('crafting/rock/%s_bricks' % rock, ['XMX', 'MXM', 'XMX'], {'X': brick, 'M': '#tfc:mortar'}, (4, bricks)).with_advancement(brick)

        damage_shapeless(rm, 'crafting/rock/%s_cracked' % rock, (bricks, '#tfc:hammers'), cracked_bricks).with_advancement(bricks)

    for metal, metal_data in METALS.items():
        if 'utility' in metal_data.types:
            rm.crafting_shaped('crafting/metal/anvil/%s' % metal, ['XXX', ' X ', 'XXX'], {'X': 'tfc:metal/double_ingot/%s' % metal}, 'tfc:metal/anvil/%s' % metal).with_advancement('tfc:metal/double_ingot/%s' % metal)
        if 'tool' in metal_data.types:
            for tool in METAL_TOOL_HEADS:
                suffix = '_blade' if tool in ('knife', 'saw', 'scythe', 'sword') else '_head'
                advanced_shaped(rm, 'crafting/metal/%s/%s' % (tool, metal), ['X', 'Y'], {'X': 'tfc:metal/%s%s/%s' % (tool, suffix, metal), 'Y': '#forge:rods/wooden'}, item_stack_provider('tfc:metal/%s/%s' % (tool, metal), copy_forging=True), (0, 0)).with_advancement('tfc:metal/%s%s/%s' % (tool, suffix, metal))

    unsalted_raw_meat = not_rotten(has_trait('#tfc:foods/raw_meats', 'tfc:salted', invert=True))
    advanced_shapeless(rm, 'crafting/salting', (unsalted_raw_meat, 'tfc:powder/salt'), item_stack_provider(copy_input=True, add_trait='tfc:salted'), unsalted_raw_meat).with_advancement('tfc:powder/salt')
    rm.crafting_shaped('crafting/wood/stick_from_twigs', ['X', 'X'], {'X': '#tfc:twigs'}, 'minecraft:stick')  # todo: advancement?

    for wood in WOODS.keys():
        def item(thing: str):
            return 'tfc:wood/%s/%s' % (thing, wood)

        def plank(thing: str):
            return 'tfc:wood/planks/%s_%s' % (wood, thing)

        rm.crafting_shaped('crafting/wood/%s_bookshelf' % wood, ['XXX', 'YYY', 'XXX'], {'X': item('planks'), 'Y': 'minecraft:book'}, plank('bookshelf')).with_advancement('minecraft:book')
        rm.crafting_shapeless('crafting/wood/%s_button' % wood, item('planks'), plank('button')).with_advancement(item('planks'))
        rm.crafting_shaped('crafting/wood/%s_door' % wood, ['XX', 'XX', 'XX'], {'X': item('lumber')}, (2, plank('door'))).with_advancement(item('lumber'))
        rm.crafting_shaped('crafting/wood/%s_fence' % wood, ['XYX', 'XYX'], {'X': item('planks'), 'Y': item('lumber')}, (8, plank('fence'))).with_advancement(item('lumber'))
        rm.crafting_shaped('crafting/wood/%s_log_fence' % wood, ['XYX', 'XYX'], {'X': item('log'), 'Y': item('lumber')}, (8, plank('log_fence'))).with_advancement(item('lumber'))
        rm.crafting_shaped('crafting/wood/%s_fence_gate' % wood, ['YXY', 'YXY'], {'X': item('planks'), 'Y': item('lumber')}, (2, plank('fence_gate'))).with_advancement(item('lumber'))
        damage_shapeless(rm, 'crafting/wood/%s_lumber_log' % wood, (item('log'), '#tfc:saws'), (8, item('lumber'))).with_advancement(item('log'))
        damage_shapeless(rm, 'crafting/wood/%s_lumber_planks' % wood, (item('planks'), '#tfc:saws'), (4, item('lumber'))).with_advancement(item('planks'))
        rm.crafting_shaped('crafting/wood/%s_stairs' % wood, ['X  ', 'XX ', 'XXX'], {'X': item('planks')}, (8, plank('stairs'))).with_advancement(item('planks'))
        rm.crafting_shaped('crafting/wood/%s_slab' % wood, ['XXX'], {'X': item('planks')}, (6, plank('slab'))).with_advancement(item('planks'))
        rm.crafting_shaped('crafting/wood/%s_planks' % wood, ['XX', 'XX'], {'X': item('lumber')}, item('planks')).with_advancement(item('lumber'))
        rm.crafting_shaped('crafting/wood/%s_tool_rack' % wood, ['XXX', '   ', 'XXX'], {'X': item('lumber')}, plank('tool_rack')).with_advancement(item('lumber'))
        rm.crafting_shaped('crafting/wood/%s_trapdoor' % wood, ['XXX', 'XXX'], {'X': item('lumber')}, (3, plank('trapdoor'))).with_advancement(item('lumber'))
        rm.crafting_shaped('crafting/wood/%s_workbench' % wood, ['XX', 'XX'], {'X': item('planks')}, plank('workbench')).with_advancement(item('planks'))
        rm.crafting_shaped('crafting/wood/%s_pressure_plate' % wood, ['XX'], {'X': item('lumber')}, plank('pressure_plate')).with_advancement(item('lumber'))
        rm.crafting_shaped('crafting/wood/%s_boat' % wood, ['X X', 'XXX'], {'X': item('planks')}, item('boat')).with_advancement(item('planks'))
        rm.crafting_shaped('crafting/wood/%s_chest' % wood, ['XXX', 'X X', 'XXX'], {'X': item('lumber')}, item('chest')).with_advancement(item('lumber'))
        rm.crafting_shapeless('crafting/wood/%s_trapped_chest' % wood, (item('chest'), 'minecraft:tripwire_hook'), (1, item('trapped_chest'))).with_advancement(item('chest'))
        damage_shapeless(rm, 'crafting/wood/%s_support' % wood, (item('log'), item('log'), '#tfc:saws'), (8, item('support'))).with_advancement('#tfc:saws')
        rm.crafting_shaped('crafting/wood/%s_loom' % wood, ['XXX', 'XSX', 'X X'], {'X': item('lumber'), 'S': 'minecraft:stick'}, plank('loom')).with_advancement(item('lumber'))
        rm.crafting_shaped('crafting/wood/%s_sluice' % wood, ['  X', ' XY', 'XYY'], {'X': '#forge:rods/wooden', 'Y': item('lumber')}, item('sluice')).with_advancement(item('lumber'))
        rm.crafting_shaped('crafting/wood/%s_sign' % wood, ['XXX', 'XXX', ' Y '], {'X': item('lumber'), 'Y': '#forge:rods/wooden'}, (3, item('sign'))).with_advancement(item('lumber'))
        rm.crafting_shaped('crafting/wood/%s_barrel' % wood, ['X X', 'X X', 'XXX'], {'X': item('lumber')}, item('barrel')).with_advancement(item('lumber'))

    rm.crafting_shaped('crafting/aggregate', ['XYX', 'Y Y', 'XYX'], {'X': '#forge:sand', 'Y': '#forge:gravel'}, (8, 'tfc:aggregate')).with_advancement('#forge:sand')
    damage_shapeless(rm, 'crafting/alabaster_brick', ('tfc:ore/gypsum', '#tfc:chisels'), (4, 'tfc:alabaster_brick')).with_advancement('tfc:ore/gypsum')
    rm.crafting_shaped('crafting/alabaster_bricks', ['XYX', 'YXY', 'XYX'], {'X': 'tfc:alabaster_brick', 'Y': '#tfc:mortar'}, (4, 'tfc:alabaster/raw/alabaster_bricks')).with_advancement('tfc:alabaster_brick')
    rm.crafting_shaped('crafting/bellows', ['XXX', 'YYY', 'XXX'], {'X': '#tfc:lumber', 'Y': '#forge:leather'}, 'tfc:bellows').with_advancement('#forge:leather')
    rm.crafting_shaped('crafting/bricks', ['XYX', 'YXY', 'XYX'], {'X': 'minecraft:brick', 'Y': '#tfc:mortar'}, (2, 'minecraft:bricks')).with_advancement('minecraft:brick')
    rm.crafting_shaped('crafting/fire_bricks', ['XYX', 'YXY', 'XYX'], {'X': 'tfc:ceramic/fire_brick', 'Y': '#tfc:mortar'}, (2, 'tfc:fire_bricks')).with_advancement('minecraft:brick')
    rm.crafting_shaped('crafting/fire_clay', ['XYX', 'YZY', 'XYX'], {'X': 'tfc:powder/kaolinite', 'Y': 'tfc:powder/graphite', 'Z': 'minecraft:clay_ball'}, 'tfc:fire_clay').with_advancement('tfc:powder/kaolinite')
    rm.crafting_shaped('crafting/fire_clay_block', ['XX', 'XX'], {'X': 'tfc:fire_clay'}, 'tfc:fire_clay_block').with_advancement('tfc:fire_clay')
    rm.crafting_shaped('crafting/firestarter', [' X', 'X '], {'X': '#forge:rods/wooden'}, 'tfc:firestarter').with_advancement('#forge:rods/wooden')
    damage_shapeless(rm, 'crafting/flux', ('#tfc:fluxstone', '#tfc:hammers'), (2, 'tfc:powder/flux')).with_advancement('#tfc:fluxstone')
    rm.crafting_shapeless('crafting/gunpowder', ('tfc:powder/saltpeter', 'tfc:powder/saltpeter', 'tfc:powder/sulfur', 'tfc:powder/charcoal'), (4, 'minecraft:gunpowder')).with_advancement('tfc:powder/sulfur')
    rm.crafting_shapeless('crafting/gunpowder_graphite', ('tfc:powder/saltpeter', 'tfc:powder/saltpeter', 'tfc:powder/saltpeter', 'tfc:powder/saltpeter', 'tfc:powder/sulfur', 'tfc:powder/sulfur', 'tfc:powder/charcoal', 'tfc:powder/charcoal', 'tfc:powder/graphite'), (12, 'minecraft:gunpowder')).with_advancement('tfc:powder/graphite')
    rm.crafting_shaped('crafting/halter', ['XYX', 'X X'], {'X': '#forge:leather', 'Y': 'minecraft:lead'}, 'tfc:halter').with_advancement('minecraft:lead')
    rm.crafting_shaped('crafting/handstone', ['Y  ', 'XXX'], {'X': '#forge:stone', 'Y': '#forge:rods/wooden'}, 'tfc:handstone').with_advancement('#forge:stone')
    rm.crafting_shaped('crafting/jute_net', ['X X', ' X ', 'X X'], {'X': 'tfc:jute_fiber'}, 'tfc:jute_net').with_advancement('tfc:jute_fiber')
    rm.crafting_shaped('crafting/lead', [' XX', ' XX', 'X  '], {'X': 'tfc:jute_fiber'}, 'minecraft:lead').with_advancement('tfc:jute_fiber')
    rm.crafting_shaped('crafting/quern', ['XXX', 'YYY'], {'X': '#forge:smooth_stone', 'Y': '#forge:stone'}, 'tfc:quern').with_advancement('#forge:smooth_stone')
    rm.crafting_shaped('crafting/spindle', ['X', 'Y'], {'X': 'tfc:ceramic/spindle_head', 'Y': '#forge:rods/wooden'}, 'tfc:spindle').with_advancement('tfc:ceramic/spindle_head')
    rm.crafting_shapeless('crafting/stick_from_bunch', 'tfc:stick_bunch', (9, 'minecraft:stick')).with_advancement('tfc:stick_bunch')
    rm.crafting_shapeless('crafting/stick_from_bundle', 'tfc:stick_bundle', (18, 'minecraft:stick')).with_advancement('tfc:stick_bundle')
    rm.crafting_shaped('crafting/stick_bunch', ['XXX', 'XXX', 'XXX'], {'X': '#forge:rods/wooden'}, 'tfc:stick_bunch').with_advancement('#forge:rods/wooden')
    rm.crafting_shaped('crafting/stick_bundle', ['X', 'X'], {'X': 'tfc:stick_bunch'}, 'tfc:stick_bundle').with_advancement('tfc:stick_bunch')
    rm.crafting_shapeless('crafting/straw', 'tfc:thatch', (4, 'tfc:straw')).with_advancement('tfc:thatch')
    rm.crafting_shaped('crafting/thatch', ['XX', 'XX'], {'X': 'tfc:straw'}, 'tfc:thatch').with_advancement('tfc:straw')
    damage_shapeless(rm, 'crafting/wool_yarn', ('tfc:spindle', 'tfc:wool'), (8, 'tfc:wool_yarn')).with_advancement('tfc:wool')
    rm.crafting_shaped('crafting/wattle', ['X', 'X'], {'X': '#minecraft:logs'}, (6, 'tfc:wattle')).with_advancement('#minecraft:logs')
    rm.crafting_shapeless('crafting/daub', ('tfc:straw', 'minecraft:clay_ball', '#minecraft:dirt'), (2, 'tfc:daub')).with_advancement('tfc:straw')
    rm.crafting_shapeless('crafting/daub_from_mud', ('tfc:straw', '#tfc:mud'), (2, 'tfc:daub')).with_advancement('#tfc:mud')
    rm.crafting_shaped('crafting/composter', ['X X', 'XYX', 'XYX'], {'X': '#tfc:lumber', 'Y': '#minecraft:dirt'}, 'tfc:composter').with_advancement('#tfc:lumber')
    rm.crafting_shaped('crafting/bloomery', ['XXX', 'X X', 'XXX'], {'X': '#forge:double_sheets/any_bronze'}, 'tfc:bloomery').with_advancement('#forge:double_sheets/any_bronze')
    rm.crafting_shaped('crafting/glow_arrow', ['XXX', 'XYX', 'XXX'], {'X': 'minecraft:arrow', 'Y': 'minecraft:glow_ink_sac'}, (8, 'tfc:glow_arrow')).with_advancement('minecraft:glow_ink_sac')
    rm.crafting_shaped('crafting/wooden_bucket', ['X X', ' X '], {'X': '#tfc:lumber'}, 'tfc:wooden_bucket').with_advancement('#tfc:lumber')
    damage_shapeless(rm, 'crafting/paper', (not_rotten('tfc:food/sugarcane'), not_rotten('tfc:food/sugarcane'), not_rotten('tfc:food/sugarcane'), '#tfc:knives'), (3, 'minecraft:paper')).with_advancement('tfc:food/sugarcane')
    rm.crafting_shaped('crafting/nest_box', ['Y Y', 'XYX', 'XXX'], {'Y': 'tfc:straw', 'X': '#tfc:lumber'}, 'tfc:nest_box').with_advancement('#tfc:lumber')

    rm.crafting_shaped('crafting/vanilla/armor_stand', ['XXX', ' X ', 'XYX'], {'X': '#minecraft:planks', 'Y': '#forge:smooth_stone_slab'}, 'minecraft:armor_stand').with_advancement('#forge:smooth_stone_slab')
    rm.crafting_shaped('crafting/vanilla/armor_stand_bulk', ['X', 'Y'], {'X': 'tfc:stick_bunch', 'Y': '#forge:smooth_stone_slab'}, 'minecraft:armor_stand').with_advancement('#forge:smooth_stone_slab')
    rm.crafting_shaped('crafting/vanilla/color/white_bed', ['XXX', 'YYY'], {'X': '#tfc:high_quality_cloth', 'Y': '#tfc:lumber'}, 'minecraft:white_bed').with_advancement('#tfc:high_quality_cloth')
    # todo: this recipe is completely wrong
    #rm.crafting_shaped('crafting/vanilla/bucket', ['XRX', 'XBX', ' X '], {'X': '#forge:ingots/wrought_iron', 'R': 'tfc:bucket/metal/red_steel', 'B': 'tfc:bucket/metal/blue_steel'}, 'minecraft:bucket').with_advancement('tfc:bucket/metal/red_steel')
    rm.crafting_shaped('crafting/vanilla/cauldron', ['X X', 'X X', 'XXX'], {'X': '#forge:sheets/wrought_iron'}, 'minecraft:cauldron').with_advancement('#forge:sheets/wrought_iron')
    rm.crafting_shaped('crafting/vanilla/compass', [' X ', 'XYX', ' X '], {'X': '#forge:sheets/wrought_iron', 'Y': '#forge:dusts/redstone'}, 'minecraft:compass').with_advancement('#forge:sheets/wrought_iron')
    rm.crafting_shaped('crafting/vanilla/clock', ['RXR', 'XYX', 'RXR'], {'X': '#forge:sheets/gold', 'Y': 'tfc:brass_mechanisms', 'R': '#forge:dusts/redstone'}, 'minecraft:clock').with_advancement('#forge:sheets/gold')
    rm.crafting_shaped('crafting/vanilla/crossbow', ['LIL', 'STS', ' L '], {'L': '#tfc:lumber', 'I': '#forge:rods/wrought_iron', 'S': '#forge:string', 'T': 'minecraft:tripwire_hook'}, 'minecraft:crossbow').with_advancement('#forge:ingots/wrought_iron')
    rm.crafting_shapeless('crafting/vanilla/fire_charge', ('minecraft:gunpowder', 'tfc:firestarter', '#minecraft:coals'), (3, 'minecraft:fire_charge')).with_advancement('minecraft:gunpowder')
    rm.crafting_shaped('crafting/vanilla/flint_and_steel', ['X ', ' Y'], {'X': '#forge:ingots/steel', 'Y': 'minecraft:flint'}, 'minecraft:flint_and_steel').with_advancement('#forge:ingots/steel')
    rm.crafting_shapeless('crafting/vanilla/hay', 'minecraft:hay_block', (9, 'tfc:straw')).with_advancement('minecraft:hay_block')
    rm.crafting_shaped('crafting/vanilla/hay_bale', ['XXX', 'XXX', 'XXX'], {'X': 'tfc:straw'}, 'minecraft:hay_block').with_advancement('tfc:straw')
    rm.crafting_shaped('crafting/vanilla/item_frame', ['XXX', 'XYX', 'XXX'], {'X': '#tfc:lumber', 'Y': '#forge:leather'}, (4, 'minecraft:item_frame')).with_advancement('#forge:leather')
    rm.crafting_shaped('crafting/vanilla/ladder', ['X X', 'X X', 'X X'], {'X': '#tfc:lumber'}, (16, 'minecraft:ladder')).with_advancement('#tfc:lumber')
    rm.crafting_shaped('crafting/vanilla/lapis_block', ['XXX', 'XXX', 'XXX'], {'X': 'tfc:gem/lapis_lazuli'}, 'minecraft:lapis_block').with_advancement('tfc:gem/lapis_lazuli')
    rm.crafting_shaped('crafting/vanilla/name_tag', ['XX', 'XY', 'XX'], {'X': 'minecraft:string', 'Y': 'minecraft:paper'}, 'minecraft:name_tag')
    rm.crafting_shaped('crafting/vanilla/painting', ['XXX', 'XYX', 'XXX'], {'X': '#tfc:high_quality_cloth', 'Y': '#forge:rods/wooden'}, 'minecraft:painting').with_advancement('#tfc:high_quality_cloth')
    rm.crafting_shaped('crafting/vanilla/tnt', ['XYX', 'YXY', 'XYX'], {'X': 'minecraft:gunpowder', 'Y': 'minecraft:sand'}, 'minecraft:tnt').with_advancement('minecraft:gunpowder')
    rm.crafting_shaped('crafting/vanilla/spyglass', ['X', 'Y', 'Y'], {'Y': '#forge:sheets/copper', 'X': 'minecraft:glass_pane'}, 'minecraft:spyglass').with_advancement('#forge:sheets/copper')
    rm.crafting_shaped('crafting/vanilla/tinted_glass', [' X ', 'XYX', ' X '], {'X': 'tfc:powder/amethyst', 'Y': 'minecraft:glass'}, 'minecraft:tinted_glass').with_advancement('minecraft:glass')

    # todo: redstone lamp
    rm.crafting_shaped('crafting/vanilla/redstone/hopper', ['X X', ' Y '], {'X': '#forge:sheets/wrought_iron', 'Y': '#forge:chests/wooden'}, 'minecraft:hopper').with_advancement('#forge:sheets/wrought_iron')
    rm.crafting_shaped('crafting/vanilla/redstone/observer', ['CCC', 'RRB', 'CCC'], {'C': '#forge:cobblestone', 'R': '#forge:dusts/redstone', 'B': 'tfc:brass_mechanisms'}, 'minecraft:observer').with_advancement('tfc:brass_mechanisms')
    rm.crafting_shaped('crafting/vanilla/redstone/piston', ['WWW', 'SXS', 'SBS'], {'X': '#forge:rods/wrought_iron', 'S': '#forge:cobblestone', 'W': '#tfc:lumber', 'B': 'tfc:brass_mechanisms'}, 'minecraft:piston').with_advancement('tfc:brass_mechanisms')
    rm.crafting_shaped('crafting/vanilla/redstone/sticky_piston', ['X', 'Y'], {'X': 'tfc:glue', 'Y': 'minecraft:piston'}, 'minecraft:sticky_piston').with_advancement('tfc:glue')
    rm.crafting_shaped('crafting/vanilla/redstone/comparator', [' T ', 'TRT', 'SSS'], {'R': '#forge:dusts/redstone', 'T': 'minecraft:redstone_torch', 'S': '#forge:smooth_stone'}, 'minecraft:comparator').with_advancement('minecraft:redstone_torch')
    rm.crafting_shaped('crafting/vanilla/redstone/repeater', ['TRT', 'SSS'], {'T': 'minecraft:redstone_torch', 'R': '#forge:dusts/redstone', 'S': '#forge:smooth_stone'}, 'minecraft:repeater').with_advancement('minecraft:redstone_torch')
    rm.crafting_shaped('crafting/vanilla/redstone/steel_hopper', ['X X', ' Y '], {'X': '#forge:sheets/steel', 'Y': '#forge:chests/wooden'}, (2, 'minecraft:hopper')).with_advancement('#forge:sheets/wrought_iron')
    rm.crafting_shaped('crafting/vanilla/redstone/heavy_weighted_pressure_plate', ['XX'], {'X': '#forge:ingots/wrought_iron'}, 'minecraft:heavy_weighted_pressure_plate').with_advancement('#forge:ingots/wrought_iron')
    rm.crafting_shaped('crafting/vanilla/redstone/daylight_detector', ['GGG', 'RRR', 'WWW'], {'G': '#forge:glass', 'R': '#forge:dusts/redstone', 'W': '#tfc:lumber'}, 'minecraft:daylight_detector').with_advancement('#forge:dusts/redstone')
    rm.crafting_shaped('crafting/vanilla/redstone/tripwire_hook', ['I', 'W', 'S'], {'I': '#forge:sheets/wrought_iron', 'W': '#tfc:lumber', 'S': '#forge:rods/wooden'}, (2, 'minecraft:tripwire_hook')).with_advancement('#forge:sheets/wrought_iron')


    rm.crafting_shaped('crafting/vanilla/redstone/activator_rail', ['SRS', 'SWS', 'SRS'], {'S': '#forge:rods/wrought_iron', 'W': 'minecraft:redstone_torch', 'R': '#forge:rods/wooden'}, (4, 'minecraft:activator_rail')).with_advancement('#forge:rods/gold')
    rm.crafting_shaped('crafting/vanilla/redstone/detector_rail', ['S S', 'SWS', 'SRS'], {'S': '#forge:rods/wrought_iron', 'W': '#minecraft:stone_pressure_plates', 'R': '#forge:dusts/redstone'}, (4, 'minecraft:detector_rail')).with_advancement('#forge:rods/wrought_iron')
    rm.crafting_shaped('crafting/vanilla/redstone/minecart', ['X X', 'XXX'], {'X': '#forge:sheets/wrought_iron'}, 'minecraft:minecart').with_advancement('#forge:sheets/wrought_iron')
    rm.crafting_shaped('crafting/vanilla/redstone/powered_rail', ['SWS', 'SRS', 'SWS'], {'S': '#forge:rods/gold', 'W': '#forge:rods/wooden', 'R': '#forge:dusts/redstone'}, (8, 'minecraft:powered_rail')).with_advancement('#forge:rods/gold')
    rm.crafting_shaped('crafting/vanilla/redstone/rail', ['S S', 'SWS', 'S S'], {'W': '#forge:rods/wooden', 'S': '#forge:rods/wrought_iron'}, (8, 'minecraft:rail')).with_advancement('#forge:rods/wrought_iron')

    rm.crafting_shaped('crafting/vanilla/redstone/steel_activator_rail', ['SRS', 'SWS', 'SRS'], {'S': '#forge:rods/steel', 'W': 'minecraft:redstone_torch', 'R': '#forge:rods/wooden'}, (8, 'minecraft:activator_rail')).with_advancement('#forge:rods/steel')
    rm.crafting_shaped('crafting/vanilla/redstone/steel_detector_rail', ['S S', 'SWS', 'SRS'], {'S': '#forge:rods/steel', 'W': '#minecraft:stone_pressure_plates', 'R': '#forge:dusts/redstone'}, (8, 'minecraft:detector_rail')).with_advancement('#forge:rods/steel')
    rm.crafting_shaped('crafting/vanilla/redstone/steel_minecart', ['X X', 'XXX'], {'X': '#forge:sheets/steel'}, (2, 'minecraft:minecart')).with_advancement('#forge:sheets/steel')
    rm.crafting_shaped('crafting/vanilla/redstone/steel_rail', ['S S', 'SWS', 'S S'], {'W': '#forge:rods/wooden', 'S': '#forge:rods/steel'}, (16, 'minecraft:rail')).with_advancement('#forge:rods/steel')

    # ============================
    # Collapse / Landslide Recipes
    # ============================

    for rock in ROCKS:
        raw = 'tfc:rock/raw/%s' % rock
        cobble = 'tfc:rock/cobble/%s' % rock
        mossy_cobble = 'tfc:rock/mossy_cobble/%s' % rock
        gravel = 'tfc:rock/gravel/%s' % rock
        spike = 'tfc:rock/spike/%s' % rock

        # Raw rock can TRIGGER and START, and FALL into cobble
        # Ores can FALL into cobble
        rm.block_tag('can_trigger_collapse', raw)
        rm.block_tag('can_start_collapse', raw)
        rm.block_tag('can_collapse', raw)

        collapse_recipe(rm, '%s_cobble' % rock, [
            raw,
            *['tfc:ore/%s/%s' % (ore, rock) for ore, ore_data in ORES.items() if not ore_data.graded],
            *['tfc:ore/poor_%s/%s' % (ore, rock) for ore, ore_data in ORES.items() if ore_data.graded],
            *['tfc:ore/normal_%s/%s' % (ore, rock) for ore, ore_data in ORES.items() if ore_data.graded],
            *['tfc:ore/rich_%s/%s' % (ore, rock) for ore, ore_data in ORES.items() if ore_data.graded]
        ], cobble)

        for ore, ore_data in ORES.items():
            if ore_data.graded:
                for grade in ORE_GRADES.keys():
                    rm.block_tag('can_start_collapse', 'tfc:ore/%s_%s/%s' % (grade, ore, rock))
                    rm.block_tag('can_collapse', 'tfc:ore/%s_%s/%s' % (grade, ore, rock))
            else:
                rm.block_tag('can_start_collapse', 'tfc:ore/%s/%s' % (ore, rock))
                rm.block_tag('can_collapse', 'tfc:ore/%s/%s' % (ore, rock))

        # Gravel and cobblestone have landslide recipes
        rm.block_tag('can_landslide', cobble, gravel, mossy_cobble)

        landslide_recipe(rm, '%s_cobble' % rock, cobble, cobble)
        landslide_recipe(rm, '%s_mossy_cobble' % rock, mossy_cobble, mossy_cobble)
        landslide_recipe(rm, '%s_gravel' % rock, gravel, gravel)

        # Spikes can collapse, but produce nothing
        rm.block_tag('can_collapse', spike)
        collapse_recipe(rm, '%s_spike' % rock, spike, copy_input=True)

        for deposit in ORE_DEPOSITS:
            rm.block_tag('can_landslide', 'tfc:deposit/%s/%s' % (deposit, rock))
            landslide_recipe(rm, '%s_%s_deposit' % (deposit, rock), 'tfc:deposit/%s/%s' % (deposit, rock), 'tfc:deposit/%s/%s' % (deposit, rock))

    # Soil Blocks
    for variant in SOIL_BLOCK_VARIANTS:
        for block_type in SOIL_BLOCK_TYPES:
            rm.block_tag('can_landslide', 'tfc:%s/%s' % (block_type, variant))

        # Blocks that create normal dirt
        landslide_recipe(rm, '%s_dirt' % variant, ['tfc:%s/%s' % (block_type, variant) for block_type in ('dirt', 'grass', 'grass_path', 'farmland', 'rooted_dirt')], 'tfc:dirt/%s' % variant)
        landslide_recipe(rm, '%s_clay_dirt' % variant, ['tfc:%s/%s' % (block_type, variant) for block_type in ('clay', 'clay_grass')], 'tfc:dirt/%s' % variant)

    # Sand
    for variant in SAND_BLOCK_TYPES:
        rm.block_tag('can_landslide', 'tfc:sand/%s' % variant)
        landslide_recipe(rm, '%s_sand' % variant, 'tfc:sand/%s' % variant, 'tfc:sand/%s' % variant)

    # Vanilla landslide blocks
    for block in ('sand', 'red_sand', 'gravel', 'cobblestone', 'mossy_cobblestone'):
        rm.block_tag('can_landslide', 'minecraft:%s' % block)
        landslide_recipe(rm, 'vanilla_%s' % block, 'minecraft:%s' % block, 'minecraft:%s' % block)

    vanilla_dirt_landslides = ('grass_block', 'dirt', 'coarse_dirt', 'podzol')
    for block in vanilla_dirt_landslides:
        rm.block_tag('can_landslide', 'minecraft:%s' % block)
    landslide_recipe(rm, 'vanilla_dirt', ['minecraft:%s' % block for block in vanilla_dirt_landslides], 'minecraft:dirt')

    # Vanilla collapsible blocks
    for rock in ('stone', 'andesite', 'granite', 'diorite'):
        block = 'minecraft:%s' % rock
        rm.block_tag('can_trigger_collapse', block)
        rm.block_tag('can_start_collapse', block)
        rm.block_tag('can_collapse', block)

        collapse_recipe(rm, 'vanilla_%s' % rock, block, block if rock != 'stone' else 'minecraft:cobblestone')

    # ============
    # Chisel Recipes
    # ============

    for rock in ROCKS.keys():
        for block_type in CUTTABLE_ROCKS:
            chisel_recipe(rm, '%s_%s_stairs' % (block_type, rock), 'tfc:rock/%s/%s' % (block_type, rock), 'tfc:rock/%s/%s_stairs' % (block_type, rock), 'stair')
            chisel_recipe(rm, '%s_%s_slab' % (block_type, rock), 'tfc:rock/%s/%s' % (block_type, rock), 'tfc:rock/%s/%s_slab' % (block_type, rock), 'slab')
        chisel_recipe(rm, '%s_smooth' % rock, 'tfc:rock/raw/%s' % rock, 'tfc:rock/smooth/%s' % rock, 'smooth')
        chisel_recipe(rm, '%s_hardened_smooth' % rock, 'tfc:rock/hardened/%s' % rock, 'tfc:rock/smooth/%s' % rock, 'smooth')
        chisel_recipe(rm, '%s_chiseled' % rock, 'tfc:rock/bricks/%s' % rock, 'tfc:rock/chiseled/%s' % rock, 'smooth')
    for sand in SAND_BLOCK_TYPES:
        for variant in ('raw', 'cut', 'smooth'):
            chisel_recipe(rm, '%s_%s_stairs' % (variant, sand), 'tfc:%s_sandstone/%s' % (variant, sand), 'tfc:%s_sandstone/%s_stairs' % (variant, sand), 'stair')
            chisel_recipe(rm, '%s_%s_slab' % (variant, sand), 'tfc:%s_sandstone/%s' % (variant, sand), 'tfc:%s_sandstone/%s_slab' % (variant, sand), 'slab')
        chisel_recipe(rm, '%s_cut' % sand, 'tfc:raw_sandstone/%s' % sand, 'tfc:cut_sandstone/%s' % sand, 'smooth')
    for color in COLORS:
        chisel_recipe(rm, '%s_alabaster_bricks_stairs' % color, 'tfc:alabaster/stained/%s_alabaster_bricks' % color, 'tfc:alabaster/stained/%s_alabaster_bricks_stairs' % color, 'stair')
        chisel_recipe(rm, '%s_alabaster_bricks_slab' % color, 'tfc:alabaster/stained/%s_alabaster_bricks' % color, 'tfc:alabaster/stained/%s_alabaster_bricks_slab' % color, 'slab')
        chisel_recipe(rm, '%s_polished_alabaster_stairs' % color, 'tfc:alabaster/stained/%s_polished_alabaster' % color, 'tfc:alabaster/stained/%s_polished_alabaster_stairs' % color, 'stair')
        chisel_recipe(rm, '%s_polished_alabaster_slab' % color, 'tfc:alabaster/stained/%s_polished_alabaster' % color, 'tfc:alabaster/stained/%s_polished_alabaster_slab' % color, 'slab')
        chisel_recipe(rm, '%s_alabaster_bricks_polished' % color, 'tfc:alabaster/stained/%s_raw_alabaster' % color, 'tfc:alabaster/stained/%s_polished_alabaster' % color, 'smooth')
    for wood in WOODS.keys():
        chisel_recipe(rm, '%s_wood_stairs' % wood, 'tfc:wood/planks/%s' % wood, 'tfc:wood/planks/%s_stairs' % wood, 'stair')
        chisel_recipe(rm, '%s_wood_slab' % wood, 'tfc:wood/planks/%s' % wood, 'tfc:wood/planks/%s_slab' % wood, 'slab')

    # ============
    # Heat Recipes
    # ============

    heat_recipe(rm, 'torch_from_stick', '#forge:rods/wooden', 60, result_item='2 tfc:torch')
    heat_recipe(rm, 'torch_from_stick_bunch', 'tfc:stick_bunch', 60, result_item='18 tfc:torch')
    heat_recipe(rm, 'glass_from_shards', 'tfc:glass_shard', 180, result_item='minecraft:glass')
    heat_recipe(rm, 'glass_from_sand', '#forge:sand', 180, result_item='minecraft:glass')
    heat_recipe(rm, 'brick', 'tfc:ceramic/unfired_brick', POTTERY_MELT, result_item='minecraft:brick')
    heat_recipe(rm, 'flower_pot', 'tfc:ceramic/unfired_flower_pot', POTTERY_MELT, result_item='minecraft:flower_pot')
    heat_recipe(rm, 'ceramic_jug', 'tfc:ceramic/unfired_jug', POTTERY_MELT, result_item='tfc:ceramic/jug')
    heat_recipe(rm, 'ceramic_pan', 'tfc:ceramic/unfired_pan', POTTERY_MELT, result_item='tfc:pan/empty')
    heat_recipe(rm, 'terracotta', 'minecraft:clay', POTTERY_MELT, result_item='minecraft:terracotta')

    for ore, ore_data in ORES.items():
        if ore_data.metal and ore_data.graded:
            temp = METALS[ore_data.metal].melt_temperature
            heat_recipe(rm, ('ore', 'small_%s' % ore), 'tfc:ore/small_%s' % ore, temp, None, '%d tfc:metal/%s' % (10, ore_data.metal))
            heat_recipe(rm, ('ore', 'poor_%s' % ore), 'tfc:ore/poor_%s' % ore, temp, None, '%d tfc:metal/%s' % (15, ore_data.metal))
            heat_recipe(rm, ('ore', 'normal_%s' % ore), 'tfc:ore/normal_%s' % ore, temp, None, '%d tfc:metal/%s' % (25, ore_data.metal))
            heat_recipe(rm, ('ore', 'rich_%s' % ore), 'tfc:ore/rich_%s' % ore, temp, None, '%d tfc:metal/%s' % (35, ore_data.metal))

    for metal, metal_data in METALS.items():
        melt_metal = metal if metal_data.melt_metal is None else metal_data.melt_metal
        for item, item_data in METAL_ITEMS_AND_BLOCKS.items():
            if item_data.type == 'all' or item_data.type in metal_data.types:
                heat_recipe(rm, ('metal', '%s_%s' % (metal, item)), 'tfc:metal/%s/%s' % (item, metal), metal_data.melt_temperature, None, '%d tfc:metal/%s' % (item_data.smelt_amount, melt_metal))

    wrought_iron = METALS['wrought_iron']
    heat_recipe(rm, 'raw_bloom', 'tfc:raw_iron_bloom', wrought_iron.melt_temperature, None, '100 tfc:metal/cast_iron')
    heat_recipe(rm, 'refined_bloom', 'tfc:refined_iron_bloom', wrought_iron.melt_temperature, None, '100 tfc:metal/cast_iron')

    # Mold, Ceramic Firing
    for tool, tool_data in METAL_ITEMS.items():
        if tool_data.mold:
            heat_recipe(rm, ('%s_mold' % tool), 'tfc:ceramic/unfired_%s_mold' % tool, POTTERY_MELT, 'tfc:ceramic/%s_mold' % tool)

    for pottery in SIMPLE_POTTERY:
        heat_recipe(rm, 'fired_' + pottery, 'tfc:ceramic/unfired_' + pottery, POTTERY_MELT, result_item='tfc:ceramic/' + pottery)

    for color in COLORS:
        heat_recipe(rm, 'glazed_terracotta_%s' % color, 'minecraft:%s_terracotta' % color, POTTERY_MELT, result_item='minecraft:%s_glazed_terracotta' % color)
        heat_recipe(rm, 'glazed_ceramic_vessel_%s' % color, 'tfc:ceramic/%s_unfired_vessel' % color, POTTERY_MELT, 'tfc:ceramic/%s_glazed_vessel' % color)

        rm.crafting_shapeless('crafting/ceramic/%s_unfired_vessel' % color, ('minecraft:%s_dye' % color, 'tfc:ceramic/unfired_vessel'), 'tfc:ceramic/%s_unfired_vessel' % color).with_advancement('minecraft:%s_dye' % color)
        if color != 'white':
            rm.crafting_shaped('crafting/vanilla/color/%s_bed' % color, ['ZZZ', 'XXX', 'YYY'], {'X': '#tfc:high_quality_cloth', 'Y': '#tfc:lumber', 'Z': 'minecraft:%s_dye' % color}, 'minecraft:%s_bed' % color).with_advancement('#tfc:high_quality_cloth')
        rm.crafting_shapeless('crafting/vanilla/color/%s_concrete_powder' % color, ('minecraft:%s_dye' % color, '#forge:sand', '#forge:sand', '#forge:sand', '#forge:sand', '#forge:gravel', '#forge:gravel', '#forge:gravel', '#forge:gravel'), (8, 'minecraft:%s_concrete_powder' % color))

    for name in DISABLED_VANILLA_RECIPES:
        disable_recipe(rm, 'minecraft:' + name)
    for section in ARMOR_SECTIONS:
        for variant in VANILLA_ARMOR_TYPES:
            disable_recipe(rm, 'minecraft:%s_%s' % (variant, section))
    for tool in VANILLA_TOOLS:
        for variant in VANILLA_TOOL_MATERIALS:
            disable_recipe(rm, 'minecraft:%s_%s' % (variant, tool))

    # Quern
    quern_recipe(rm, 'olive', 'tfc:food/olive', 'tfc:olive_paste', count=2)
    quern_recipe(rm, 'borax', 'tfc:ore/borax', 'tfc:powder/flux', count=6)
    quern_recipe(rm, 'fluxstone', '#tfc:fluxstone', 'tfc:powder/flux', count=2)
    quern_recipe(rm, 'cinnabar', 'tfc:ore/cinnabar', 'minecraft:redstone', count=8)
    quern_recipe(rm, 'cryolite', 'tfc:ore/cryolite', 'minecraft:redstone', count=8)
    quern_recipe(rm, 'bone', 'minecraft:bone', 'minecraft:bone_meal', count=3)
    quern_recipe(rm, 'bone_block', 'minecraft:bone_block', 'minecraft:bone_meal', count=9)
    quern_recipe(rm, 'charcoal', 'minecraft:charcoal', 'tfc:powder/charcoal', count=4)
    quern_recipe(rm, 'salt', 'tfc:ore/halite', 'tfc:powder/salt', count=4)
    quern_recipe(rm, 'blaze_rod', 'minecraft:blaze_rod', 'minecraft:blaze_powder', count=2)
    quern_recipe(rm, 'raw_limestone', 'tfc:rock/raw/limestone', 'tfc:ore/gypsum')
    quern_recipe(rm, 'sylvite', 'tfc:ore/sylvite', 'tfc:powder/sylvite', count=4)

    for grain in GRAINS:
        heat_recipe(rm, grain + '_dough', not_rotten('tfc:food/%s_dough' % grain), 200, result_item=item_stack_provider('tfc:food/%s_bread' % grain))
        quern_recipe(rm, grain + '_grain', not_rotten('tfc:food/%s_grain' % grain), item_stack_provider('tfc:food/%s_flour' % grain))
        res = utils.resource_location(rm.domain, grain + '_cutting')
        rm.write((*rm.resource_dir, 'data', res.domain, 'recipes', 'crafting', res.path), {
            'type': 'tfc:extra_products_shapeless_crafting',
            'extra_products': utils.item_stack_list('tfc:straw'),
            'recipe': {
                'type': 'tfc:damage_inputs_shapeless_crafting',
                'recipe': {
                    'type': 'minecraft:crafting_shapeless',
                    'ingredients': utils.item_stack_list((not_rotten('tfc:food/%s' % grain), '#tfc:knives')),
                    'result': utils.item_stack('tfc:food/%s_grain' % grain)
                }
            }
        })
        rm.crafting_shapeless('crafting/%s_dough' % grain, (not_rotten('tfc:food/%s_flour' % grain), fluid_item_ingredient('100 minecraft:water')), (2, 'tfc:food/%s_dough' % grain)).with_advancement('tfc:food/%s_grain' % grain)
        damage_shaped(rm, 'crafting/%s_sandwich' % grain, ['ZX ', 'YYY', ' X '], {'X': not_rotten('tfc:food/%s_bread' % grain), 'Y': not_rotten('#tfc:foods/usable_in_sandwich'), 'Z': '#tfc:knives'}, (2, 'tfc:food/%s_bread_sandwich' % grain), recipe_type='tfc:sandwich_crafting').with_advancement('tfc:food/%s_bread' % grain)

    for meat in MEATS:
        heat_recipe(rm, meat, not_rotten('tfc:food/%s' % meat), 200, result_item=item_stack_provider('tfc:food/cooked_%s' % meat))

    heat_recipe(rm, 'seaweed', 'tfc:groundcover/seaweed', 200, item_stack_provider('tfc:food/dried_seaweed'))
    heat_recipe(rm, 'giant_kelp_flower', 'tfc:plant/giant_kelp_flower', 200, item_stack_provider('tfc:food/dried_kelp'))

    for ore in ['hematite', 'limonite', 'malachite']:
        for grade, data in ORE_GRADES.items():
            quern_recipe(rm, '%s_%s' % (grade, ore), 'tfc:ore/%s_%s' % (grade, ore), 'tfc:powder/%s' % ore, count=data.grind_amount)
        quern_recipe(rm, 'small_%s' % ore, 'tfc:ore/small_%s' % ore, 'tfc:powder/%s' % ore, count=2)

    for ore in ['sulfur', 'saltpeter', 'graphite', 'kaolinite']:
        quern_recipe(rm, ore, 'tfc:ore/%s' % ore, 'tfc:powder/%s' % ore, count=4)
    for gem in GEMS:
        quern_recipe(rm, gem, 'tfc:ore/%s' % gem, 'tfc:powder/%s' % gem, count=4)

    for color, plants in PLANT_COLORS.items():
        for plant in plants:
            quern_recipe(rm, 'plant/%s' % plant, 'tfc:plant/%s' % plant, 'minecraft:%s_dye' % color, count=2)

    for i, size in enumerate(('small', 'medium', 'large')):
        scraping_recipe(rm, '%s_soaked_hide' % size, 'tfc:%s_soaked_hide' % size, 'tfc:%s_scraped_hide' % size)
        damage_shapeless(rm, 'crafting/%s_sheepskin' % size, ('tfc:%s_sheepskin_hide' % size, '#tfc:knives'), (i + 1, 'tfc:wool')).with_advancement('tfc:%s_sheepskin_hide' % size)

    paste = utils.ingredient('tfc:olive_paste')
    rm.recipe(('pot', 'olive_oil_water'), 'tfc:pot_fluid', {
        'ingredients': [paste, paste, paste, paste, paste],
        'fluid_ingredient': fluid_stack_ingredient('1000 minecraft:water'),
        'duration': 2000,
        'temperature': 300,
        'fluid_output': fluid_stack('1000 tfc:olive_oil_water')
    })

    blubber = utils.ingredient('tfc:blubber')
    rm.recipe(('pot', 'tallow'), 'tfc:pot_fluid', {
        'ingredients': [blubber, blubber, blubber, blubber, blubber],
        'fluid_ingredient': fluid_stack_ingredient('1000 minecraft:water'),
        'duration': 2000,
        'temperature': 600,
        'fluid_output': fluid_stack('1000 tfc:tallow')
    })

    ash = utils.ingredient('tfc:powder/wood_ash')
    rm.recipe(('pot', 'lye'), 'tfc:pot_fluid', {
        'ingredients': [ash, ash, ash, ash, ash],
        'fluid_ingredient': fluid_stack_ingredient('1000 minecraft:water'),
        'duration': 2000,
        'temperature': 600,
        'fluid_output': fluid_stack('1000 tfc:lye')
    })

    for color in COLORS:
        rm.recipe(('pot', '%s_dye' % color), 'tfc:pot_fluid', {
            'ingredients': [utils.ingredient('minecraft:%s_dye' % color)],
            'fluid_ingredient': fluid_stack_ingredient('1000 minecraft:water'),
            'duration': 2000,
            'temperature': 600,
            'fluid_output': fluid_stack('1000 tfc:%s_dye' % color)
        })

    soup_food = not_rotten(utils.ingredient('#tfc:foods/usable_in_soup'))
    rm.recipe(('pot', 'soup_3'), 'tfc:pot_soup', {
        'ingredients': [soup_food, soup_food, soup_food],
        'fluid_ingredient': fluid_stack_ingredient('1000 minecraft:water'),
        'duration': 1000,
        'temperature': 300
    })
    rm.recipe(('pot', 'soup_4'), 'tfc:pot_soup', {
        'ingredients': [soup_food, soup_food, soup_food, soup_food],
        'fluid_ingredient': fluid_stack_ingredient('1000 minecraft:water'),
        'duration': 1150,
        'temperature': 300
    })
    rm.recipe(('pot', 'soup_5'), 'tfc:pot_soup', {
        'ingredients': [soup_food, soup_food, soup_food, soup_food, soup_food],
        'fluid_ingredient': fluid_stack_ingredient('1000 minecraft:water'),
        'duration': 1300,
        'temperature': 300
    })

    clay_knapping(rm, 'vessel', [' XXX ', 'XXXXX', 'XXXXX', 'XXXXX', ' XXX '], 'tfc:ceramic/unfired_vessel')
    clay_knapping(rm, 'jug', [' X   ', 'XXXX ', 'XXX X', 'XXXX ', 'XXX  '], 'tfc:ceramic/unfired_jug')
    clay_knapping(rm, 'pot', ['X   X', 'X   X', 'X   X', 'XXXXX', ' XXX '], 'tfc:ceramic/unfired_pot')
    clay_knapping(rm, 'bowl_2', ['X   X', ' XXX '], (2, 'tfc:ceramic/unfired_bowl'), False)
    clay_knapping(rm, 'bowl_4', ['X   X', ' XXX ', '     ', 'X   X', ' XXX '], (4, 'tfc:ceramic/unfired_bowl'))
    clay_knapping(rm, 'brick', ['XXXXX', '     ', 'XXXXX', '     ', 'XXXXX'], (3, 'tfc:ceramic/unfired_brick'))
    clay_knapping(rm, 'flower_pot', [' X X ', ' XXX ', '     ', ' X X ', ' XXX '], (2, 'tfc:ceramic/unfired_flower_pot'))
    clay_knapping(rm, 'spindle_head', ['  X  ', 'XXXXX', '  X  '], 'tfc:ceramic/unfired_spindle_head', False)
    clay_knapping(rm, 'pan', ['X   X', 'XXXXX', ' XXX '], 'tfc:ceramic/unfired_pan', False)

    clay_knapping(rm, 'ingot_mold', ['XXXX', 'X  X', 'X  X', 'X  X', 'XXXX'], (2, 'tfc:ceramic/unfired_ingot_mold'))
    clay_knapping(rm, 'axe_head_mold', ['X XXX', '    X', '     ', '    X', 'X XXX'], 'tfc:ceramic/unfired_axe_head_mold', True)
    clay_knapping(rm, 'chisel_head_mold', ['XX XX', 'XX XX', 'XX XX', 'XX XX', 'XX XX'], 'tfc:ceramic/unfired_chisel_head_mold', True)
    clay_knapping(rm, 'hammer_head_mold', ['XXXXX', '     ', '     ', 'XX XX', 'XXXXX'], 'tfc:ceramic/unfired_hammer_head_mold', True)
    clay_knapping(rm, 'hoe_head_mold', ['XXXXX', '     ', '  XXX', 'XXXXX'], 'tfc:ceramic/unfired_hoe_head_mold', True)
    clay_knapping(rm, 'javelin_head_mold', ['   XX', '    X', '     ', 'X   X', 'XX XX'], 'tfc:ceramic/unfired_javelin_head_mold', True)
    clay_knapping(rm, 'knife_blade_mold', ['XX X', 'X  X', 'X  X', 'X  X', 'X  X'], 'tfc:ceramic/unfired_knife_blade_mold', True)
    clay_knapping(rm, 'mace_blade_mold', ['XX XX', 'X   X', 'X   X', 'X   X', 'XX XX'], 'tfc:ceramic/unfired_mace_head_mold', True)
    clay_knapping(rm, 'pickaxe_head_mold', ['XXXXX', 'X   X', ' XXX ', 'XXXXX'], 'tfc:ceramic/unfired_pickaxe_head_mold', True)
    clay_knapping(rm, 'propick_head_mold', ['XXXXX', '    X', ' XXX ', ' XXXX', 'XXXXX'], 'tfc:ceramic/unfired_propick_head_mold', True)
    clay_knapping(rm, 'saw_blade_mold', ['  XXX', '   XX', 'X   X', 'X    ', 'XXX  '], 'tfc:ceramic/unfired_saw_blade_mold', True)
    clay_knapping(rm, 'shovel_head_mold', ['X   X', 'X   X', 'X   X', 'X   X', 'XX XX'], 'tfc:ceramic/unfired_shovel_head_mold', True)
    clay_knapping(rm, 'sword_blade_mold', ['  XXX', '   XX', 'X   X', 'XX  X', 'XXXX '], 'tfc:ceramic/unfired_sword_blade_mold', True)
    clay_knapping(rm, 'scythe_blade_mold', ['XXXXX', 'X    ', '    X', '  XXX', 'XXXXX'], 'tfc:ceramic/unfired_scythe_blade_mold', True)

    fire_clay_knapping(rm, 'crucible', ['X   X', 'X   X', 'X   X', 'X   X', 'XXXXX'], 'tfc:ceramic/unfired_crucible')
    fire_clay_knapping(rm, 'brick', ['XXXXX', '     ', 'XXXXX', '     ', 'XXXXX'], (3, 'tfc:ceramic/unfired_fire_brick'))

    leather_knapping(rm, 'helmet', ['XXXXX', 'X   X', 'X   X', '     ', '     '], 'minecraft:leather_helmet')
    leather_knapping(rm, 'chestplate', ['X   X', 'XXXXX', 'XXXXX', 'XXXXX', 'XXXXX'], 'minecraft:leather_chestplate')
    leather_knapping(rm, 'leggings', ['XXXXX', 'XXXXX', 'XX XX', 'XX XX', 'XX XX'], 'minecraft:leather_leggings')
    leather_knapping(rm, 'boots', ['XX   ', 'XX   ', 'XX   ', 'XXXX ', 'XXXXX'], 'minecraft:leather_boots')
    leather_knapping(rm, 'saddle', ['  X  ', 'XXXXX', 'XXXXX', 'XXXXX', '  X  '], 'minecraft:saddle')
    # todo: quiver

    for category in ROCK_CATEGORIES:
        predicate = '#tfc:%s_rock' % category
        rock_knapping(rm, 'axe_head_%s' % category, [' X   ', 'XXXX ', 'XXXXX', 'XXXX ', ' X   '], 'tfc:stone/axe_head/%s' % category, predicate)
        rock_knapping(rm, 'shovel_head_%s' % category, ['XXX', 'XXX', 'XXX', 'XXX', ' X '], 'tfc:stone/shovel_head/%s' % category, predicate)
        rock_knapping(rm, 'hoe_head_%s' % category, ['XXXXX', '   XX'], 'tfc:stone/hoe_head/%s' % category, predicate)
        rock_knapping(rm, 'knife_head_%s' % category, ['X ', 'XX', 'XX', 'XX', 'XX'], 'tfc:stone/knife_head/%s' % category, predicate)
        rock_knapping(rm, 'knife_head_1_%s' % category, ['X  X ', 'XX XX', 'XX XX', 'XX XX', 'XX XX'], (2, 'tfc:stone/knife_head/%s' % category), predicate)
        rock_knapping(rm, 'knife_head_2_%s' % category, ['X   X', 'XX XX', 'XX XX', 'XX XX', 'XX XX'], (2, 'tfc:stone/knife_head/%s' % category), predicate)
        rock_knapping(rm, 'knife_head_3_%s' % category, [' X X ', 'XX XX', 'XX XX', 'XX XX', 'XX XX'], (2, 'tfc:stone/knife_head/%s' % category), predicate)
        rock_knapping(rm, 'hoe_head_1_%s' % category, ['XXXXX', 'XX   ', '     ', 'XXXXX', 'XX   '], (2, 'tfc:stone/hoe_head/%s' % category), predicate)
        rock_knapping(rm, 'hoe_head_2_%s' % category, ['XXXXX', 'XX   ', '     ', 'XXXXX', '   XX'], (2, 'tfc:stone/hoe_head/%s' % category), predicate)
        rock_knapping(rm, 'knife_head_%s' % category, ['X ', 'XX', 'XX', 'XX', 'XX'], 'tfc:stone/knife_head/%s' % category, predicate)
        rock_knapping(rm, 'javelin_head_%s' % category, ['XXX  ', 'XXXX ', 'XXXXX', ' XXX ', '  X  '], 'tfc:stone/javelin_head/%s' % category, predicate)
        rock_knapping(rm, 'hammer_head_%s' % category, ['XXXXX', 'XXXXX', '  X  '], 'tfc:stone/hammer_head/%s' % category, predicate)

        for tool in ROCK_CATEGORY_ITEMS:
            rm.crafting_shaped('crafting/stone/%s_%s' % (tool, category), ['X', 'Y'], {'X': 'tfc:stone/%s_head/%s' % (tool, category), 'Y': '#forge:rods/wooden'}, 'tfc:stone/%s/%s' % (tool, category)).with_advancement('tfc:stone/%s_head/%s' % (tool, category))

    # Casting Recipes

    for metal, metal_data in METALS.items():
        for tool, tool_data in METAL_ITEMS.items():
            if tool == 'ingot' or (tool_data.mold and 'tool' in metal_data.types and metal_data.tier <= 2):
                casting_recipe(rm, '%s_%s' % (metal, tool), tool, metal, tool_data.smelt_amount, 0.1 if tool == 'ingot' else 1)

    rm.recipe('casting', 'tfc:casting_crafting', {})  # simple recipe to allow any casting recipe to be used in a crafting grid
    rm.recipe('food_combining', 'tfc:food_combining', {})

    # Alloy Recipes

    alloy_recipe(rm, 'bismuth_bronze', 'bismuth_bronze', ('zinc', 0.2, 0.3), ('copper', 0.5, 0.65), ('bismuth', 0.1, 0.2))
    alloy_recipe(rm, 'black_bronze', 'black_bronze', ('copper', 0.5, 0.7), ('silver', 0.1, 0.25), ('gold', 0.1, 0.25))
    alloy_recipe(rm, 'bronze', 'bronze', ('copper', 0.88, 0.92), ('tin', 0.08, 0.12))
    alloy_recipe(rm, 'brass', 'brass', ('copper', 0.88, 0.92), ('zinc', 0.08, 0.12))
    alloy_recipe(rm, 'rose_gold', 'rose_gold', ('copper', 0.15, 0.3), ('gold', 0.7, 0.85))
    alloy_recipe(rm, 'sterling_silver', 'sterling_silver', ('copper', 0.2, 0.4), ('silver', 0.6, 0.8))
    alloy_recipe(rm, 'weak_steel', 'weak_steel', ('steel', 0.5, 0.7), ('nickel', 0.15, 0.25), ('black_bronze', 0.15, 0.25))
    alloy_recipe(rm, 'weak_blue_steel', 'weak_blue_steel', ('black_steel', 0.5, 0.55), ('steel', 0.2, 0.25), ('bismuth_bronze', 0.1, 0.15), ('sterling_silver', 0.1, 0.15))
    alloy_recipe(rm, 'weak_red_steel', 'weak_red_steel', ('black_steel', 0.5, 0.55), ('steel', 0.2, 0.25), ('brass', 0.1, 0.15), ('rose_gold', 0.1, 0.15))

    # Bloomery Recipes
    bloomery_recipe(rm, 'raw_iron_bloom', 'tfc:raw_iron_bloom', '100 tfc:metal/cast_iron', 'minecraft:charcoal', 15000)

    # Barrel Recipes
    for size, amount, output in (('small', 300, 1), ('medium', 400, 2), ('large', 500, 3)):
        barrel_sealed_recipe(rm, '%s_soaked_hide' % size, '%s Soaked Hide' % size, 8000, 'tfc:%s_raw_hide' % size, '%d tfc:limewater' % amount, output_item='tfc:%s_soaked_hide' % size)
        barrel_sealed_recipe(rm, '%s_prepared_hide' % size, '%s Prepared Hide' % size, 8000, 'tfc:%s_scraped_hide' % size, '%d minecraft:water' % amount, output_item='tfc:%s_prepared_hide' % size)
        barrel_sealed_recipe(rm, '%s_leather' % size, 'Leather', 8000, 'tfc:%s_prepared_hide' % size, '%d tfc:tannin' % amount, output_item='%d minecraft:leather' % output)

    barrel_sealed_recipe(rm, 'tannin', 'Tannin', 8000, '#tfc:makes_tannin', '1000 minecraft:water', output_fluid='1000 tfc:tannin')
    barrel_sealed_recipe(rm, 'jute_fiber', 'Jute Fiber', 8000, 'tfc:jute', '200 minecraft:water', output_item='tfc:jute_fiber')
    barrel_sealed_recipe(rm, 'sugar', 'Sugar', 8000, 'tfc:food/sugarcane', '600 minecraft:water', output_item='minecraft:sugar')
    barrel_sealed_recipe(rm, 'glue', 'Glue', 8000, 'minecraft:bone_meal', '500 tfc:limewater',  output_item='tfc:glue')

    barrel_sealed_recipe(rm, 'beer', 'Fermenting Beer', 72000, 'tfc:food/barley_flour', '500 minecraft:water', output_fluid='500 tfc:beer')
    barrel_sealed_recipe(rm, 'cider', 'Fermenting Cider', 72000, '#tfc:foods/apples', '500 minecraft:water', output_fluid='500 tfc:cider')
    barrel_sealed_recipe(rm, 'rum', 'Fermenting Rum', 72000, 'minecraft:sugar', '500 minecraft:water', output_fluid='500 tfc:rum')
    barrel_sealed_recipe(rm, 'sake', 'Fermenting Sake', 72000, 'tfc:food/rice_flour', '500 minecraft:water', output_fluid='500 tfc:sake')
    barrel_sealed_recipe(rm, 'vodka', 'Fermenting Vodka', 72000, 'tfc:food/potato', '500 minecraft:water', output_fluid='500 tfc:vodka')
    barrel_sealed_recipe(rm, 'whiskey', 'Fermenting Whiskey', 72000, 'tfc:food/wheat_flour', '500 minecraft:water', output_fluid='500 tfc:whiskey')
    barrel_sealed_recipe(rm, 'corn_whiskey', 'Fermenting Corn Whiskey', 72000, 'tfc:food/maize_flour', '500 minecraft:water', output_fluid='500 tfc:corn_whiskey')
    barrel_sealed_recipe(rm, 'rye_whiskey', 'Fermenting Rye Whiskey', 72000, 'tfc:food/rye_flour', '500 minecraft:water', output_fluid='500 tfc:rye_whiskey')

    barrel_sealed_recipe(rm, 'vinegar', 'Vinegar', 8000, '#tfc:foods/fruits', '250 #tfc:alcohols', output_fluid='250 tfc:vinegar')

    barrel_sealed_recipe(rm, 'pickling', 'Pickling', 4000, not_rotten(has_trait(['#tfc:foods/fruits', '#tfc:foods/vegetables', '#tfc:foods/meats'], 'tfc:brined')), '125 tfc:vinegar', item_stack_provider(copy_input=True, add_trait='tfc:pickled'))
    barrel_sealed_recipe(rm, 'brined', 'Brining', 4000, not_rotten(['#tfc:foods/fruits', '#tfc:foods/vegetables', '#tfc:foods/meats']), '125 tfc:brine', item_stack_provider(copy_input=True, add_trait='tfc:brined'))
    barrel_sealed_recipe(rm, 'preserved_in_vinegar', 'Preserving in Vinegar', -1, not_rotten(has_trait(['#tfc:foods/fruits', '#tfc:foods/vegetables', '#tfc:foods/meats'], 'tfc:pickled')), '125 tfc:vinegar', on_seal=item_stack_provider(copy_input=True, add_trait='tfc:vinegar'), on_unseal=item_stack_provider(copy_input=True, remove_trait='tfc:vinegar'))

    barrel_sealed_recipe(rm, 'mortar', 'Mortar', 8000, '#minecraft:sand', '100 tfc:limewater', output_item='16 tfc:mortar')
    barrel_sealed_recipe(rm, 'curdling', 'Curdling Milk', 8000, input_fluid='1 tfc:milk_vinegar', output_fluid='1 tfc:curdled_milk')
    barrel_sealed_recipe(rm, 'cheese', 'Cheese', 8000, input_fluid='625 tfc:curdled_milk', output_item=item_stack_provider('2 tfc:food/cheese'))
    barrel_sealed_recipe(rm, 'raw_alabaster', 'Raw Alabaster', 1000, 'tfc:ore/gypsum', '100 tfc:limewater', output_item='tfc:alabaster/raw/alabaster')
    barrel_sealed_recipe(rm, 'clean_jute_net', 'Cleaning Jute Net', 1000, 'tfc:dirty_jute_net', '125 minecraft:water', output_item='tfc:jute_net')

    # Bleaching Recipes
    for variant in VANILLA_DYED_ITEMS:
        cost = 125 if variant != 'carpet' else 25
        barrel_sealed_recipe(rm, 'dye/bleach_%s' % variant, 'Bleaching %s' % variant, 1000, '#tfc:colored_%s' % variant, '%d tfc:lye' % cost, output_item='minecraft:white_%s' % variant)
    barrel_sealed_recipe(rm, 'dye/bleach_shulkers', 'Bleaching Shulker Box', 1000, '#tfc:colored_shulker_boxes', '125 tfc:lye', output_item='minecraft:shulker_box')
    barrel_sealed_recipe(rm, 'dye/bleach_concrete_powder', 'Bleaching Concrete Powder', 1000, '#tfc:colored_concrete_powder', '125 tfc:lye', output_item='tfc:aggregate')
    for variant in ('raw_alabaster', 'alabaster_bricks', 'polished_alabaster'):
        result_name = 'tfc:alabaster/raw/%s' % variant if variant != 'raw_alabaster' else 'tfc:alabaster/raw/alabaster'
        barrel_sealed_recipe(rm, 'dye/bleach_%s' % variant, 'Bleaching %s' % variant, 1000, '#tfc:colored_%s' % variant, '125 tfc:lye', output_item=result_name)

    # Dyeing Items
    for color in COLORS:
        fluid = '125 tfc:%s_dye' % color
        for variant in VANILLA_DYED_ITEMS:
            item = 'minecraft:%s_%s' % (color, variant)
            if color != 'white':
                barrel_sealed_recipe(rm, 'dye/%s_%s' % (color, variant), 'Dyeing %s %s' % (variant, color), 1000, 'minecraft:white_%s' % variant, fluid, item)

        barrel_sealed_recipe(rm, 'dye/%s_shulker' % color, 'Dyeing Shulker %s' % color, 1000, 'minecraft:shulker_box', fluid, 'minecraft:%s_shulker_box' % color)
        barrel_sealed_recipe(rm, 'dye/%s_glazed_vessel' % color, 'Dyeing Unfired Vessel %s' % color, 1000, 'tfc:ceramic/unfired_vessel', fluid, 'tfc:ceramic/%s_unfired_vessel' % color)
        barrel_sealed_recipe(rm, 'dye/%s_concrete_powder' % color, 'Dyeing Aggregate %s' % color, 1000, 'tfc:aggregate', fluid, 'minecraft:%s_concrete_powder' % color)

    # Instant Barrel Recipes
    barrel_instant_recipe(rm, 'fresh_to_salt_water', 'tfc:powder/salt', '125 minecraft:water', output_fluid='125 tfc:salt_water')
    barrel_instant_recipe(rm, 'limewater', 'tfc:powder/flux', '500 minecraft:water', output_fluid='500 tfc:limewater')
    barrel_instant_recipe(rm, 'olive_oil', 'tfc:jute_net', '250 tfc:olive_oil_water', 'tfc:dirty_jute_net', '50 tfc:olive_oil')
    barrel_instant_recipe(rm, 'cooling_freshwater', {'ingredient': {'type': 'tfc:heatable', 'min_temp': 0}}, '1 minecraft:water', output_item=item_stack_provider(copy_input=True, add_heat=-5), sound='minecraft:block.fire.extinguish')
    barrel_instant_recipe(rm, 'cooling_saltwater', {'ingredient': {'type': 'tfc:heatable', 'min_temp': 0}}, '1 tfc:salt_water', output_item=item_stack_provider(copy_input=True, add_heat=-5), sound='minecraft:block.fire.extinguish')
    barrel_instant_recipe(rm, 'cooling_olive_oil', {'ingredient': {'type': 'tfc:heatable', 'min_temp': 0}}, '1 tfc:olive_oil', output_item=item_stack_provider(copy_input=True, add_heat=-40), sound='minecraft:block.fire.extinguish')
    barrel_instant_recipe(rm, 'brine', {'ingredient': fluid_item_ingredient('1000 tfc:vinegar')}, '9000 tfc:salt_water', output_fluid='10000 tfc:brine')
    barrel_instant_recipe(rm, 'milk_vinegar', {'ingredient': fluid_item_ingredient('1000 tfc:vinegar')}, '9000 minecraft:milk', output_fluid='10000 tfc:milk_vinegar')
    barrel_instant_recipe(rm, 'clean_soup_bowl', '#tfc:soup_bowls', '100 minecraft:water', output_item=item_stack_provider(empty_bowl=True))

    # Loom Recipes
    loom_recipe(rm, 'burlap_cloth', 'tfc:jute_fiber', 12, 'tfc:burlap_cloth', 12, 'tfc:block/burlap')
    loom_recipe(rm, 'wool_cloth', 'tfc:wool_yarn', 16, 'tfc:wool_cloth', 16, 'minecraft:block/white_wool')
    loom_recipe(rm, 'silk_cloth', 'minecraft:string', 24, 'tfc:silk_cloth', 24, 'minecraft:block/white_wool')
    loom_recipe(rm, 'wool_block', 'tfc:wool_cloth', 4, (8, 'minecraft:white_wool'), 4, 'minecraft:block/white_wool')

    # Anvil Working Recipes
    metal = '?'

    def item(_variant: str) -> str:
        return 'tfc:metal/%s/%s' % (_variant, metal)

    for metal, metal_data in METALS.items():

        # Misc
        if 'part' in metal_data.types:
            anvil_recipe(rm, '%s_sheet' % metal, item('double_ingot'), item('sheet'), metal_data.tier, Rules.hit_last, Rules.hit_second_last, Rules.hit_third_last)
            anvil_recipe(rm, '%s_rod' % metal, item('ingot'), '2 tfc:metal/rod/%s' % metal, metal_data.tier, Rules.bend_last, Rules.draw_second_last, Rules.draw_third_last)

        # Tools
        if 'tool' in metal_data.types:
            anvil_recipe(rm, '%s_tuyere' % metal, 'tfc:metal/double_sheet/%s' % metal, 'tfc:metal/tuyere/%s' % metal, metal_data.tier, Rules.bend_last, Rules.bend_second_last)
            anvil_recipe(rm, '%s_pickaxe_head' % metal, item('ingot'), item('pickaxe_head'), metal_data.tier, Rules.punch_last, Rules.bend_not_last, Rules.draw_not_last, bonus=True)
            anvil_recipe(rm, '%s_shovel_head' % metal, item('ingot'), item('shovel_head'), metal_data.tier, Rules.punch_last, Rules.hit_not_last, bonus=True)

            anvil_recipe(rm, '%s_axe_head' % metal, item('ingot'), item('axe_head'), metal_data.tier, Rules.punch_last, Rules.hit_second_last, Rules.upset_third_last, bonus=True)
            anvil_recipe(rm, '%s_hoe_head' % metal, item('ingot'), item('hoe_head'), metal_data.tier, Rules.punch_last, Rules.hit_not_last, Rules.bend_not_last, bonus=True)
            anvil_recipe(rm, '%s_hammer_head' % metal, item('ingot'), item('hammer_head'), metal_data.tier, Rules.punch_last, Rules.shrink_not_last, bonus=True)
            anvil_recipe(rm, '%s_propick_head' % metal, item('ingot'), item('propick_head'), metal_data.tier, Rules.punch_last, Rules.draw_not_last, Rules.bend_not_last, bonus=True)
            anvil_recipe(rm, '%s_saw_blade' % metal, item('ingot'), item('saw_blade'), metal_data.tier, Rules.hit_last, Rules.hit_second_last, bonus=True)
            anvil_recipe(rm, '%s_sword_blade' % metal, item('double_ingot'), item('sword_blade'), metal_data.tier, Rules.hit_last, Rules.bend_second_last, Rules.bend_third_last, bonus=True)
            anvil_recipe(rm, '%s_mace_head' % metal, item('double_ingot'), item('mace_head'), metal_data.tier, Rules.hit_last, Rules.shrink_not_last, Rules.bend_not_last, bonus=True)
            anvil_recipe(rm, '%s_scythe_blade' % metal, item('ingot'), item('scythe_blade'), metal_data.tier, Rules.hit_last, Rules.draw_second_last, Rules.bend_third_last, bonus=True)
            anvil_recipe(rm, '%s_knife_blade' % metal, item('ingot'), item('knife_blade'), metal_data.tier, Rules.hit_last, Rules.draw_second_last, Rules.draw_third_last, bonus=True)
            anvil_recipe(rm, '%s_javelin_head' % metal, item('ingot'), item('javelin_head'), metal_data.tier, Rules.hit_last, Rules.hit_second_last, Rules.draw_third_last, bonus=True)
            anvil_recipe(rm, '%s_chisel_head' % metal, item('ingot'), item('chisel_head'), metal_data.tier, Rules.hit_last, Rules.hit_not_last, Rules.draw_not_last, bonus=True)

            anvil_recipe(rm, '%s_shield' % metal, item('double_sheet'), item('shield'), metal_data.tier, Rules.upset_last, Rules.bend_second_last, Rules.bend_third_last, bonus=True)

        # Armor
        if 'armor' in metal_data.types:
            anvil_recipe(rm, '%s_unfinished_helmet' % metal, item('double_sheet'), item('unfinished_helmet'), metal_data.tier, Rules.hit_last, Rules.bend_second_last, Rules.bend_third_last)
            anvil_recipe(rm, '%s_unfinished_chestplate' % metal, item('double_sheet'), item('unfinished_chestplate'), metal_data.tier, Rules.hit_last, Rules.hit_second_last, Rules.upset_third_last)
            anvil_recipe(rm, '%s_unfinished_greaves' % metal, item('double_sheet'), item('unfinished_greaves'), metal_data.tier, Rules.bend_any, Rules.draw_any, Rules.hit_any)
            anvil_recipe(rm, '%s_unfinished_boots' % metal, item('sheet'), item('unfinished_boots'), metal_data.tier, Rules.bend_last, Rules.bend_second_last, Rules.shrink_third_last)

        if 'utility' in metal_data.types:
            anvil_recipe(rm, '%s_trapdoor' % metal, item('sheet'), item('trapdoor'), metal_data.tier, Rules.bend_last, Rules.draw_second_last, Rules.draw_third_last)
            anvil_recipe(rm, '%s_lamp' % metal, item('ingot'), item('lamp'), metal_data.tier, Rules.bend_last, Rules.bend_second_last, Rules.draw_third_last)
            anvil_recipe(rm, '%s_chain' % metal, item('ingot'), '16 tfc:metal/chain/%s' % metal, metal_data.tier, Rules.hit_any, Rules.hit_any, Rules.draw_last)

    hit_x3 = Rules.hit_last, Rules.hit_second_last, Rules.hit_third_last

    anvil_recipe(rm, 'refined_iron_bloom', 'tfc:raw_iron_bloom', 'tfc:refined_iron_bloom', 2, *hit_x3)
    anvil_recipe(rm, 'wrought_iron_from_bloom', 'tfc:refined_iron_bloom', 'tfc:metal/ingot/wrought_iron', 2, *hit_x3)

    for metal_in, metal_out in (
        ('pig_iron', 'high_carbon_steel'),
        ('high_carbon_steel', 'steel'),
        ('high_carbon_black_steel', 'black_steel'),
        ('high_carbon_blue_steel', 'blue_steel'),
        ('high_carbon_red_steel', 'red_steel')
    ):
        anvil_recipe(rm, '%s_ingot' % metal_out, 'tfc:metal/ingot/%s' % metal_in, 'tfc:metal/ingot/%s' % metal_out, METALS[metal_out].tier, *hit_x3)

    anvil_recipe(rm, 'iron_bars', 'tfc:metal/sheet/wrought_iron', '8 minecraft:iron_bars', 3, Rules.upset_last, Rules.punch_second_last, Rules.punch_third_last)
    anvil_recipe(rm, 'iron_bars_double', 'tfc:metal/double_sheet/wrought_iron', '16 iron_bars', 3, Rules.upset_last, Rules.punch_second_last, Rules.punch_third_last)
    anvil_recipe(rm, 'iron_door', 'tfc:metal/sheet/wrought_iron', 'minecraft:iron_door', 3, Rules.hit_last, Rules.draw_not_last, Rules.punch_not_last)
    # anvil_recipe(rm, 'red_steel_bucket', 'tfc:metal/sheet/red_steel', 'tfc:red_steel_bucket', 6, Rules.bend_last, Rules.bend_second_last, Rules.bend_third_last)
    # anvil_recipe(rm, 'blue_steel_bucket', 'tfc:metal/sheet/blue_steel', 'tfc:blue_steel_bucket', 6, Rules.bend_last, Rules.bend_second_last, Rules.bend_third_last)
    anvil_recipe(rm, 'wrought_iron_grill', 'tfc:metal/double_sheet/wrought_iron', 'tfc:wrought_iron_grill', 3, Rules.draw_any, Rules.punch_last, Rules.punch_not_last)
    anvil_recipe(rm, 'brass_mechanisms', 'tfc:metal/ingot/brass', '2 tfc:brass_mechanisms', 1, Rules.punch_last, Rules.hit_second_last, Rules.punch_third_last)

    # Welding Recipes

    for metal, metal_data in METALS.items():
        if 'part' in metal_data.types:
            welding_recipe(rm, '%s_double_ingot' % metal, item('ingot'), item('ingot'), item('double_ingot'), metal_data.tier - 1)
            welding_recipe(rm, '%s_double_sheet' % metal, item('sheet'), item('sheet'), item('double_sheet'), metal_data.tier - 1)

        if 'armor' in metal_data.types:
            welding_recipe(rm, '%s_helmet' % metal, item('unfinished_helmet'), item('sheet'), item('helmet'), metal_data.tier - 1)
            welding_recipe(rm, '%s_chestplate' % metal, item('unfinished_chestplate'), item('double_sheet'), item('chestplate'), metal_data.tier - 1)
            welding_recipe(rm, '%s_greaves' % metal, item('unfinished_greaves'), item('sheet'), item('greaves'), metal_data.tier - 1)
            welding_recipe(rm, '%s_boots' % metal, item('unfinished_boots'), item('sheet'), item('boots'), metal_data.tier - 1)

        if 'tool' in metal_data.types:
            welding_recipe(rm, '%s_shears' % metal, item('knife_blade'), item('knife_blade'), item('shears'), metal_data.tier - 1)

    for metal_in_1, metal_in_2, metal_out in (
        ('weak_steel', 'pig_iron', 'high_carbon_black_steel'),
        ('weak_blue_steel', 'black_steel', 'high_carbon_blue_steel'),
        ('weak_red_steel', 'black_steel', 'high_carbon_red_steel')
    ):
        welding_recipe(rm, '%s_ingot' % metal_out, 'tfc:metal/ingot/%s' % metal_in_1, 'tfc:metal/ingot/%s' % metal_in_2, 'tfc:metal/ingot/%s' % metal_out, METALS[metal_out].tier - 1)


def disable_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier):
    rm.recipe(name_parts, 'forge:conditional', {'recipes': []})


def collapse_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient, result: Optional[utils.Json] = None, copy_input: Optional[bool] = None):
    assert result is not None or copy_input
    rm.recipe(('collapse', name_parts), 'tfc:collapse', {
        'ingredient': ingredient,
        'result': result,
        'copy_input': copy_input
    })


def landslide_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient: utils.Json, result: utils.Json):
    rm.recipe(('landslide', name_parts), 'tfc:landslide', {
        'ingredient': ingredient,
        'result': result
    })

def chisel_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient: utils.Json, result: str, mode: str):
    rm.recipe(('chisel', mode, name_parts), 'tfc:chisel', {
        'ingredient': ingredient,
        'result': result,
        'mode': mode,
        'extra_drop': item_stack_provider(result) if mode == 'slab' else None
    })

def stone_cutting(rm: ResourceManager, name_parts: utils.ResourceIdentifier, item: str, result: str, count: int = 1) -> RecipeContext:
    return rm.recipe(('stonecutting', name_parts), 'minecraft:stonecutting', {
        'ingredient': utils.ingredient(item),
        'result': result,
        'count': count
    })


def damage_shapeless(rm: ResourceManager, name_parts: ResourceIdentifier, ingredients: Json, result: Json, group: str = None, conditions: utils.Json = None) -> RecipeContext:
    res = utils.resource_location(rm.domain, name_parts)
    rm.write((*rm.resource_dir, 'data', res.domain, 'recipes', res.path), {
        'type': 'tfc:damage_inputs_shapeless_crafting',
        'recipe': {
            'type': 'minecraft:crafting_shapeless',
            'group': group,
            'ingredients': utils.item_stack_list(ingredients),
            'result': utils.item_stack(result),
            'conditions': utils.recipe_condition(conditions)
        }
    })
    return RecipeContext(rm, res)

def damage_shaped(rm: ResourceManager, name_parts: utils.ResourceIdentifier, pattern: Sequence[str], ingredients: Json, result: Json, group: str = None, conditions: Optional[Json] = None, recipe_type: str = 'tfc:damage_inputs_shaped_crafting') -> RecipeContext:
    res = utils.resource_location(rm.domain, name_parts)
    rm.write((*rm.resource_dir, 'data', res.domain, 'recipes', res.path), {
        'type': recipe_type,
        'recipe': {
            'type': 'minecraft:crafting_shaped',
            'group': group,
            'pattern': pattern,
            'key': utils.item_stack_dict(ingredients, ''.join(pattern)[0]),
            'result': utils.item_stack(result),
            'conditions': utils.recipe_condition(conditions)
        }
    })
    return RecipeContext(rm, res)

def advanced_shaped(rm: ResourceManager, name_parts: ResourceIdentifier, pattern: Sequence[str], ingredients: Json, result: Json, input_xy: Tuple[int, int], group: str = None, conditions: Optional[Json] = None) -> RecipeContext:
    res = utils.resource_location(rm.domain, name_parts)
    rm.write((*rm.resource_dir, 'data', res.domain, 'recipes', res.path), {
        'type': 'tfc:advanced_shaped_crafting',
        'group': group,
        'pattern': pattern,
        'key': utils.item_stack_dict(ingredients, ''.join(pattern)[0]),
        'result': item_stack_provider(result),
        'input_row': input_xy[1],
        'input_column': input_xy[0],
        'conditions': utils.recipe_condition(conditions)
    })
    return RecipeContext(rm, res)

def advanced_shapeless(rm: ResourceManager, name_parts: ResourceIdentifier, ingredients: Json, result: Json, primary_ingredient: Json, group: str = None, conditions: Optional[Json] = None) -> RecipeContext:
    res = utils.resource_location(rm.domain, name_parts)
    rm.write((*rm.resource_dir, 'data', res.domain, 'recipes', res.path), {
        'type': 'tfc:advanced_shapeless_crafting',
        'group': group,
        'ingredients': utils.item_stack_list(ingredients),
        'result': result,
        'primary_ingredient': utils.ingredient(primary_ingredient),
        'conditions': utils.recipe_condition(conditions)
    })
    return RecipeContext(rm, res)

def quern_recipe(rm: ResourceManager, name: ResourceIdentifier, item: str, result: str, count: int = 1) -> RecipeContext:
    result = result if not isinstance(result, str) else utils.item_stack((count, result))
    return rm.recipe(('quern', name), 'tfc:quern', {
        'ingredient': utils.ingredient(item),
        'result': result
    })


def scraping_recipe(rm: ResourceManager, name: ResourceIdentifier, item: str, result: str, count: int = 1) -> RecipeContext:
    return rm.recipe(('scraping', name), 'tfc:scraping', {
        'ingredient': utils.ingredient(item),
        'result': utils.item_stack((count, result))
    })


def clay_knapping(rm: ResourceManager, name_parts: ResourceIdentifier, pattern: List[str], result: Json, outside_slot_required: bool = None):
    knapping_recipe(rm, 'clay_knapping', name_parts, pattern, result, outside_slot_required)


def fire_clay_knapping(rm: ResourceManager, name_parts: utils.ResourceIdentifier, pattern: List[str], result: utils.Json, outside_slot_required: bool = None):
    knapping_recipe(rm, 'fire_clay_knapping', name_parts, pattern, result, outside_slot_required)


def leather_knapping(rm: ResourceManager, name_parts: utils.ResourceIdentifier, pattern: List[str], result: utils.Json, outside_slot_required: bool = None):
    knapping_recipe(rm, 'leather_knapping', name_parts, pattern, result, outside_slot_required)


def knapping_recipe(rm: ResourceManager, knapping_type: str, name_parts: utils.ResourceIdentifier, pattern: List[str], result: utils.Json, outside_slot_required: bool = None):
    rm.recipe((knapping_type, name_parts), 'tfc:%s' % knapping_type, {
        'outside_slot_required': outside_slot_required,
        'pattern': pattern,
        'result': utils.item_stack(result)
    })


def rock_knapping(rm: ResourceManager, name, pattern: List[str], result: utils.ResourceIdentifier, ingredient: str = None, outside_slot_required: bool = False):
    ingredient = None if ingredient is None else utils.ingredient(ingredient)
    return rm.recipe(('rock_knapping', name), 'tfc:rock_knapping', {
        'outside_slot_required': outside_slot_required,
        'pattern': pattern,
        'result': utils.item_stack(result),
        'ingredient': ingredient
    })


def heat_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient: utils.Json, temperature: float, result_item: Optional[str | Json] = None, result_fluid: Optional[str] = None) -> RecipeContext:
    result_item = item_stack_provider(result_item) if isinstance(result_item, str) else result_item
    result_fluid = None if result_fluid is None else fluid_stack(result_fluid)
    return rm.recipe(('heating', name_parts), 'tfc:heating', {
        'ingredient': utils.ingredient(ingredient),
        'result_item': result_item,
        'result_fluid': result_fluid,
        'temperature': temperature
    })


def casting_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, mold: str, metal: str, amount: int, break_chance: float):
    rm.recipe(('casting', name_parts), 'tfc:casting', {
        'mold': {'item': 'tfc:ceramic/%s_mold' % mold},
        'fluid': fluid_stack_ingredient('%d tfc:metal/%s' % (amount, metal)),
        'result': utils.item_stack('tfc:metal/%s/%s' % (mold, metal)),
        'break_chance': break_chance
    })


def alloy_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, metal: str, *parts: Tuple[str, float, float]):
    rm.recipe(('alloy', name_parts), 'tfc:alloy', {
        'result': 'tfc:%s' % metal,
        'contents': [{
            'metal': 'tfc:%s' % p[0],
            'min': p[1],
            'max': p[2]
        } for p in parts]
    })


def bloomery_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, result: Json, metal: Json, catalyst: Json, time: int):
    rm.recipe(('bloomery', name_parts), 'tfc:bloomery', {
        'result': item_stack_provider(result),
        'fluid': fluid_stack_ingredient(metal),
        'catalyst': utils.ingredient(catalyst),
        'duration': time
    })

def barrel_sealed_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, translation: str, duration: int, input_item: Optional[Json] = None, input_fluid: Optional[Json] = None, output_item: Optional[Json] = None, output_fluid: Optional[Json] = None, on_seal: Optional[Json] = None, on_unseal: Optional[Json] = None, sound: Optional[str] = None):
    rm.recipe(('barrel', name_parts), 'tfc:barrel_sealed', {
        'input_item': item_stack_ingredient(input_item) if input_item is not None else None,
        'input_fluid': fluid_stack_ingredient(input_fluid) if input_fluid is not None else None,
        'output_item': item_stack_provider(output_item) if isinstance(output_item, str) else output_item,
        'output_fluid': fluid_stack(output_fluid) if output_fluid is not None else None,
        'duration': duration,
        'on_seal': on_seal,
        'on_unseal': on_unseal,
        'sound': sound
    })
    res = utils.resource_location('tfc', name_parts)
    rm.lang('tfc.recipe.barrel.' + res.domain + '.barrel.' + res.path.replace('/', '.'), lang(translation))


def barrel_instant_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, input_item: Optional[Json] = None, input_fluid: Optional[Json] = None, output_item: Optional[Json] = None, output_fluid: Optional[Json] = None, sound: Optional[str] = None):
    rm.recipe(('barrel', name_parts), 'tfc:barrel_instant', {
        'input_item': item_stack_ingredient(input_item) if input_item is not None else None,
        'input_fluid': fluid_stack_ingredient(input_fluid) if input_fluid is not None else None,
        'output_item': item_stack_provider(output_item) if output_item is not None else None,
        'output_fluid': fluid_stack(output_fluid) if output_fluid is not None else None,
        'sound': sound
    })


def loom_recipe(rm: ResourceManager, name: utils.ResourceIdentifier, ingredient: Json, input_count: int, result: Json, steps: int, in_progress_texture: str):
    return rm.recipe(('loom', name), 'tfc:loom', {
        'ingredient': utils.ingredient(ingredient),
        'input_count': input_count,
        'result': utils.item_stack(result),
        'steps_required': steps,
        'in_progress_texture': in_progress_texture
    })


def anvil_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient: Json, result: Json, tier: int, *rules: Rules, bonus: bool = None):
    rm.recipe(('anvil', name_parts), 'tfc:anvil', {
        'input': utils.ingredient(ingredient),
        'result': item_stack_provider(result),
        'tier': tier,
        'rules': [r.name for r in rules],
        'apply_forging_bonus': bonus
    })


def welding_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, first_input: Json, second_input: Json, result: Json, tier: int, ):
    rm.recipe(('welding', name_parts), 'tfc:welding', {
        'first_input': utils.ingredient(first_input),
        'second_input': utils.ingredient(second_input),
        'tier': tier,
        'result': item_stack_provider(result)
    })


def fluid_stack(data_in: Json) -> Json:
    if isinstance(data_in, dict):
        return data_in
    fluid, tag, amount, _ = utils.parse_item_stack(data_in, False)
    assert not tag, 'fluid_stack() cannot be a tag'
    return {
        'fluid': fluid,
        'amount': amount
    }


def fluid_stack_ingredient(data_in: Json) -> Json:
    if isinstance(data_in, dict):
        return {
            'ingredient': fluid_ingredient(data_in['ingredient']),
            'amount': data_in['amount']
        }
    if pair := utils.maybe_unordered_pair(data_in, int, object):
        amount, fluid = pair
        return {'ingredient': fluid_ingredient(fluid), 'amount': amount}
    fluid, tag, amount, _ = utils.parse_item_stack(data_in, False)
    if tag:
        return {'ingredient': {'tag': fluid}, 'amount': amount}
    else:
        return {'ingredient': fluid, 'amount': amount}


def fluid_ingredient(data_in: Json) -> Json:
    if isinstance(data_in, dict):
        return data_in
    elif isinstance(data_in, List):
        return [*utils.flatten_list([fluid_ingredient(e) for e in data_in])]
    else:
        fluid, tag, amount, _ = utils.parse_item_stack(data_in, False)
        if tag:
            return {'tag': fluid}
        else:
            return fluid


def item_stack_ingredient(data_in: Json):
    if isinstance(data_in, dict):
        return {
            'ingredient': utils.ingredient(data_in['ingredient']),
            'count': data_in['count'] if data_in.get('count') is not None else None
        }
    if pair := utils.maybe_unordered_pair(data_in, int, object):
        count, item = pair
        return {'ingredient': fluid_ingredient(item), 'count': count}
    item, tag, count, _ = utils.parse_item_stack(data_in, False)
    if tag:
        return {'ingredient': {'tag': item}, 'count': count}
    else:
        return {'ingredient': {'item': item}, 'count': count}

def fluid_item_ingredient(fluid: Json, delegate: Json = None):
    return {
        'type': 'tfc:fluid_item',
        'ingredient': delegate,
        'fluid_ingredient': fluid_stack_ingredient(fluid)
    }


def item_stack_provider(data_in: Json = None, copy_input: bool = False, copy_heat: bool = False, copy_food: bool = False, reset_food: bool = False, add_heat: float = None, add_trait: str = None, remove_trait: str = None, empty_bowl: bool = False, copy_forging: bool = False) -> Json:
    if isinstance(data_in, dict):
        return data_in
    stack = utils.item_stack(data_in) if data_in is not None else None
    modifiers = [k for k, v in (
        ('tfc:copy_input', copy_input),
        ('tfc:copy_heat', copy_heat),
        ('tfc:copy_food', copy_food),
        ('tfc:reset_food', reset_food),
        ('tfc:empty_bowl', empty_bowl),
        ('tfc:copy_forging_bonus', copy_forging),
        ({'type': 'tfc:add_heat', 'temperature': add_heat}, add_heat is not None),
        ({'type': 'tfc:add_trait', 'trait': add_trait}, add_trait is not None),
        ({'type': 'tfc:remove_trait', 'trait': remove_trait}, remove_trait is not None)
    ) if v]
    if modifiers:
        return {
            'stack': stack,
            'modifiers': modifiers
        }
    return stack

def not_rotten(ingredient: Json) -> Json:
    return {
        'type': 'tfc:not_rotten',
        'ingredient': utils.ingredient(ingredient)
    }

def has_trait(ingredient: Json, trait: str, invert: bool = False) -> Json:
    return {
        'type': 'tfc:lacks_trait' if invert else 'tfc:has_trait',
        'trait': trait,
        'ingredient': utils.ingredient(ingredient)
    }
