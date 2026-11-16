---
name: podcast-clipper-search
description: Transcribe long podcasts or videos locally with Whisper, build a timestamped full-text search index, and clip highlight segments with ffmpeg and captions. Use when the user asks to search inside a long podcast/video, find specific quotes, or cut short social clips from long recordings.
allowed-tools: client
---
# Podcast Clipper & Search

Transcribe long podcasts or video recordings locally, search across timestamped transcripts, and extract clean highlight clips with `ffmpeg` and optional burned-in subtitles.

## When to Use

- The user has a long podcast, lecture, or interview (`.mp3`, `.wav`, `.mp4`, `.mkv`) and wants to search what was said.
- The user wants to extract 30-90 second highlight clips around specific topics or quotes.
- The user wants vertical/landscape clips with clean `.srt` captions.

## Steps

### 1. Check Tools (`ffmpeg` and Whisper)

Verify `ffmpeg` and a local transcription tool (`whisper`, `faster-whisper`, or `whisper-cli`):

```bash
ffmpeg -version | head -n 1 && which whisper || python3 -c "import faster_whisper; print('faster-whisper OK')"
```

### 2. Transcribe with Word/Segment Timestamps

Generate `.json` and `.srt` transcripts once and save them beside the media file so searches are instant:

```bash
whisper "/path/to/episode.mp4" --model medium --output_format all --output_dir /tmp/podcast_transcripts
```

### 3. Search and Identify Clip Windows

- Search the `.json`/`.srt` transcript for keywords, themes, or strong standalone hooks.
- Present candidate clips with exact `[HH:MM:SS -> HH:MM:SS]` timestamps and a 1-line quote preview so the user can confirm which ones to cut.

### 4. Cut Clips with `ffmpeg`

Extract accurate clips (add a small 0.3s pad at boundaries, re-encode cleanly for frame-accurate cuts, and optionally burn `.srt` subtitles):

```bash
ffmpeg -ss 00:12:34.0 -to 00:13:28.5 -i "/path/to/episode.mp4" \
  -c:v libx264 -c:a aac -movflags +faststart "/tmp/clip_01.mp4"
```

## Gotchas

- **Input `-ss` placement**: Putting `-ss` before `-i` is fast, but pair it with re-encoding (`-c:v libx264 -c:a aac`) for frame-accurate cuts; `-c copy` can land on distant keyframes and clip speech.
- **Line length for captions**: Keep burned-in subtitle lines under 42 characters and 2 lines max for readability on mobile.
- **Cache transcripts**: Never re-transcribe a 2-hour file for every search query—save the `.json`/`.srt` output first.
