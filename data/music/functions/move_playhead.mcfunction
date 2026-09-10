execute if score music_move_direction music matches 0 run execute as @e[type=minecraft:block_display,tag=music] at @s run tp @s ~1 ~ ~
execute if score music_move_direction music matches 1 run execute as @e[type=minecraft:block_display,tag=music] at @s run tp @s ~-1 ~ ~
execute if score music_move_direction music matches 2 run execute as @e[type=minecraft:block_display,tag=music] at @s run tp @s ~ ~ ~1
execute if score music_move_direction music matches 3 run execute as @e[type=minecraft:block_display,tag=music] at @s run tp @s ~ ~ ~-1
