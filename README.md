# Auto Music

一个用于 Minecraft Java Edition 1.20.1 的数据包（Datapack），通过 `block_display` 播放头沿指定方向移动，检测不同方块和 Y 高度来自动播放音符，模拟某些音乐编辑软件。

如果你需要从 NBS 文件自动生成适配播放头的音符方块投影原理图，你可以使用这个项目中的子项目（需要自行构建）：[Nbs2LitematicaEx/LitematicGenerator](https://github.com/chenjunfu2/Nbs2LitematicaEx/tree/master/LitematicGenerator)

## 功能

- 自动沿指定方向移动播放头（`block_display`）。
- 允许同时存在多个播放头。
- 根据播放头当前位置检测方块并播放对应的音符。
- Y 轴高度 `0~24` 对应 Minecraft 音符盒的 `0~24` 音高。
- 通过不同方块映射不同乐器/音色。
- 支持控制玩家是否跟随播放头。
- 内置 Python 音符函数生成器，可根据 `config.json` 配置自动生成 25 个音高的音色函数。

## 安装
点击 `Download ZIP` 下载仓库原始代码压缩包，将整个压缩包直接放入 Minecraft 世界存档的 datapacks 目录下：

```text
saves/<你的世界>/datapacks/
```

例如：

```text
.minecraft/
└── saves/
    └── MyWorld/
        └── datapacks/
            └── Auto-Music-Datapack.zip
```

进入世界后执行：

```mcfunction
/reload
```

如果加载成功，可以在聊天栏看到：

```text
[auto-music] loaded!
```

## 基本使用

### 1. 生成播放头

在你当前所在位置生成播放头：

```mcfunction
/function music:summon_playhead
```

播放头是一个 `block_display`，标签为 `music`。

### 2. 开始播放

```mcfunction
/function music:start_play
```

开始播放后，数据包会每 tick：

1. 根据计分板设置的方向移动播放头。
2. 检测播放头当前位置所有与其相交的方块。
3. 根据方块类型决定音色，Y轴高度决定音高，播放对应音符。

### 3. 停止播放

```mcfunction
/function music:stop_play
```

注意这只会停止播放，不会删除播放头。

如需删除播放头：

```mcfunction
/function music:kill_playhead
```

注意这会删除所有已加载区块内的所有播放头。

## 播放方向

播放头默认沿 X 轴正方向移动。

移动方向由计分板 `music_move_direction` 控制：

| 数值 | 方向 |
|---:|---|
| `0` | X 正方向 `+X` |
| `1` | X 负方向 `-X` |
| `2` | Z 正方向 `+Z` |
| `3` | Z 负方向 `-Z` |

可以直接修改：

```mcfunction
/scoreboard players set music_move_direction music 0
```

例如改成 Z 负方向：

```mcfunction
/scoreboard players set music_move_direction music 3
```

## 音符布局

数据包会检查播放头当前位置上方的 25 个高度：

```text
Y + 24 -> note 24
...
Y + 2  -> note 2
Y + 1  -> note 1
Y + 0  -> note 0
```

因此可以把它理解为一个纵向的 25 音阶。

例如播放头当前所在位置附近：

```text
Y+24  █  <- note 24
Y+23
...
Y+12  █  <- note 12
...
Y+1
Y+0   █  <- note 0
```

某一层如果存在对应方块，就会触发该高度对应的音符（前提是方块类型必须符合要求），如果是空气，则不会播放。

## 乐器 / 方块映射

当前 `config.json` 默认配置包含以下映射：

| 方块 | 音色 |
|---|---|
| `minecraft:oak_planks` | Bass |
| `minecraft:stone` | Basedrum |
| `minecraft:sand` | Snare |
| `minecraft:glass` | Hat |
| `minecraft:clay` | Flute |
| `minecraft:gold_block` | Bell |
| `#minecraft:wool` | Guitar |
| `minecraft:packed_ice` | Chime |
| `minecraft:bone_block` | Xylophone |
| `minecraft:iron_block` | Iron Xylophone |
| `minecraft:soul_sand` | Cow Bell |
| `minecraft:pumpkin` | Didgeridoo |
| `minecraft:emerald_block` | Bit |
| `minecraft:hay_block` | Banjo |
| `minecraft:glowstone` | Pling |
| `minecraft:dirt` | Harp |

映射配置位于：

```text
data/music/functions/音符生成器/config.json
```

每个乐器配置包含：

```json
{
  "block": "minecraft:oak_planks",
  "sound": "minecraft:block.note_block.bass",
  "source": "block"
}
```

其中：

- `block`：触发该音色的方块。
- `sound`：要播放的 Minecraft 声音事件。
- `source`：`playsound` 使用的声音类别。

## 修改音色

编辑：

```text
data/music/functions/音符生成器/config.json
```

例如增加一个新的音色：

```json
{
  "block": "minecraft:copper_block",
  "sound": "minecraft:block.note_block.cow_bell",
  "source": "block"
}
```

运行脚本即可自动重新生成 `note/*.mcfunction`。

## 音符函数生成器

生成器位于：

```text
data/music/functions/音符生成器/note_gen.py
```

需要 Python 3。

在数据包根目录执行：

```bash
python data/music/functions/音符生成器/note_gen.py
```

或者进入生成器目录后：

```bash
cd data/music/functions/音符生成器
python note_gen.py
```

也可以显式指定配置文件：

```bash
python note_gen.py config.json
```

还可以同时指定数据包根目录：

```bash
python note_gen.py config.json /path/to/datapack
```

生成器会：

- 读取 `config.json`。
- 校验配置是否合法。
- 生成 `note/0.mcfunction` 到 `note/24.mcfunction`。
- 根据 Minecraft 音符编号计算对应 pitch。
- 为每个音符生成所有配置乐器的播放命令。

生成完成后会输出每个音符对应的 pitch。

## 玩家跟随

启用玩家跟随播放头：

```mcfunction
/function music:enable_follow_playhead
```

关闭：

```mcfunction
/function music:disable_follow_playhead
```

只有在积分榜中有配置的玩家才会跟随播放头，且玩家总是会跟随距离他自己最近的播放头。

设置需要跟随播放头的玩家，请使用：

```mcfunction
/function music:set_follow_1
```

或者

```mcfunction
/function music:set_follow_2
```

由于播放头沿不同方向移动时，玩家可能需要位于播放头的不同一侧，set_follow_1 和 set_follow_2 就用于设置不同的跟随方向。

需要取消某个玩家的跟随可以使用：

```mcfunction
/function music:set_unfollow
```

来取消。

注意/function的执行者为玩家自身，

如果需要控制其它玩家，可以使用execute改变执行者，比如：

```mcfunction
/execute as <玩家名> run function music:set_follow_1
```

```mcfunction
/execute as <玩家名> run function music:set_unfollow
```

如果是命令方块，那么应该总是使用此形式配置需要跟随的玩家。

## 播放状态

数据包内部使用以下 scoreboard 中的 player 项：

```text
music_play
music_move_direction
follow_playhead
```

其中：

- `music_play = 1`：正在播放。
- `music_play = 0`：停止播放。
- `music_move_direction`：播放头移动方向。
- `follow_playhead = 1`：启用跟随。
- `follow_playhead = 0`：关闭跟随。

通常不需要手动初始化，这些目标会由：

```mcfunction
/function music:load
```

自动创建；正常使用 `/reload` 即可。

## 许可证

本项目使用MIT许可证。
