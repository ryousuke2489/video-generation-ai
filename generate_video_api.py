"""
動画生成スクリプト v2 — HuggingFace Inference API
ダウンロード不要・APIキー不要（無料枠）
HF_TOKEN 環境変数があればレートリミット解除
"""
import os
import sys
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "outputs" / "02_動画" / "draft"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 試行するモデル（上から順に試す）
T2V_MODELS = [
    "damo-vilab/text-to-video-ms-1.7b",
    "ali-vilab/text-to-video-ms-1.7b",
    "cerspense/zeroscope_v2_576w",
]

SCENES = {
    "b_roll_office": {
        "prompt": (
            "Modern bright office space, professionals working on laptops, "
            "natural sunlight through large windows, minimal clean interior, "
            "people gently moving, warm atmosphere, cinematic, slow camera pan"
        ),
    },
    "ai_instructor": {
        "prompt": (
            "Professional female presenter in white blouse, warm smile, "
            "looking at camera, clean white studio background, soft lighting, "
            "gentle natural movement, cinematic, photorealistic"
        ),
    },
    "sns_short": {
        "prompt": (
            "Close-up hands typing on glowing smartphone, "
            "neon light effects blue and purple, dark background, "
            "dynamic energetic motion, social media style"
        ),
    },
}


def try_generate(client, prompt: str) -> bytes | None:
    for model in T2V_MODELS:
        print(f"  → モデル試行: {model}")
        try:
            result = client.text_to_video(prompt, model=model)
            if result:
                print(f"  ✓ 成功: {model}")
                return result
        except Exception as e:
            print(f"  ✗ 失敗 ({model}): {e}")
    return None


def main():
    from huggingface_hub import InferenceClient

    token = os.getenv("HF_TOKEN")
    client = InferenceClient(token=token) if token else InferenceClient()
    print(f"[INFO] HF_TOKEN: {'あり（認証済み）' if token else 'なし（無料匿名枠）'}")

    targets = sys.argv[1:] if len(sys.argv) > 1 else list(SCENES.keys())
    generated = []

    for name in targets:
        if name not in SCENES:
            print(f"[WARN] 不明なシーン: {name} — スキップ")
            continue

        scene = SCENES[name]
        print(f"\n[INFO] 生成開始: {name}")
        print(f"[INFO] プロンプト: {scene['prompt'][:80]}...")

        video_bytes = try_generate(client, scene["prompt"])

        if video_bytes:
            ts = datetime.now().strftime("%Y-%m-%d")
            out_path = OUTPUT_DIR / f"{ts}_{name}_hf_api_draft.mp4"
            out_path.write_bytes(video_bytes if isinstance(video_bytes, bytes) else bytes(video_bytes))
            size_kb = out_path.stat().st_size // 1024
            print(f"[OK] 保存: {out_path} ({size_kb}KB)")
            generated.append(str(out_path))
        else:
            print(f"[ERROR] {name}: 全モデル失敗")

    print("\n=== 完了 ===")
    for p in generated:
        print(f"  → {p}")
    if not generated:
        print("  生成なし（HF_TOKENの設定またはモデル変更を検討）")


if __name__ == "__main__":
    main()
