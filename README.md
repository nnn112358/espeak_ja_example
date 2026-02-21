# espeak_ja

espeak-ng を使った日本語音声合成スクリプト。
漢字→ひらがな変換 (pykakasi) → 音素変換 (ESpeakNG) → WAV 出力のパイプラインで動作する。

## 必要なもの

```bash
# espeak-ng 本体
sudo apt-get install -y espeak-ng

# MBROLA ボイス (--mbrola オプションを使う場合)
sudo apt-get install -y mbrola mbrola-jp1 mbrola-jp2 mbrola-jp3
```

Python パッケージは uv が自動でインストールする。

## 使い方

```bash
# デフォルト文 → output.wav
uv run espeak_ja.py

# テキスト指定
uv run espeak_ja.py "日本語のテキストを読み上げます"

# ファイル出力先を指定
uv run espeak_ja.py "こんにちは" -o hello.wav

# 速度・ピッチ調整
uv run espeak_ja.py "ゆっくり話します" -s 100 -p 70

# 再生 (aplay / paplay / ffplay のいずれか必要)
uv run espeak_ja.py "再生テスト" --play

# MBROLA 3ボイスで一括出力 → output_jp1.wav / jp2.wav / jp3.wav
uv run espeak_ja.py "テキスト" --mbrola
```

## オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| `text` | `こんにちは、世界！` | 読み上げるテキスト |
| `-v`, `--voice` | `jpx/ja` | ボイス名 |
| `-s`, `--speed` | `150` | 速度 words/min (80〜500) |
| `-p`, `--pitch` | `50` | ピッチ (0〜99) |
| `-o`, `--output` | — | 出力 WAV ファイルパス |
| `--play` | — | 合成後に再生する |
| `--mbrola` | — | mb/mb-jp1〜jp3 の3ボイスで一括出力 |

## 利用可能な日本語ボイス

| ボイス | 性別 | 備考 |
|---|---|---|
| `jpx/ja` | 男声 | デフォルト。追加インストール不要 |
| `mb/mb-jp1` | 男声 | mbrola-jp1 が必要 |
| `mb/mb-jp2` | 女声 | mbrola-jp2 が必要 |
| `mb/mb-jp3` | 女声 | mbrola-jp3 が必要 |

## 出力例

```
テキスト: 日本語のテキストを読み上げます
ボイス: jpx/ja  速度: 150  ピッチ: 50
ひらがな: にほんごのてきすとをよみあげます  (363.8ms)
音素:    n,ihoNg,onot,ekis,uto,ojom,iagem'asu
IPA(1):  n_ˌi_h_o̞_ŋ_ɡ_ˌo̞_n_o̞_t_ˌe̞_k_i_s_ˌɯᵝ_t_o̞_ˌo̞_j_o̞_m_ˌi_ä_ɡ_e̞_m_ˈä_s_ɯᵝ
IPA(2):  nˌiho̞ŋɡˌo̞no̞tˌe̞kisˌɯ͡ᵝto̞ˌo̞jo̞mˌiäɡe̞mˈäsɯ͡ᵝ
合成:    10.4ms
合計:    405.1ms
WAV サイズ: 115,846 bytes
保存: output.wav
```

## 依存

- [espeak-ng](https://github.com/espeak-ng/espeak-ng) — 音声合成エンジン
- [py-espeak-ng](https://pypi.org/project/py-espeak-ng/) — espeak-ng Python ラッパー
- [pykakasi](https://pypi.org/project/pykakasi/) — 漢字→ひらがな変換
