#!/usr/bin/env python3
"""
ディレクトリ別 全単射写像検証 (修正版)

修正点:
- 参照抽出元を MD/HTML のみに限定 (SVG/JSON/PYからの抽出を除外)
- ディレクトリの性質別に評価指標を分ける:
  * Leaf (画像/補助データのみ): 外部被参照率のみ
  * Spec (仕様書1つ + 補助): 内部完結率 + 外部被参照率
  * Journal (時系列ジャーナル): 個々の参照健全性
  * Hub (READMEで束ねる): 内部参照網羅率
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, deque

REPO = Path("/home/claude/pianica-organ")

FILE_EXTS = {".md", ".svg", ".png", ".jpg", ".jpeg", ".docx", ".html", ".json", ".py"}
# 参照抽出を行うのは MD と HTML のみに限定
REF_SOURCE_EXTS = {".md", ".html"}

REF_PATTERNS = [
    re.compile(r'\[[^\]]*\]\(([^)]+\.(?:md|svg|png|jpg|jpeg|docx|html|json|py))\)', re.IGNORECASE),
    re.compile(r'!\[[^\]]*\]\(([^)]+\.(?:md|svg|png|jpg|jpeg))\)', re.IGNORECASE),
    re.compile(r'`([^`\s]+\.(?:md|svg|png|jpg|jpeg|docx|html|json|py))`', re.IGNORECASE),
    re.compile(r'(?:^|\s|"|\')((?:\.\./)*[\w\-./]+/[\w\-/.]+\.(?:md|svg|png|jpg|jpeg|docx|html|json|py))', re.IGNORECASE | re.MULTILINE),
    re.compile(r'(?:^|\s|"|\')([\w\-]+\.(?:md|svg|png|jpg|jpeg|docx|html|json|py))(?:\s|$|"|\'|\.|,|;|:|\)|\])', re.IGNORECASE | re.MULTILINE),
]

def collect_all_files():
    all_files = set()
    basename_to_paths = defaultdict(set)
    for path in REPO.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_file() and path.suffix.lower() in FILE_EXTS:
            rel = str(path.relative_to(REPO))
            all_files.add(rel)
            basename_to_paths[path.name].add(rel)
    return all_files, basename_to_paths

def resolve_ref(raw_ref, source_path, all_files, basename_to_paths):
    raw_ref = raw_ref.strip().strip('"').strip("'")
    if raw_ref.startswith(("http://", "https://", "/")):
        return None
    
    if raw_ref in all_files:
        return raw_ref
    
    source_dir = (REPO / source_path).parent
    try:
        rel = (source_dir / raw_ref).resolve().relative_to(REPO)
        if str(rel) in all_files:
            return str(rel)
    except (ValueError, OSError):
        pass
    
    basename = Path(raw_ref).name
    if basename in basename_to_paths:
        cands = list(basename_to_paths[basename])
        if len(cands) == 1:
            return cands[0]
        try:
            same_dir_str = str((REPO / source_path).parent.relative_to(REPO))
            same_dir = [c for c in cands if str(Path(c).parent) == same_dir_str]
            if same_dir:
                return same_dir[0]
        except ValueError:
            pass
        return cands[0]
    
    return None

def extract_refs(file_path, all_files, basename_to_paths):
    p = REPO / file_path
    if p.suffix.lower() not in REF_SOURCE_EXTS:
        return set(), set()
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return set(), set()
    
    raw_refs = set()
    for pattern in REF_PATTERNS:
        for m in pattern.findall(text):
            raw_refs.add(m)
    
    self_basename = Path(file_path).name
    raw_refs = {r for r in raw_refs if Path(r).name != self_basename}
    
    resolved = set()
    ghost = set()
    for r in raw_refs:
        res = resolve_ref(r, file_path, all_files, basename_to_paths)
        if res:
            resolved.add(res)
        else:
            ghost.add(r)
    return resolved, ghost

def normalize_dir(path_str):
    p = Path(path_str)
    return str(p.parent) if str(p.parent) != "." else "<root>"

def classify_dir(d, files):
    """ディレクトリの性質を分類"""
    text_count = sum(1 for f in files if Path(f).suffix.lower() in REF_SOURCE_EXTS)
    has_journal = any("journals/" in f for f in files)
    has_readme = any(Path(f).name == "README.md" for f in files)
    
    if has_journal:
        return "Journal"
    if text_count == 0:
        return "Leaf"  # 画像のみ
    if "/figures" in d or "/images" in d:
        return "Figures"  # SVG/MDの説明組
    if has_readme and text_count == 1:
        return "Index"   # READMEのみ
    if has_readme:
        return "Hub"     # README + 仕様書
    return "Spec"        # 仕様書のみ

def main():
    all_files, basename_to_paths = collect_all_files()
    
    file_refs_out = {}
    file_ghosts_out = {}
    incoming = defaultdict(set)
    
    for f in all_files:
        if Path(f).suffix.lower() in REF_SOURCE_EXTS:
            resolved, ghost = extract_refs(f, all_files, basename_to_paths)
            file_refs_out[f] = resolved
            file_ghosts_out[f] = ghost
            for tgt in resolved:
                incoming[tgt].add(f)
        else:
            file_refs_out[f] = set()
            file_ghosts_out[f] = set()
    
    dir_files = defaultdict(set)
    for f in all_files:
        dir_files[normalize_dir(f)].add(f)
    
    dir_stats = {}
    for d, files in dir_files.items():
        text_files = {f for f in files if Path(f).suffix.lower() in REF_SOURCE_EXTS}
        non_text_files = files - text_files
        
        # 内部到達率: D内テキスト起点で D内ファイルへの推移閉包
        reachable_in_d = set(text_files)
        queue = deque(text_files)
        while queue:
            current = queue.popleft()
            for tgt in file_refs_out.get(current, set()):
                if tgt in files and tgt not in reachable_in_d:
                    reachable_in_d.add(tgt)
                    queue.append(tgt)
        
        # 被参照状況
        externally_referenced = set()
        internally_referenced = set()
        not_referenced = set()
        for f in files:
            sources = incoming.get(f, set())
            external_sources = {s for s in sources if normalize_dir(s) != d}
            internal_sources = {s for s in sources if normalize_dir(s) == d and s != f}
            if external_sources:
                externally_referenced.add(f)
            if internal_sources:
                internally_referenced.add(f)
            if not external_sources and not internal_sources:
                not_referenced.add(f)
        
        # 真の孤児: 引用されない かつ 自身も他を引用しない
        # (ただしREADMEは主体的なので除外)
        true_orphan = set()
        for f in not_referenced:
            outgoing = file_refs_out.get(f, set())
            if not outgoing and Path(f).name != "README.md":
                true_orphan.add(f)
        
        # D内エントリの外向き参照
        outgoing_to_external = set()
        outgoing_to_internal = set()
        for f in text_files:
            for tgt in file_refs_out.get(f, set()):
                if tgt in files:
                    outgoing_to_internal.add(tgt)
                else:
                    outgoing_to_external.add(tgt)
        
        ghost_out = set()
        for f in text_files:
            ghost_out.update(file_ghosts_out.get(f, set()))
        
        dir_type = classify_dir(d, files)
        
        # 評価指標 (ディレクトリ性質別)
        if dir_type in ("Leaf", "Figures") and len(text_files) == 0:
            # 画像のみ: 外部被参照率
            score = (len(externally_referenced) / len(files) * 100) if files else 0
            score_label = "外部被参照率"
        elif dir_type == "Figures":
            # 図 + 説明MD混在: 内部完結
            score = (len(reachable_in_d) / len(files) * 100) if files else 0
            score_label = "内部完結率"
        elif dir_type == "Journal":
            # ジャーナル: 内部完結率 (時系列なので内部参照の網)
            internal_internally_ref = len(internally_referenced) / len(text_files) * 100 if text_files else 0
            score = internal_internally_ref
            score_label = "内部相互参照率"
        elif dir_type in ("Hub", "Spec", "Index"):
            # ハブ/仕様: 内部完結率
            score = (len(reachable_in_d) / len(files) * 100) if files else 0
            score_label = "内部完結率"
        else:
            score = 0
            score_label = "?"
        
        dir_stats[d] = {
            "type": dir_type,
            "total_files": len(files),
            "text_files": len(text_files),
            "non_text_files": len(non_text_files),
            "reachable_internally": len(reachable_in_d),
            "internal_reach_rate": len(reachable_in_d) / len(files) if files else 0.0,
            "externally_referenced": len(externally_referenced),
            "internally_referenced": len(internally_referenced),
            "not_referenced": len(not_referenced),
            "true_orphan_count": len(true_orphan),
            "true_orphan_files": sorted(true_orphan),
            "outgoing_external_count": len(outgoing_to_external),
            "outgoing_internal_count": len(outgoing_to_internal),
            "ghost_refs_count": len(ghost_out),
            "ghost_refs_list": sorted(ghost_out),
            "score": score,
            "score_label": score_label,
        }
    
    print(f"=== ディレクトリ別 全単射性検証 (修正版, {len(dir_files)} ディレクトリ) ===\n")
    print(f"{'Directory':<50} {'Type':<8} {'Files':>5} {'Txt':>4} {'Reach':>6} {'Ext参':>5} {'Int参':>5} {'Orph':>5} {'Ghost':>5} {'Score':>7}")
    print("-" * 113)
    
    for d in sorted(dir_files.keys()):
        s = dir_stats[d]
        files_str = f"{s['total_files']}"
        txt_str = f"{s['text_files']}"
        reach_str = f"{int(s['internal_reach_rate']*100)}%" if s['total_files'] > 0 else "-"
        ext_str = str(s['externally_referenced']) if s['externally_referenced'] > 0 else "-"
        int_str = str(s['internally_referenced']) if s['internally_referenced'] > 0 else "-"
        orph_str = str(s['true_orphan_count']) if s['true_orphan_count'] > 0 else "-"
        ghost_str = str(s['ghost_refs_count']) if s['ghost_refs_count'] > 0 else "-"
        score_str = f"{int(s['score'])}%"
        print(f"{d:<50} {s['type']:<8} {files_str:>5} {txt_str:>4} {reach_str:>6} {ext_str:>5} {int_str:>5} {orph_str:>5} {ghost_str:>5} {score_str:>7}")
    
    # サマリ
    total_files = sum(s['total_files'] for s in dir_stats.values())
    total_orphans = sum(s['true_orphan_count'] for s in dir_stats.values())
    total_ghosts = sum(s['ghost_refs_count'] for s in dir_stats.values())
    
    print()
    print(f"=== 全体サマリ ===")
    print(f"全ディレクトリ数: {len(dir_files)}")
    print(f"全ファイル数    : {total_files}")
    print(f"真の孤児合計    : {total_orphans}")
    print(f"幽霊参照合計    : {total_ghosts}")
    
    # ディレクトリ性質別集計
    print()
    print(f"=== ディレクトリ性質別集計 ===")
    type_count = defaultdict(int)
    type_files = defaultdict(int)
    type_orphan = defaultdict(int)
    type_ghost = defaultdict(int)
    for d, s in dir_stats.items():
        type_count[s['type']] += 1
        type_files[s['type']] += s['total_files']
        type_orphan[s['type']] += s['true_orphan_count']
        type_ghost[s['type']] += s['ghost_refs_count']
    print(f"{'Type':<10} {'#Dir':>5} {'#Files':>7} {'Orphan':>7} {'Ghost':>6}")
    for t in sorted(type_count.keys()):
        print(f"{t:<10} {type_count[t]:>5} {type_files[t]:>7} {type_orphan[t]:>7} {type_ghost[t]:>6}")
    
    out = {
        "summary": {
            "total_dirs": len(dir_files),
            "total_files": total_files,
            "total_orphans": total_orphans,
            "total_ghosts": total_ghosts,
        },
        "by_type": {t: {"dirs": type_count[t], "files": type_files[t], "orphans": type_orphan[t], "ghosts": type_ghost[t]} for t in type_count},
        "by_directory": dir_stats,
    }
    
    output_path = REPO / "03-design/v3/scripts/verification/bijection_by_dir_v2.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n=> 詳細: {output_path}")
    
    return out

if __name__ == "__main__":
    main()
