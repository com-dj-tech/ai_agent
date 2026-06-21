"""
Typecast TTS Script
API: https://api.typecast.ai/v1/text-to-speech
"""

import argparse
import os
import sys
import requests

API_KEY = "__pltA5r3KcikZWEKGAZ3BewYN5nNkkG24Hf2ivjBuqds"
DEFAULT_VOICE_ID = "tc_69c1f8e4f8842d80fbe7fa4f"  # 우니
DEFAULT_MODEL = "ssfm-v30"
API_URL = "https://api.typecast.ai/v1/text-to-speech"


def synthesize(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model: str = DEFAULT_MODEL,
    audio_format: str = "mp3",
    output_path: str = "output.mp3",
    volume: int = 100,
    audio_tempo: float = 1.0,
) -> str:
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model": model,
        "voice_id": voice_id,
        "output": {
            "audio_format": audio_format,
            "volume": volume,
            "audio_tempo": audio_tempo,
        },
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

    if response.status_code != 200:
        print(f"[ERROR] HTTP {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Typecast TTS CLI")
    parser.add_argument("text", help="변환할 텍스트")
    parser.add_argument("--voice-id", default=DEFAULT_VOICE_ID, help="Voice ID")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="TTS 모델")
    parser.add_argument("--format", default="mp3", choices=["mp3", "wav"], help="오디오 포맷")
    parser.add_argument("--output", default="output.mp3", help="출력 파일 경로")
    parser.add_argument("--tempo", type=float, default=1.0, help="재생 속도 (0.5~2.0)")
    parser.add_argument("--volume", type=int, default=100, help="볼륨 (0~200)")
    args = parser.parse_args()

    print(f"[TTS] 텍스트: {args.text}")
    print(f"[TTS] Voice ID: {args.voice_id} | 모델: {args.model} | 포맷: {args.format}")

    saved = synthesize(
        text=args.text,
        voice_id=args.voice_id,
        model=args.model,
        audio_format=args.format,
        output_path=args.output,
        volume=args.volume,
        audio_tempo=args.tempo,
    )

    size_kb = os.path.getsize(saved) / 1024
    print(f"[OK] 저장 완료: {saved} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
