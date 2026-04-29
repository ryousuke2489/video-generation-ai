# 動画生成AI

Higgsfield AI MCP を Claude Code に接続し、**テキスト → 画像 → 動画** の一気通貫パイプラインを構築するプロジェクト。

## 概要

| 項目 | 内容 |
|------|------|
| プラットフォーム | [Higgsfield AI](https://higgsfield.ai) |
| MCP接続 | `https://mcp.higgsfield.ai/mcp` |
| 画像モデル | Soul 2.0 / Nano Banana Pro / Flux / Seedream |
| 動画モデル | Seedance / Kling / Veo / Minimax Hailuo |
| 最長動画 | 15秒 / 最大4K画質 |

## ディレクトリ構成

```
video-generation-ai/
├── README.md
├── CLAUDE.md                  ← Claude Code向け作業指示
├── 動画制作プラン_v1.md        ← 制作テーマ・プロンプト集
├── _INDEX.md                  ← 生成履歴ログ
├── assets/                    ← 入力素材（参照画像・キャラクター）
├── outputs/
│   ├── 01_画像/
│   │   ├── draft/             ← ドラフト確認用
│   │   └── final/             ← 最終品質
│   ├── 02_動画/
│   │   ├── draft/
│   │   └── final/
│   └── 03_サムネイル/
└── prompts/
    └── characters.md          ← Soul Characters ID管理
```

## セットアップ

### 1. Higgsfield MCP を Claude Code に登録

`~/.claude/settings.json` の `mcpServers` に追加:

```json
"higgsfield": {
  "url": "https://mcp.higgsfield.ai/mcp",
  "description": "Higgsfield AI: 画像生成・動画生成・キャラクター管理"
}
```

### 2. Claude Code を再起動して認証

Claude Code 再起動後、Higgsfield アカウントで OAuth 認証（APIキー不要）。

### 3. スキルを使って生成開始

```
/higgsfield-workflow
```

## 制作ワークフロー

### 基本パイプライン（画像→動画）

```
Step 1: テキストから画像生成（Soul 2.0 / Flux）
Step 2: 生成画像を image_url として動画生成へ渡す（Seedance / Kling）
Step 3: outputs/ に保存・_INDEX.md に記録
```

### コスト目安

| モデル | クレジット/生成 |
|-------|-------------|
| Soul 2.0（画像） | 0.125c |
| Nano Banana Pro（画像） | 2c |
| Kling 3.0（動画5秒） | ~7.5c |
| Seedance（動画5秒） | ~8c |

## 制作プラン v1

3セット・8シーンの制作計画 → [動画制作プラン_v1.md](動画制作プラン_v1.md) を参照。

### セット構成

| セット | テーマ | 形式 | モデル |
|-------|-------|------|-------|
| セット1 | AI講師キャラクター | 9:16 縦型 5〜8秒 | Soul→Seedance |
| セット2 | テクノロジー B-roll | 16:9 横型 8〜10秒 | Flux→Kling |
| セット3 | SNS用ショート動画 | 9:16 縦型 5〜6秒 | Seedream→Minimax |

## 関連スキル

- `higgsfield-workflow` — メインパイプライン
- `fal-ai-media` — fal.ai モデルとの補完利用
- `video-editing` — 生成後の編集・テロップ追加
- `remotion-video-creation` — 字幕・UI合成・仕上げ

## ライセンス

生成コンテンツの利用規約は [Higgsfield Terms of Use](https://higgsfield.ai/terms-of-use-agreement) に準拠。
