def srt_format_timestamp(seconds: float) -> str:
    milliseconds = round(seconds * 1000.0)
    hours = milliseconds // 3600000
    minutes = (milliseconds % 3600000) // 60000
    seconds = (milliseconds % 60000) // 1000
    ms = milliseconds % 1000
    return f"{hours}:{minutes:02}:{seconds:02},{ms:03}"

def write_srt(segments: list[dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            f.write(f"{i}\n")
            f.write(f"{srt_format_timestamp(seg['start'])} --> {srt_format_timestamp(seg['end'])}\n")
            f.write(f"{seg['text'].replace('-->', '->').strip()}\n\n")