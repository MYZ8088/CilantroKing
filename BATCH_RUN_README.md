# 批量运行指南

## 快速开始

### 1. 重置进度（可选）
如果需要从头开始运行：
```bash
python reset_progress.py
```
或手动删除 `batch_progress.json` 文件

### 2. 清空数据库（可选）
如果需要重新开始，手动删除 `results.db` 文件。

### 3. 运行批量测试
```bash
python batch_run_advanced.py
```

### 4. 查看结果
```bash
python view_batch_results.py
```

## 测试规格

- **总案例数**: 128 个
- **参数范围**: 
  - m = 45 (固定)
  - n = 7-14
  - k = 6 (固定)
  - s = 3-7
  - j = s 到 k
  - t = 1 和 4 (t=4 仅当 C(j,s)>=4)
- **时间预算**: 120秒/案例
- **预计总时间**: 最多 4.3 小时（实际会更短）

## 进度跟踪

- 进度自动保存到 `batch_progress.json`
- 可以随时中断（Ctrl+C）
- 重新运行会自动继续未完成的案例
- **重置进度**: 运行 `python reset_progress.py` 或删除 `batch_progress.json`
- 完成后可以删除进度文件

## 案例格式

案例 ID 格式: `m-n-k-j-s-run-groups (at least t)`

示例:
- `45-8-6-5-4-1-12 (at least 1)` (第1次运行，12个组)
- `45-8-6-5-4-1-15 (at least 4)` (第1次运行，15个组)
- `45-14-6-6-3-2-8 (at least 1)` (第2次运行，8个组)

## 详细规格

查看 `BATCH_RUN_FINAL_SPEC.md` 了解完整的技术规格和案例分布。
