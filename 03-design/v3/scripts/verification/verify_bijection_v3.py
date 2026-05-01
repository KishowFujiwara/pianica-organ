#!/usr/bin/env python3
"""
v3: 推移閉包による全単射写像検証

論理:
- ユーザの指示「すべてのジャーナルとすべてのジャーナルに記されている
  すべてのMDファイルなどの悉皆性を全単射写像検証」
- 解釈:
  - 起点 = 全ジャーナル
  - そこから参照されるMD等 = 第1階層
  - そのMDが参照する別のファイル = 第2階層
  - ... 推移閉包
- 全単射 = 全ファイルがジャーナルから到達可能か (全射)
         + 参照は全て実在するか (単射的=幽霊参照ゼロ)

加えて、READMEからの参照も考慮 (READMEは事実上のエントリポイント)。
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, deque

REPO = Path("/home/claude/pianica-organ")

FILE_EXTS = {".md", ".svg", ".png", ".jpg", ".jpeg", ".docx", ".html", ".json", ".py"}
TEXT_EXTS = {".md", ".html", ".svg", ".json", ".py"}  # 中身を読んで参照抽出するもの

REF_PATTERNS = [
    re.compile(r'\[[^\]]*\]\(([^)]+\.(?:md|svg|png|jpg|jpeg|docx|html|json|py))\)', re.IGNORECASE),
    re.compile(r'!\[[^\]]*\]\(([^)]+\.(?:md|svg|png|jpg|jpeg))\)', re.IGNORECASE),
    re.compile(r'`([^`\s]+\.(?:md|svg|png|jpg|jpeg|docx|html|json|py))`', re.IGNORECASE),
    re.compile(r'(?:^|\s|"|\')((?:\.\./)*[\w\-./]+/[\w\-/.]+\.(?:md|svg|png|jpg|jpeg|docx|html|json|py))', re.IGNORECASE | re.MULTILINE),
    re.compile(r'(?:^|\s|"|\')([\w\-]+\.(?:md|svg|png|jpg|jpeg|docx|html|json|py))(?:\s|$|"|\'|\.|,|;|:|\)|\])', re.IGNORECASE | re.MULTILINE),
]

def collect_all_files():
    all_files = set()
    journals = set()
    readmes = set()
    basename_to_paths = defaultdict(set)
    for path in REPO.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_file() and path.suffix.lower() in FILE_EXTS:
            rel = str(path.relative_to(REPO))
            all_files.add(rel)
            basename_to_paths[path.name].add(rel)
            if "journals/" in rel:
                journals.add(rel)
            if path.name == "README.md":
                readmes.add(rel)
    return all_files, journals, readmes, basename_to_paths

def resolve_ref(raw_ref, source_path, all_files, basename_to_paths):
    raw_ref = raw_ref.strip().strip('"').strip("'")
    if raw_ref.startswith("http://") or raw_ref.startswith("https://"):
        return None, "url"
    if raw_ref.startswith("/"):
        return None, "absolute"
    
    source_dir = (REPO / source_path).parent
    
    # 試行1: そのまま
    if raw_ref in all_files:
        return raw_ref, "exact_root"
    
    # 試行2: 相対パス解決
    try:
        rel = (source_dir / raw_ref).resolve().relative_to(REPO)
        if str(rel) in all_files:
            return str(rel), "relative"
    except (ValueError, OSError):
        pass
    
    # 試行3: basename
    basename = Path(raw_ref).name
    if basename in basename_to_paths:
        cands = list(basename_to_paths[basename])
        if len(cands) == 1:
            return cands[0], "basename_unique"
        # 同一ディレクトリ優先
        try:
            same_dir_str = str((REPO / source_path).parent.relative_to(REPO))
            same_dir = [c for c in cands if str(Path(c).parent) == same_dir_str]
            if same_dir:
                return same_dir[0], "basename_same_dir"
        except ValueError:
            pass
        return cands[0], f"basename_multiple({len(cands)})"
    
    return None, "ghost"

def extract_refs(file_path, all_files, basename_to_paths):
    """参照抽出 (拡張子により分岐)"""
    p = REPO / file_path
    if p.suffix.lower() not in TEXT_EXTS:
        return {}
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {}
    
    raw_refs = set()
    for pattern in REF_PATTERNS:
        for m in pattern.findall(text):
            raw_refs.add(m)
    
    self_basename = Path(file_path).name
    raw_refs = {r for r in raw_refs if Path(r).name != self_basename}
    
    resolved = {}
    for r in raw_refs:
        res, method = resolve_ref(r, file_path, all_files, basename_to_paths)
        resolved[r] = (res, method)
    return resolved

def transitive_closure(seeds, all_files, basename_to_paths):
    """シード集合から推移的に到達可能な全ファイルを取得"""
    visited = set(seeds)
    queue = deque(seeds)
    edges = defaultdict(set)  # source -> targets
    ghost_per_source = defaultdict(list)
    method_counts = defaultdict(int)
    
    while queue:
        current = queue.popleft()
        refs = extract_refs(current, all_files, basename_to_paths)
        for raw, (resolved, method) in refs.items():
            method_counts[method] += 1
            if resolved is None:
                ghost_per_source[current].append(raw)
                continue
            edges[current].add(resolved)
            if resolved not in visited:
                visited.add(resolved)
                queue.append(resolved)
    
    return visited, edges, ghost_per_source, method_counts

def main():
    all_files, journals, readmes, basename_to_paths = collect_all_files()
    non_journal_files = all_files - journals
    
    print(f"=== ファイル統計 (v3 推移閉包) ===")
    print(f"全対象ファイル: {len(all_files)}")
    print(f"  - ジャーナル: {len(journals)}")
    print(f"  - README   : {len(readmes)}")
    print(f"  - その他   : {len(all_files - journals - readmes)}")
    print()
    
    # ====================
    # 起点1: ジャーナルのみ
    # ====================
    reachable_from_journals, edges_j, ghost_j, methods_j = transitive_closure(
        journals, all_files, basename_to_paths
    )
    
    # ====================
    # 起点2: ジャーナル + README
    # ====================
    seeds_v2 = journals | readmes
    reachable_from_journals_readme, edges_jr, ghost_jr, methods_jr = transitive_closure(
        seeds_v2, all_files, basename_to_paths
    )
    
    # ====================
    # 結果
    # ====================
    print("=== 結果1: ジャーナル起点の推移閉包 ===")
    print(f"到達可能ファイル: {len(reachable_from_journals)} / {len(all_files)}")
    print(f"未到達(孤児)    : {len(all_files - reachable_from_journals)}")
    print(f"幽霊参照(全件)  : {sum(len(g) for g in ghost_j.values())}")
    print(f"幽霊参照(ユニーク): {len({r for gs in ghost_j.values() for r in gs})}")
    print()
    
    print("=== 結果2: ジャーナル+README起点の推移閉包 ===")
    print(f"到達可能ファイル: {len(reachable_from_journals_readme)} / {len(all_files)}")
    print(f"未到達(孤児)    : {len(all_files - reachable_from_journals_readme)}")
    print(f"幽霊参照(全件)  : {sum(len(g) for g in ghost_jr.values())}")
    print()
    
    # 真の孤児 (どこからも到達不能)
    final_orphans = sorted(all_files - reachable_from_journals_readme)
    
    print(f"=== 真の孤児ファイル ({len(final_orphans)}件) ===")
    orphan_by_dir = defaultdict(list)
    for f in final_orphans:
        orphan_by_dir[str(Path(f).parent)].append(Path(f).name)
    for d, fs in sorted(orphan_by_dir.items(), key=lambda x: -len(x[1])):
        print(f"  {d}: {len(fs)}件")
    print()
    
    # 全幽霊参照
    all_ghost_refs = set()
    for src, refs in ghost_jr.items():
        for r in refs:
            all_ghost_refs.add((src, r))
    
    print(f"=== 全幽霊参照詳細 ({len({r for _, r in all_ghost_refs})}件) ===")
    ghost_target_to_sources = defaultdict(list)
    for src, target in all_ghost_refs:
        ghost_target_to_sources[target].append(src)
    for target, sources in sorted(ghost_target_to_sources.items()):
        if len(target) <= 60:
            print(f"  {target}")
            for s in sorted(set(sources))[:3]:
                print(f"    <- {s}")
    print()
    
    # 結果保存
    result = {
        "summary": {
            "total_files": len(all_files),
            "journals": len(journals),
            "readmes": len(readmes),
            "reachable_from_journals_only": len(reachable_from_journals),
            "reachable_from_journals_and_readme": len(reachable_from_journals_readme),
            "true_orphans": len(final_orphans),
            "ghost_refs_unique": len({r for _, r in all_ghost_refs}),
        },
        "true_orphans": final_orphans,
        "true_orphans_by_dir": {d: sorted(fs) for d, fs in orphan_by_dir.items()},
        "ghost_refs": {target: sorted(set(sources)) for target, sources in sorted(ghost_target_to_sources.items())},
        "edges_count": {src: len(targets) for src, targets in sorted(edges_jr.items())},
        "resolution_methods_v3": dict(methods_jr),
    }
    
    out = REPO / "bijection_verification_v3.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"=> 詳細結果: {out}")
    
    return result

if __name__ == "__main__":
    main()
