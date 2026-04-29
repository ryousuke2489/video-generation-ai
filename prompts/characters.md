# Soul Characters — キャラクター管理

Higgsfield の Soul Characters を使う場合、ここにキャラクターIDと設定を記録する。

## 登録キャラクター

| 名前 | Soul Character ID | 用途 | 登録日 |
|------|-----------------|------|-------|
| — | — | — | — |

## 使い方

```
# キャラクターを指定して画像生成
generate_image(
  character_id: "<soul_character_id>",
  prompt: "ビジネスミーティング中のシーン、オフィス背景",
  style: "cinematic"
)

# キャラクターを使って動画生成
generate_video(
  character_id: "<soul_character_id>",
  prompt: "カメラに向かって話しかける、自然な動作",
  duration: 5
)
```
