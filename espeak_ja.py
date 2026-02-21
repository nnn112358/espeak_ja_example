# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pykakasi",
#   "py-espeak-ng",
# ]
# ///

"""espeak-ng を使った日本語音声合成スクリプト"""

import tempfile
import subprocess
import time
from pathlib import Path

import pykakasi
from espeakng import ESpeakNG


def to_hiragana(text: str) -> str:
    """漢字混じりテキストをひらがなに変換する。"""
    kks = pykakasi.kakasi()
    result = kks.convert(text)
    return "".join(item["hira"] for item in result)


def synthesize(
    text: str,
    voice: str = "jpx/ja",
    speed: int = 150,
    pitch: int = 50,
    output_file: str | None = None,
) -> bytes:
    """テキストを ESpeakNG で合成して WAV バイト列を返す。"""
    t0 = time.perf_counter()

    hiragana = to_hiragana(text)
    t1 = time.perf_counter()
    print(f"ひらがな: {hiragana}  ({(t1-t0)*1000:.1f}ms)")

    engine = ESpeakNG(voice=voice, speed=speed, pitch=pitch)
    print(f"音素:    {engine.g2p(hiragana)}")
    print(f"IPA(1):  {engine.g2p(hiragana, ipa=1)}")
    print(f"IPA(2):  {engine.g2p(hiragana, ipa=2)}")

    t2 = time.perf_counter()
    wav_bytes = engine.synth_wav(hiragana)
    t3 = time.perf_counter()
    print(f"合成:    {(t3-t2)*1000:.1f}ms")
    print(f"合計:    {(t3-t0)*1000:.1f}ms")

    if output_file:
        Path(output_file).write_bytes(wav_bytes)
        print(f"保存: {output_file}")

    return wav_bytes


def play(wav_bytes: bytes) -> None:
    """WAV バイト列を再生する (aplay 使用)。"""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(wav_bytes)
        tmp_path = f.name

    for player in ["aplay", "paplay", "ffplay"]:
        result = subprocess.run(["which", player], capture_output=True)
        if result.returncode == 0:
            subprocess.run([player, tmp_path])
            break
    else:
        print("再生コマンド (aplay/paplay/ffplay) が見つかりません。")

    Path(tmp_path).unlink(missing_ok=True)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="espeak-ng 日本語 TTS")
    parser.add_argument("text", nargs="?", default="こんにちは、世界！", help="読み上げるテキスト")
    parser.add_argument("-v", "--voice", default="jpx/ja", help="ボイス (デフォルト: jpx/ja)")
    parser.add_argument("-s", "--speed", type=int, default=150, help="速度 words/min (デフォルト: 150)")
    parser.add_argument("-p", "--pitch", type=int, default=50, help="ピッチ 0-99 (デフォルト: 50)")
    parser.add_argument("-o", "--output", help="出力 WAV ファイルパス")
    parser.add_argument("--play", action="store_true", help="合成後に再生する")
    parser.add_argument("--mbrola", action="store_true", help="mb/mb-jp1〜jp3 の3ボイスで一括出力")
    args = parser.parse_args()

    print(f"テキスト: {args.text}")

    if args.mbrola:
        for voice in ["mb/mb-jp1", "mb/mb-jp2", "mb/mb-jp3"]:
            tag = voice.split("-")[-1]
            out = f"output_{tag}.wav"
            print(f"\n--- {voice} ---")
            print(f"速度: {args.speed}  ピッチ: {args.pitch}")
            try:
                wav = synthesize(text=args.text, voice=voice, speed=args.speed, pitch=args.pitch, output_file=out)
                print(f"WAV サイズ: {len(wav):,} bytes")
            except Exception as e:
                print(f"エラー: {e}")
        return

    print(f"ボイス: {args.voice}  速度: {args.speed}  ピッチ: {args.pitch}")

    wav = synthesize(
        text=args.text,
        voice=args.voice,
        speed=args.speed,
        pitch=args.pitch,
        output_file=args.output,
    )

    print(f"WAV サイズ: {len(wav):,} bytes")

    if args.play:
        print("再生中...")
        play(wav)
    elif not args.output:
        default_out = "output.wav"
        Path(default_out).write_bytes(wav)
        print(f"保存: {default_out}")


if __name__ == "__main__":
    main()
