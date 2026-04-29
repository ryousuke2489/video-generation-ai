"""
動画生成スクリプト — Wan2.1-T2V-1.3B (Apple Silicon MPS / CPU)
無料・ローカル実行。APIキー不要。
"""
import os
import sys
import torch
import imageio
import numpy as np
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "outputs" / "02_動画" / "draft"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_ID = "Wan-AI/Wan2.1-T2V-1.3B-Diffusers"

# 生成設定
CONFIGS = {
    "b_roll_office": {
        "prompt": (
            "Modern bright office space with diverse professionals working on laptops, "
            "natural sunlight through large windows, minimal clean interior design, "
            "people gently moving and collaborating, warm atmosphere, cinematic quality, "
            "slow camera pan, 4K, photorealistic"
        ),
        "negative_prompt": "blurry, low quality, distorted, watermark, text",
        "num_frames": 16,
        "height": 320,
        "width": 576,
        "guidance_scale": 5.0,
        "num_inference_steps": 20,
    },
    "ai_instructor": {
        "prompt": (
            "Professional Japanese female presenter, white blouse, warm smile, "
            "looking at camera, clean white studio background, soft natural lighting, "
            "gentle natural head movement, subtle breathing, cinematic, photorealistic"
        ),
        "negative_prompt": "blurry, distorted, watermark, text, multiple people",
        "num_frames": 16,
        "height": 576,
        "width": 320,
        "guidance_scale": 5.0,
        "num_inference_steps": 20,
    },
    "sns_short": {
        "prompt": (
            "Close-up of hands typing on a glowing smartphone, "
            "dynamic neon light effects in blue and purple, dark background, "
            "fast energetic motion, social media style, eye-catching, vertical format"
        ),
        "negative_prompt": "blurry, low quality, static, boring",
        "num_frames": 16,
        "height": 576,
        "width": 320,
        "guidance_scale": 5.0,
        "num_inference_steps": 20,
    },
}


def get_device():
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def load_pipeline(device: str):
    from diffusers import AutoencoderKLWan, WanPipeline
    from diffusers.schedulers.scheduling_unipc_multistep import UniPCMultistepScheduler
    from transformers import AutoTokenizer, UMT5EncoderModel

    print(f"[INFO] モデルを読み込み中: {MODEL_ID}")
    print(f"[INFO] デバイス: {device} (初回は ~3GB ダウンロード)")

    dtype = torch.float32  # MPS/CPU は float16 非対応のため float32

    pipe = WanPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
    )

    if device == "mps":
        pipe = pipe.to("mps")
    elif device == "cuda":
        pipe = pipe.to("cuda")
    else:
        pipe.enable_sequential_cpu_offload()

    pipe.vae.enable_slicing()

    return pipe


def generate(pipe, config_name: str, config: dict, device: str) -> Path:
    print(f"\n[INFO] 生成開始: {config_name}")
    print(f"[INFO] プロンプト: {config['prompt'][:80]}...")

    generator = torch.Generator(device="cpu").manual_seed(42)

    output = pipe(
        prompt=config["prompt"],
        negative_prompt=config.get("negative_prompt", ""),
        height=config["height"],
        width=config["width"],
        num_frames=config["num_frames"],
        guidance_scale=config["guidance_scale"],
        num_inference_steps=config["num_inference_steps"],
        generator=generator,
    )

    frames = output.frames[0]  # list of PIL images

    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = OUTPUT_DIR / f"{timestamp}_{config_name}_wan21_draft.mp4"

    # PIL frames → numpy → MP4
    frames_np = [np.array(f) for f in frames]
    imageio.mimwrite(str(filename), frames_np, fps=8, quality=8)

    print(f"[OK] 保存完了: {filename}")
    return filename


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(CONFIGS.keys())

    device = get_device()
    print(f"[INFO] デバイス選択: {device}")

    pipe = load_pipeline(device)
    generated = []

    for name in targets:
        if name not in CONFIGS:
            print(f"[WARN] 不明な設定: {name} — スキップ")
            continue
        try:
            path = generate(pipe, name, CONFIGS[name], device)
            generated.append(str(path))
        except Exception as e:
            print(f"[ERROR] {name} の生成に失敗: {e}")

    print("\n=== 生成完了 ===")
    for p in generated:
        print(f"  → {p}")


if __name__ == "__main__":
    main()
