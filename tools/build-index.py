#!/usr/bin/env python3
"""Build a standalone index.html (GitHub Pages / any phone browser) from the artifact fragment trypanon.html.
The artifact host adds <!doctype>, <head> and the viewport for us; a plain web host does not, so we add them here."""
import sys,pathlib
src=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '/home/claude/trypanon.html').read_text()
head='''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, maximum-scale=1, user-scalable=no">
<title>트리파논 · 지구를 뚫어라</title>
<meta name="description" content="한반도 한가운데 양구에서 지구 반대편까지 — 방치형 시추 게임">
<meta name="theme-color" content="#0e1315"><meta name="color-scheme" content="dark only">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="트리파논">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="icon" type="image/png" sizes="512x512" href="icon-512.png">
<link rel="manifest" href="manifest.webmanifest">
<style>:root{color-scheme:dark only}html,body{margin:0;background:#0e1315;-webkit-text-size-adjust:100%;overscroll-behavior:none}</style>
</head>
<body>
'''
pathlib.Path(sys.argv[2] if len(sys.argv)>2 else 'index.html').write_text(head+src+'\n</body>\n</html>\n')
print('built index.html',len(head+src))
