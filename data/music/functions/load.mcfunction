scoreboard objectives add music dummy "Auto-Music"
execute unless score music_move_direction music matches -2147483648..2147483647 run scoreboard players set music_move_direction music 0
execute unless score music_play music matches -2147483648..2147483647 run scoreboard players set music_play music 0
execute unless score follow_playhead music matches -2147483648..2147483647 run scoreboard players set follow_playhead music 0
tellraw @a "[auto-music] loaded!"
