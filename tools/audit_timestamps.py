#!/usr/bin/env python3
import json, os, re, csv, sys
from typing import List, Tuple, Optional

# ----------------------------
# Config (can be overridden by CLI args)
COURSE_JSON_PATH = "src/content/course.json"
OUTPUT_DIR = "audits"
CSV_PATH = os.path.join(OUTPUT_DIR, "course_timestamp_audit.csv")
JSON_PATH = os.path.join(OUTPUT_DIR, "course_timestamp_audit.json")

MAX_GAP_S = 900     # 15 minutes
MIN_SEP_S = 8       # seconds
LABEL_WORDS_MIN = 2
LABEL_WORDS_MAX = 5
DESC_WORDS_MIN = 5
DESC_WORDS_MAX = 15
# ----------------------------

TIME_RE = re.compile(r"^(?:(\d+):)?([0-5]?\d):([0-5]\d)$")  # H:MM:SS or M:SS also matches as H optional
GENERIC_LABELS = {"overview", "discussion", "recap", "intro", "general"}

def to_seconds(hmmss: str) -> Optional[int]:
    """Parse H:MM:SS strictly. Return seconds or None if bad format."""
    m = TIME_RE.match(hmmss.strip())
    if not m: return None
    h = int(m.group(1) or 0)
    mm = int(m.group(2))
    ss = int(m.group(3))
    # Enforce H:MM:SS form; treat single-part M:SS as 0:MM:SS by callers if desired
    return h*3600 + mm*60 + ss

def is_h_mm_ss(s: str) -> bool:
    return TIME_RE.match(s.strip()) is not None

def words(s: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9_]+", s.lower())

def word_count(s: str) -> int:
    return len(words(s))

def jget(obj, path: List):
    cur = obj
    for p in path:
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            return None
    return cur

def severity_from_flags(has_range, has_order, has_coverage, has_density, has_labelweak, has_descweak):
    if has_range or has_order:
        return "Critical"
    if has_coverage or has_density:
        return "High"
    if has_labelweak or has_descweak:
        return "Medium"
    return "Low"

