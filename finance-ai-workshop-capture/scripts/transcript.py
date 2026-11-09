#!/usr/bin/env python3
"""Normalise a Microsoft Teams transcript to one line per utterance: [hh:mm:ss] Speaker: text

Usage: transcript.py <file.vtt|file.docx|file.txt> [--session W2] > W2_transcript.txt
Handles Teams .vtt (WEBVTT with <v Speaker> tags) and the .docx download
(speaker name with a timestamp on one line, text on the next). Plain .txt is passed through.
"""
import re, sys, argparse


def hms(t):
    parts = t.split(".")[0].split(":")
    parts = [int(p) for p in parts]
    while len(parts) < 3:
        parts.insert(0, 0)
    return "%02d:%02d:%02d" % tuple(parts[-3:])


def from_vtt(text):
    out, start = [], None
    for line in text.splitlines():
        m = re.match(r"(\d{1,2}:\d{2}:\d{2}(?:\.\d+)?|\d{1,2}:\d{2}(?:\.\d+)?)\s+-->", line)
        if m:
            start = hms(m.group(1)); continue
        v = re.match(r"<v ([^>]+)>(.*?)(</v>)?$", line.strip())
        if v and start:
            out.append((start, v.group(1).strip(), re.sub(r"<[^>]+>", "", v.group(2)).strip()))
        elif line.strip() and start and not line.startswith(("WEBVTT", "NOTE")) and not re.match(r"^[0-9a-f-]{8,}(/\d+-\d+)?$", line.strip()):
            out.append((start, "", re.sub(r"<[^>]+>", "", line).strip()))
    return out


def from_docx(path):
    from docx import Document
    paras = [p.text.strip() for p in Document(path).paragraphs if p.text.strip()]
    out, i = [], 0
    while i < len(paras):
        m = re.match(r"^(.*?)\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*$", paras[i])
        if m and i + 1 < len(paras):
            out.append((hms(m.group(2)), m.group(1).strip(), paras[i + 1])); i += 2
        else:
            out.append(("", "", paras[i])); i += 1
    return out


def merge(rows):
    merged = []
    for t, s, x in rows:
        if merged and merged[-1][1] == s and s:
            merged[-1] = (merged[-1][0], s, merged[-1][2] + " " + x)
        else:
            merged.append((t, s, x))
    return merged


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--session", default="")
    a = ap.parse_args()
    if a.file.lower().endswith(".vtt"):
        rows = from_vtt(open(a.file, encoding="utf-8-sig").read())
    elif a.file.lower().endswith(".docx"):
        rows = from_docx(a.file)
    else:
        sys.stdout.write(open(a.file, encoding="utf-8-sig").read()); sys.exit()
    if a.session:
        print(f"# Session {a.session}")
    for t, s, x in merge(rows):
        print(f"[{t}] {s}: {x}" if s else f"[{t}] {x}")
