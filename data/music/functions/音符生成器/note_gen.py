#!/usr/bin/env python3

import json
import math
import sys
from pathlib import Path


def note_pitch(note: int) -> float:
    """Minecraft 音符盒 0~24 对应的 pitch。"""
    if not 0 <= note <= 24:
        raise ValueError(f"note 必须在 0~24 之间，当前为 {note}")

    return 2 ** ((note - 12) / 12)


def format_pitch(value: float) -> str:
    return f"{value:.3f}"


def load_config(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"找不到配置文件: {path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise SystemExit(
            f"config.json 格式错误：第 {e.lineno} 行，第 {e.colno} 列：{e.msg}"
        )

    if not isinstance(config, dict):
        raise SystemExit("config.json 最外层必须是对象 {}")

    namespace = config.get("namespace", "music")
    volume = config.get("volume", 32)
    min_volume = config.get("min_volume", 1)
    instruments = config.get("instruments")

    if not isinstance(namespace, str) or not namespace:
        raise SystemExit("namespace 必须是非空字符串")

    if not isinstance(instruments, list) or not instruments:
        raise SystemExit("instruments 必须是非空数组")

    if not isinstance(volume, (int, float)):
        raise SystemExit("volume 必须是数字")

    if not isinstance(min_volume, (int, float)):
        raise SystemExit("min_volume 必须是数字")

    normalized = []

    for index, item in enumerate(instruments):
        if not isinstance(item, dict):
            raise SystemExit(f"instruments[{index}] 必须是对象")

        block = item.get("block")
        sound = item.get("sound")
        source = item.get("source", "block")

        if not isinstance(block, str) or not block:
            raise SystemExit(f"instruments[{index}].block 无效")

        if not isinstance(sound, str) or not sound:
            raise SystemExit(f"instruments[{index}].sound 无效")

        if not isinstance(source, str) or not source:
            raise SystemExit(f"instruments[{index}].source 无效")

        normalized.append({
            "block": block,
            "sound": sound,
            "source": source,
        })

    # 检查是否有重复方块
    blocks = [item["block"] for item in normalized]
    duplicates = sorted({
        block for block in blocks
        if blocks.count(block) > 1
    })

    if duplicates:
        raise SystemExit(
            "检测到重复的 block："
            + ", ".join(duplicates)
        )

    return {
        "namespace": namespace,
        "volume": volume,
        "min_volume": min_volume,
        "instruments": normalized,
    }


def generate(config: dict, datapack_root: Path):
    namespace = config["namespace"]
    volume = config["volume"]
    min_volume = config["min_volume"]
    instruments = config["instruments"]

    output_dir = (
        datapack_root
        / "data"
        / namespace
        / "functions"
        / "note"
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    volume_text = f"{volume:g}"
    min_volume_text = f"{min_volume:g}"

    for note in range(25):
        pitch = note_pitch(note)
        pitch_text = format_pitch(pitch)

        lines = []

        for instrument in instruments:
            line = (
                f"execute if block ~ ~ ~ {instrument['block']} "
                f"run playsound {instrument['sound']} "
                f"{instrument['source']} @a ~ ~ ~ "
                f"{volume_text} {pitch_text} {min_volume_text}"
            )

            lines.append(line)

        output_file = output_dir / f"{note}.mcfunction"
        output_file.write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8"
        )

    print()
    print(f"生成完成：{output_dir}")
    print(f"共生成 25 个函数，每个函数 {len(instruments)} 种音色。")
    print()

    print("Pitch：")
    for note in range(25):
        print(
            f"  {note:2d} -> {format_pitch(note_pitch(note))}"
        )


def main():
    if len(sys.argv) == 1:
        # 默认读取脚本所在目录的 config.json
        script_dir = Path(__file__).resolve().parent
        config_path = script_dir / "config.json"

        # 默认数据包根目录：
        # gen.py 所在位置如果是
        #
        # data/music/functions/新建文件夹/gen.py
        #
        # 那么自动向上寻找 data 目录，并把它当作数据包根目录。
        current = script_dir
        datapack_root = None

        for parent in [current, *current.parents]:
            if (parent / "data").is_dir():
                datapack_root = parent
                break

        if datapack_root is None:
            datapack_root = current

    elif len(sys.argv) == 2:
        # python gen.py config.json
        config_path = Path(sys.argv[1]).resolve()

        current = config_path.parent
        datapack_root = None

        for parent in [current, *current.parents]:
            if (parent / "data").is_dir():
                datapack_root = parent
                break

        if datapack_root is None:
            datapack_root = current

    elif len(sys.argv) == 3:
        # python gen.py config.json datapack_root
        config_path = Path(sys.argv[1]).resolve()
        datapack_root = Path(sys.argv[2]).resolve()

    else:
        print("用法：")
        print("  python gen.py")
        print("  python gen.py config.json")
        print("  python gen.py config.json datapack_root")
        raise SystemExit(2)

    config = load_config(config_path)
    generate(config, datapack_root)


if __name__ == "__main__":
    main()