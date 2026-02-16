# Release Checks

> Danh sách kiểm tra trước khi nộp / nghiệm thu.
> Chạy theo thứ tự, đánh dấu ✅ khi hoàn tất.

---

## 1. Pipeline Validation

- [ ] Docker services running: `docker compose ps`
- [ ] Full pipeline pass: `.\scripts\run_all.ps1` → exit code 0
- [ ] Smoke test PASS in pipeline log
- [ ] Benchmark PASS in pipeline log
- [ ] Artifacts collected (check `results/run_*/`)

## 2. SPEC Compliance Sync

> Pre-release gate: README SPEC Compliance line must match matrix summary totals (currently 36 PASS · 7 PARTIAL · 0 FAIL).

- [ ] Matrix summary numbers: `Select-String -Path docs/SPEC_IMPLEMENTATION_MATRIX.md -Pattern "TOTAL|Result"`
- [ ] **README compliance badge matches matrix summary**
  - README line: `| **SPEC Compliance** | XX PASS · Y PARTIAL · Z FAIL |`
  - Matrix summary section: verify numbers match
- [ ] No ❌ FAIL items in matrix

## 3. Documentation Consistency

- [ ] README project structure matches actual files (`Get-ChildItem logger/tools/`)
- [ ] API.md topic examples match SPEC
- [ ] All doc links resolve (no 404 within repo)
- [ ] Scripts in `scripts/` match README usage examples

## 4. Code Quality

- [ ] No Python syntax errors: `python -m py_compile logger/tools/*.py`
- [ ] PowerShell syntax OK: `powershell -NoProfile -Command "Get-Command .\scripts\run_all.ps1 | Select-Object Name"` (no parse errors)
- [ ] Quick pipeline sanity: `.\scripts\run_all.ps1 -SkipDocker -BenchCount 3` → exit 0
- [ ] No hardcoded credentials in code (use pwfile / env)

## 5. Final Packaging

- [ ] Git status clean: `git status --short` → no uncommitted changes
- [ ] All changes pushed: `git log --oneline -5`
- [ ] Results artifacts policy: `results/` is runtime-only and must stay untracked (attach reports separately if needed)

---

> **Tip:** Chạy pipeline với intersection khác để verify multi-intersection:
>
> ```powershell
> .\scripts\run_all.ps1 -City demo -Intersection 002 -BenchCount 5
> ```
