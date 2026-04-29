"""
動画生成スクリプト v3 — CogVideoX-5b (HF Space / 完全無料)
登録・APIキー不要。HF Spaces の無料 GPU を使用。
"""
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "outputs" / "02_動画" / "draft"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EMPTY_FILE = {
    "path": None, "url": None, "size": None,
    "orig_name": None, "mime_type": None,
    "is_stream": False, "meta": {"_type": "gradio.FileData"},
}

SCENES = {
    "b_roll_office": (
        "A modern bright office space with diverse professionals working on laptops, "
        "natural sunlight streams through large floor-to-ceiling windows, "
        "minimal clean interior design with plants, people gently moving and collaborating, "
        "warm golden atmosphere, slow cinematic camera pan left to right, "
        "4K quality, photorealistic, professional B-roll footage"
    ),
    "ai_instructor": (
        "A professional female presenter in a white blouse with a warm smile, "
        "looking directly at the camera in a clean white studio, "
        "soft natural lighting from the left, gentle natural head movement, "
        "subtle breathing motion, speaking to an audience, cinematic, photorealistic, "
        "medium close-up shot, professional talking-head style"
    ),
    "sns_short": (
        "Extreme close-up of hands typing on a glowing smartphone screen, "
        "dynamic neon light effects in blue and purple reflect on the fingertips, "
        "dark moody background with bokeh, fast energetic motion, "
        "social media style content creation, vertical composition, eye-catching"
    ),
}


def generate_cogvx(scene_name: str, prompt: str) -> Path | None:
    from gradio_client import Client

    print(f"\n[INFO] CogVideoX-5b Space に接続中...")
    try:
        client = Client("THUDM/CogVideoX-5b", verbose=False)
    except Exception as e:
        print(f"[ERROR] 接続失敗: {e}")
        return None

    print(f"[INFO] 生成開始: {scene_name}")
    print(f"[INFO] プロンプト: {prompt[:80]}...")
    print("[INFO] (HF 無料 GPU キューを待機中 — 数分かかる場合があります)")

    try:
        result = client.predict(
            prompt=prompt,
            image_input=EMPTY_FILE,
            video_input={"video": None, "subtitles": None},
            video_strength=0.8,
            seed_value=-1,
            scale_status=False,
            rife_status=False,
            api_name="/generate",
        )
        # result: (video_dict, download_path, gif_path, seed)
        video_dict = result[0]
        src = video_dict.get("video") if isinstance(video_dict, dict) else str(result[1])

        if not src or not Path(src).exists():
            print(f"[ERROR] 動画ファイルが見つかりません: {result}")
            return None

        ts = datetime.now().strftime("%Y-%m-%d")
        dst = OUTPUT_DIR / f"{ts}_{scene_name}_cogvx5b_draft.mp4"
        shutil.copy2(src, dst)
        size_mb = dst.stat().st_size / (1024 * 1024)
        print(f"[OK] 保存: {dst} ({size_mb:.1f}MB)")
        return dst

    except Exception as e:
        print(f"[ERROR] 生成失敗: {e}")
        return None


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(SCENES.keys())
    generated = []

    for name in targets:
        if name not in SCENES:
            print(f"[WARN] 不明なシーン: {name}")
            continue
        result = generate_cogvx(name, SCENES[name])
        if result:
            generated.append(str(result))

    print("\n=== 完了 ===")
    for p in generated:
        print(f"  → {p}")
    if not generated:
        print("  生成なし。HF Spaceのキューが混んでいる可能性があります。")


if __name__ == "__main__":
    main()
