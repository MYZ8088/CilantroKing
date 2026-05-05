# 批量运行指南 (n=15 到 25)

## 快速开始

### 1. 重置进度（可选）
如果需要从头开始运行：
```bash
python reset_progress_n15_to_n25.py
```
或手动删除 `batch_progress_n15_to_n25.json` 文件

### 2. 运行批量测试
```bash
python batch_run_n15_to_n25.py
```

### 3. 查看结果
```bash
python view_batch_results.py
```

## 测试规格

- **总案例数**: 176 个
- **参数范围**: 
  - m = 45 (固定)
  - n = 15-25 (11 个值)
  - k = 6 (固定)
  - s = 3-7
  - j = s 到 k
  - t = 1 和 4 (t=4 仅当 C(j,s)>=4)
- **时间预算**: 120秒/案例
- **预计总时间**: 最多 5.9 小时（实际会更短）

## 进度跟踪

- 进度自动保存到 `batch_progress_n15_to_n25.json`
- 可以随时中断（Ctrl+C）
- 重新运行会自动继续未完成的案例
- **重置进度**: 运行 `python reset_progress_n15_to_n25.py` 或删除进度文件
- 完成后可以删除进度文件

## 案例格式

案例 ID 格式: `m-n-k-j-s-run-groups (at least t)`

示例:
- `45-15-6-5-4-1-12 (at least 1)` (第1次运行，12个组)
- `45-15-6-5-4-1-15 (at least 4)` (第1次运行，15个组)
- `45-25-6-6-3-2-8 (at least 1)` (第2次运行，8个组)

## 每个 n 的案例数

每个 n 值有 16 个案例：
- s=3: 7 个案例 (j=3,4,5,6 with t=1 and t=4 where valid)
- s=4: 5 个案例 (j=4,5,6 with t=1 and t=4 where valid)
- s=5: 3 个案例 (j=5,6 with t=1 and t=4 where valid)
- s=6: 1 个案例 (j=6 with t=1)

总计: 11 个 n 值 × 16 案例 = 176 案例

## 注意事项

1. **数据库共享**: 使用相同的 `results.db` 数据库
2. **进度独立**: 使用独立的进度文件 `batch_progress_n15_to_n25.json`
3. **可并行运行**: 可以与 n=7-14 的批量运行同时进行（如果资源充足）
4. **时间预算**: 每个案例固定 120 秒，但算法会尽早停止

## 详细规格

查看 `BATCH_RUN_FINAL_SPEC.md` 了解完整的技术规格和案例分布。
