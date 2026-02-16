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

- [ ] Run `SPEC_IMPLEMENTATION_MATRIX.md` — count PASS / PARTIAL / FAIL
- [ ] **README compliance badge matches matrix summary**
  - README line: `| **SPEC Compliance** | XX PASS · Y PARTIAL · Z FAIL |`
  - Matrix summary section: verify numbers match
- [ ] No ❌ FAIL items in matrix

## 3. Documentation Consistency

- [ ] README project structure matches actual files (`ls logger/tools/`)
- [ ] API.md topic examples match SPEC
- [ ] All doc links resolve (no 404 within repo)
- [ ] Scripts in `scripts/` match README usage examples

## 4. Code Quality

- [ ] No Python syntax errors: `python -m py_compile logger/tools/*.py`
- [ ] PowerShell script accepted: `powershell -ExecutionPolicy Bypass -File .\scripts\run_all.ps1 -WhatIf` (dry-run)
- [ ] No hardcoded credentials in code (use pwfile / env)

## 5. Final Packaging

- [ ] Git status clean: `git status --short` → no uncommitted changes
- [ ] All changes pushed: `git log --oneline -5`
- [ ] Results folder `.gitignore`d (not tracked)

---

> **Tip:** Chạy pipeline với intersection khác để verify multi-intersection:
>
> ```powershell
> .\scripts\run_all.ps1 -City demo -Intersection 002 -BenchCount 5
> ```
