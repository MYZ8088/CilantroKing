# 快速开始指南

## 重新开始批量运行

### 方法 1: 使用重置脚本（推荐）
```bash
python reset_progress.py
```
然后运行批量测试：
```bash
python batch_run_advanced.py
```

### 方法 2: 手动删除
删除 `batch_progress.json` 文件，然后运行：
```bash
python batch_run_advanced.py
```

## 继续未完成的运行

直接运行（会自动从上次中断的地方继续）：
```bash
python batch_run_advanced.py
```

## 查看结果

```bash
python view_batch_results.py
```

## 文件说明

- `batch_progress.json` - 进度跟踪文件
  - 删除此文件 = 重新开始
  - 保留此文件 = 继续运行
  
- `results.db` - 结果数据库
  - 存储所有运行结果
  - 删除此文件 = 清空所有结果

## 常见操作

| 操作 | 命令 |
|------|------|
| 从头开始 | `python reset_progress.py` |
| 继续运行 | `python batch_run_advanced.py` |
| 查看结果 | `python view_batch_results.py` |
| 清空数据库 | 手动删除 `results.db` |
| 清空进度 | 手动删除 `batch_progress.json` |

## 测试信息

- **总案例数**: 128
- **每案例时间**: 最多 120 秒
- **预计总时间**: 最多 4.3 小时（实际会更短）
- **参数**: m=45, n=7-14, k=6, t=1和4
