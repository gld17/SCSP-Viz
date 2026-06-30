# IMPL Summary

## Changes Made
- web/index.html:816 — Replaced `Spaceborne Computing Simulation<br/>Platform（天基计算仿真平台）` with `SCSP-Viz`
- README.md:62 — Replaced `SCSP simulation platform` with `SCSP-Viz`

## Verification
- `grep -n "天基计算仿真平台" web/index.html` → (no output) ✓
- `grep -n "SCSP simulation platform" README.md` → only line 3 shows (line 62 removed) ✓

## Files Modified
- web/index.html
- README.md
