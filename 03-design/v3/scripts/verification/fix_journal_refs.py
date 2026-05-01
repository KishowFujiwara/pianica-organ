#!/usr/bin/env python3
"""
ジャーナル間相互参照の章別マッピング修正

旧構造: journals/2026-04/0430b_xxx.md
新構造: journals/02-physics/2026-04/0430b_xxx.md

各ファイルからの相対パスを、参照先の章を見て計算し直す:
- 同章同月: ./basename
- 同章別月: ../{tgt_ym}/basename
- 別章: ../../{tgt_chapter}/{tgt_ym}/basename
"""

import re
from pathlib import Path

REPO = Path("/home/claude/pianica-organ")

# basename → (chapter, year_month) のマップ
journal_map = {}
for p in REPO.glob("journals/*/2026-*/*.md"):
    parts = p.relative_to(REPO).parts
    # journals/XX-YYY/ZZZZ-MM/basename.md
    if len(parts) >= 4:
        chapter = parts[1]
        year_month = parts[2]
        journal_map[p.name] = (chapter, year_month)

print(f"Journal map: {len(journal_map)} entries")
print()

def calc_rel_path(src_path: Path, tgt_basename: str) -> str:
    """source から target basename への相対パスを計算"""
    if tgt_basename not in journal_map:
        return None
    
    src_parts = src_path.relative_to(REPO).parts
    tgt_chapter, tgt_ym = journal_map[tgt_basename]
    
    # source は journals/{chapter}/{ym}/foo.md の形
    if len(src_parts) >= 4 and src_parts[0] == "journals":
        src_chapter = src_parts[1]
        src_ym = src_parts[2]
        
        if src_chapter == tgt_chapter and src_ym == tgt_ym:
            return f"./{tgt_basename}"
        elif src_chapter == tgt_chapter:
            return f"../{tgt_ym}/{tgt_basename}"
        else:
            return f"../../{tgt_chapter}/{tgt_ym}/{tgt_basename}"
    
    # journals/外からの参照
    return f"journals/{tgt_chapter}/{tgt_ym}/{tgt_basename}"

# 修正パターン
# パターン1: ../2026-XX/basename.md (旧構造ジャーナル間参照)
# パターン2: ../../journals/2026-XX/basename.md (旧構造非ジャーナルからの参照)
# パターン3: journals/2026-XX/basename.md (絶対っぽい記述)

modified_files = []

# 全リポジトリのMD/HTMLを対象に
for p in REPO.rglob("*.md"):
    if ".git" in p.parts:
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    original = text
    
    # パターン1: ../2026-XX/basename.md
    def replace_pattern1(m):
        ym = m.group(1)
        basename = m.group(2)
        if basename in journal_map:
            tgt_chapter, tgt_ym = journal_map[basename]
            # ジャーナル内参照のみ処理
            src_parts = p.relative_to(REPO).parts
            if len(src_parts) >= 4 and src_parts[0] == "journals":
                rel = calc_rel_path(p, basename)
                if rel:
                    return rel
        return m.group(0)
    
    text = re.sub(r'\.\./(2026-0[45])/(\w+_opus_\w+\.md)', replace_pattern1, text)
    
    # パターン2: ../../journals/2026-XX/basename.md または ../../../journals/2026-XX/basename.md
    def replace_pattern2(m):
        prefix = m.group(1)
        ym = m.group(2)
        basename = m.group(3)
        if basename in journal_map:
            tgt_chapter, tgt_ym = journal_map[basename]
            src_parts = p.relative_to(REPO).parts
            
            # journals/外からの参照 (例: 02-physics/foo.md → journals/02-physics/2026-04/0430b.md)
            if src_parts[0] != "journals":
                # 深さに応じて相対パスを構築
                # 例: 02-physics/22-paths/foo.md (深さ3) → journals/.../bar.md
                # ../../journals/02-physics/2026-04/bar.md
                depth = len(src_parts) - 1  # ファイル名を除く深さ
                up = "../" * depth
                return f"{up}journals/{tgt_chapter}/{tgt_ym}/{basename}"
        return m.group(0)
    
    text = re.sub(r'(\.\./\.\./|\.\./\.\./\.\./)journals/(2026-0[45])/(\w+_opus_\w+\.md)', replace_pattern2, text)
    
    # パターン3: journals/2026-XX/basename.md (絶対っぽい)
    def replace_pattern3(m):
        ym = m.group(1)
        basename = m.group(2)
        if basename in journal_map:
            tgt_chapter, tgt_ym = journal_map[basename]
            return f"journals/{tgt_chapter}/{tgt_ym}/{basename}"
        return m.group(0)
    
    # 単独パターンマッチ (前にスラッシュやドットがないもの)
    text = re.sub(r'(?<![./\w])journals/(2026-0[45])/(\w+_opus_\w+\.md)', replace_pattern3, text)
    
    # パターン4: ../journals/2026-XX/basename.md → ../journals/{chapter}/2026-XX/basename.md
    def replace_pattern4(m):
        ym = m.group(1)
        basename = m.group(2)
        if basename in journal_map:
            tgt_chapter, tgt_ym = journal_map[basename]
            src_parts = p.relative_to(REPO).parts
            if src_parts[0] != "journals":
                depth = len(src_parts) - 1
                up = "../" * depth
                return f"{up}journals/{tgt_chapter}/{tgt_ym}/{basename}"
        return m.group(0)
    
    text = re.sub(r'\.\./journals/(2026-0[45])/(\w+_opus_\w+\.md)', replace_pattern4, text)
    
    if text != original:
        p.write_text(text, encoding="utf-8")
        modified_files.append(str(p.relative_to(REPO)))

print(f"修正ファイル数: {len(modified_files)}")
for f in modified_files[:20]:
    print(f"  {f}")
if len(modified_files) > 20:
    print(f"  ... +{len(modified_files)-20}件")