def main():
    # CLI overrides
    import argparse
    ap = argparse.ArgumentParser(description="Audit course timestamps and summaries.")
    ap.add_argument("--course", default=COURSE_JSON_PATH)
    ap.add_argument("--outdir", default=OUTPUT_DIR)
    ap.add_argument("--max_gap_s", type=int, default=MAX_GAP_S)
    ap.add_argument("--min_sep_s", type=int, default=MIN_SEP_S)
    ap.add_argument("--label_min", type=int, default=LABEL_WORDS_MIN)
    ap.add_argument("--label_max", type=int, default=LABEL_WORDS_MAX)
    ap.add_argument("--desc_min", type=int, default=DESC_WORDS_MIN)
    ap.add_argument("--desc_max", type=int, default=DESC_WORDS_MAX)
    args = ap.parse_args()

    course_path = args.course
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    with open(course_path, "r", encoding="utf-8") as f:
        course = json.load(f)

    rows = []
    json_report = {
        "status": "ok",
        "config": {
            "course_json_path": course_path,
            "max_gap_s": args.max_gap_s,
            "min_sep_s": args.min_sep_s,
            "label_words": [args.label_min, args.label_max],
            "desc_words": [args.desc_min, args.desc_max],
        },
        "summary": {"weeks": 0, "lessons": 0, "issues_total": 0},
        "lessons": []
    }

    weeks = course.get("weeks", [])
    json_report["summary"]["weeks"] = len(weeks)

    # CSV header
    header = ["Week","Lesson ID","Title","Duration Clean?","Out-of-Range Timestamps",
              "Order OK?","Coverage OK?","Density OK?","Label Quality","Description Quality",
              "Severity","Example Problem","Actions"]

    for w in weeks:
        week_id = w.get("id","")
        lessons = w.get("lessons",[])
        for lesson in lessons:
            json_report["summary"]["lessons"] += 1
            lesson_id = lesson.get("id","")
            title = lesson.get("title","")
            duration_str = lesson.get("duration","") or ""
            timestamps = lesson.get("timestamps",[])

            # Duration check (strict H:MM:SS, no extra text)
            duration_ok = bool(duration_str) and is_h_mm_ss(duration_str.strip())
            duration_s = to_seconds(duration_str.strip()) if duration_ok else None

            # Prepare analyses
            times_s = []
            bad_format = []
            for t in timestamps:
                ts = (t.get("time") or "").strip()
                if not is_h_mm_ss(ts):
                    bad_format.append(ts)
                    continue
                times_s.append(to_seconds(ts))

            out_of_range = []
            non_monotonic = []
            too_dense = []
            coverage_gaps = []

            # Range check
            if duration_s is not None:
                for i, s_val in enumerate(times_s):
                    if s_val is None or s_val < 0 or s_val > duration_s:
                        out_of_range.append(timestamps[i].get("time",""))

            # Order check (monotonic non-decreasing)
            prev = -1
            for i, s_val in enumerate(times_s):
                if s_val is None:
                    continue
                if s_val < prev:
                    non_monotonic.append(timestamps[i].get("time",""))
                prev = max(prev, s_val)

            # Density check
            for i in range(1, len(times_s)):
                a, b = times_s[i-1], times_s[i]
                if a is None or b is None: 
                    continue
                if (b - a) < args.min_sep_s:
                    too_dense.append(f"{timestamps[i-1].get('time','')}→{timestamps[i].get('time','')}")

            # Coverage check (find max gap)
            coverage_ok = True
            if duration_s is not None and len(times_s) >= 2:
                for i in range(1, len(times_s)):
                    gap = times_s[i] - times_s[i-1]
                    if gap > args.max_gap_s:
                        coverage_ok = False
                        coverage_gaps.append({
                            "start": timestamps[i-1].get("time",""),
                            "end": timestamps[i].get("time",""),
                            "length_s": gap
                        })

            # Label/description heuristics
            vague_labels = []
            weak_descriptions = []
            for t in timestamps:
                label = (t.get("label") or "").strip()
                desc = (t.get("description") or "").strip()
                # Label
                lw = word_count(label)
                tokens = set(words(label))
                is_generic = any(g in tokens for g in GENERIC_LABELS)
                if lw < args.label_min or lw > args.label_max or is_generic:
                    vague_labels.append(t.get("time",""))
                # Description
                dw = word_count(desc)
                # overlap ratio
                ltoks = set(words(label))
                dtoks = set(words(desc))
                overlap = (len(ltoks & dtoks) / max(1, len(dtoks))) if dtoks else 0.0
                if dw < args.desc_min or dw > args.desc_max or overlap >= 0.7:
                    weak_descriptions.append(t.get("time",""))

            label_quality_ok = (len(vague_labels) == 0)
            desc_quality_ok = (len(weak_descriptions) == 0)

            # Summarize booleans
            duration_clean = "OK" if duration_ok else "Needs fix"
            range_bad = len(out_of_range) > 0
            order_ok = "OK" if len(non_monotonic) == 0 else "Broken"
            density_ok = "OK" if len(too_dense) == 0 else "Too dense"
            coverage_ok_str = "OK" if coverage_ok else "Gaps"
            label_quality = "OK" if label_quality_ok else "Weak"
            desc_quality = "OK" if desc_quality_ok else "Weak"

            # Severity & actions
            severity = severity_from_flags(range_bad, order_ok=="Broken", not coverage_ok, density_ok!="OK", not label_quality_ok, not desc_quality_ok)
            actions = []
            if not duration_ok: actions.append("fix_duration")
            if range_bad: actions.append("fix_range")
            if order_ok == "Broken": actions.append("fix_order")
            if coverage_ok_str != "OK": actions.append("fix_coverage")
            if density_ok != "OK": actions.append("fix_density")
            if label_quality != "OK" or desc_quality != "OK": actions.append("rewrite_summaries")

            # Example problem
            example = ""
            if bad_format:
                example = f"Bad time format: {bad_format[0]}"
            elif out_of_range:
                example = f"Out of range: {out_of_range[0]}"
            elif non_monotonic:
                example = f"Order broken at: {non_monotonic[0]}"
            elif too_dense:
                example = f"Too dense: {too_dense[0]}"
            elif not label_quality_ok:
                example = f"Vague label at: {vague_labels[0]}"
            elif not desc_quality_ok:
                example = f"Weak description at: {weak_descriptions[0]}"

            # CSV row
            rows.append([
                week_id,
                lesson_id,
                title,
                duration_clean,
                len(out_of_range),
                order_ok,
                coverage_ok_str,
                density_ok,
                label_quality,
                desc_quality,
                severity,
                example,
                ", ".join(actions)
            ])

            # JSON lesson entry
            json_report["lessons"].append({
                "week_id": week_id,
                "lesson_id": lesson_id,
                "title": title,
                "duration_ok": duration_ok,
                "timestamp_issues": {
                    "format": bad_format,
                    "out_of_range": out_of_range,
                    "non_monotonic": non_monotonic,
                    "density": too_dense,
                    "coverage_gaps": coverage_gaps
                },
                "summary_issues": {
                    "vague_labels": vague_labels,
                    "weak_descriptions": weak_descriptions
                },
                "acceptance": {
                    "timestamps_pass": (duration_ok and not range_bad and order_ok=="OK" and coverage_ok_str=="OK" and density_ok=="OK"),
                    "summaries_pass": (label_quality_ok and desc_quality_ok),
                    "overall": "pass" if (duration_ok and not range_bad and order_ok=="OK" and coverage_ok_str=="OK" and density_ok=="OK" and label_quality_ok and desc_quality_ok) else "needs_fixes"
                },
                "actions": actions
            })

    # issues_total
    issues_total = sum(1 for L in json_report["lessons"] if L["acceptance"]["overall"] != "pass")
    json_report["summary"]["issues_total"] = issues_total

    # Write CSV/JSON
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(json_report, f, ensure_ascii=False, indent=2)

    print(f"[OK] Wrote CSV:  {CSV_PATH}")
    print(f"[OK] Wrote JSON: {JSON_PATH}")
    print(f"[OK] Lessons: {json_report['summary']['lessons']}, Issues: {issues_total}")

if __name__ == "__main__":
    main()