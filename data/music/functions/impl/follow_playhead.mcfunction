execute as @a at @s if score @s music matches 1 if score music_move_direction music matches 0 run execute positioned as @e[type=minecraft:block_display,tag=music,sort=nearest,limit=1] run tp @s ~ ~12 ~9
execute as @a at @s if score @s music matches 2 if score music_move_direction music matches 0 run execute positioned as @e[type=minecraft:block_display,tag=music,sort=nearest,limit=1] run tp @s ~ ~12 ~-9

execute as @a at @s if score @s music matches 1 if score music_move_direction music matches 1 run execute positioned as @e[type=minecraft:block_display,tag=music,sort=nearest,limit=1] run tp @s ~ ~12 ~9
execute as @a at @s if score @s music matches 2 if score music_move_direction music matches 1 run execute positioned as @e[type=minecraft:block_display,tag=music,sort=nearest,limit=1] run tp @s ~ ~12 ~-9

execute as @a at @s if score @s music matches 1 if score music_move_direction music matches 2 run execute positioned as @e[type=minecraft:block_display,tag=music,sort=nearest,limit=1] run tp @s ~9 ~12 ~
execute as @a at @s if score @s music matches 2 if score music_move_direction music matches 2 run execute positioned as @e[type=minecraft:block_display,tag=music,sort=nearest,limit=1] run tp @s ~-9 ~12 ~

execute as @a at @s if score @s music matches 1 if score music_move_direction music matches 3 run execute positioned as @e[type=minecraft:block_display,tag=music,sort=nearest,limit=1] run tp @s ~9 ~12 ~
execute as @a at @s if score @s music matches 2 if score music_move_direction music matches 3 run execute positioned as @e[type=minecraft:block_display,tag=music,sort=nearest,limit=1] run tp @s ~-9 ~12 ~
