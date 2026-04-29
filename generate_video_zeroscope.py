"""
動画生成スクリプト v4 — ZeroScope V2 (HF Space / 完全無料)
登録・APIキー不要。hysts/zeroscope-v2 の無料 GPU を使用。
"""
import sys
import shutil
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "outputs" / "02_動画" / "draft"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SCENES = {
    "b_roll_office": (
        "Modern bright office space, professionals working on laptops, "
        "natural sunlight through large windows, minimal clean interior, "
        "people gently moving, warm atmosphere, cinematic, slow camera pan"
    ),
    "ai_instructor": (
        "Professional female presenter in white blouse, warm smile, "
        "looking at camera, clean white studio background, soft lighting, "
        "gentle natural movement, cinematic, photorealistic"
    ),
    "sns_short": (
        "Close-up hands typing on glowing smartphone, "
        "neon light effects blue and purple, dark background, "
        "dynamic energetic motion, social media style"
    ),
}


def generate(scene_name: str, prompt: str) -> Path | None:
    from gradio_client import Client

    print(f"\n[INFO] ZeroScope V2 Space に接続中...")
    try:
        client = Client("hysts/zeroscope-v2", verbose=False)
    except Exception as e:
        print(f"[ERROR] 接続失敗: {e}")
        return None

    print(f"[INFO] 生成開始: {scene_name}")
    print(f"[INFO] プロンプト: {prompt[:80]}...")
    print("[INFO] (HF 無料 GPU キューを待機中 — 数分かかる場合があります)")

    try:
        result = client.predict(
            prompt=prompt,
            seed=42,
            num_frames=24,
            num_inference_steps=25,
            api_name="/run",
        )
        src = result.get("video") if isinstance(result, dict) else None

        if not src or not Path(src).exists():
            print(f"[ERROR] 動画ファイルが見つかりません: {result}")
            return None

        ts = datetime.now().strftime("%Y-%m-%d")
        dst = OUTPUT_DIR / f"{ts}_{scene_name}_zeroscope_draft.mp4"
        shutil.copy2(src, dst)
        size_kb = dst.stat().st_size // 1024
        print(f"[OK] 保存: {dst} ({size_kb}KB)")
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
        result = generate(name, SCENES[name])
        if result:
            generated.append(str(result))

    print("\n=== 完了 ===")
    for p in generated:
        print(f"  → {p}")
    if not generated:
        print("  生成なし。HF Spaceのキューが混んでいる可能性があります。")


if __name__ == "__main__":
    main()
