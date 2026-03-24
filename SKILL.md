---
name: deep-learn-x-api-search
description: 通过对话查询学深求索。用于 SZPU 网关 searchLogin/searchScore 接口调用、加密参数生成与结果整理输出。
---

# 🎓 Deep Learn X API Search 技能

对接 SZPU 网关的 `searchLogin` 与 `searchScore` 接口。

## 图标配置

> 说明：当前技能元数据没有官方 `icon` 字段。推荐用“标题 emoji + 可选本地图标文件”的方式实现视觉图标。

- 对话内图标：本技能统一使用 `🎓` 作为标题前缀与关键结果标识。
- 本地图标文件（可选）：在技能目录放置 `icon.png`（建议 `128x128` 或 `256x256`），用于团队约定或文档展示。
- 命名建议：
  - `deep-learn-x-api-search/icon.png`
  - `deep-learn-x-api-search/preview.md`（可放图标预览与说明）

## 对话输出规范（美化版）

执行本技能时，默认按以下结构输出，保证整齐、可扫描：

1. **结果标题行**：`🎓 学深求索结果`
2. **请求信息块**：接口、账号、时间、状态
3. **核心结果块**：成功/失败、关键信息、必要字段
4. **明细表格块**：成绩明细或错误详情
5. **下一步建议块**：可执行命令或排查建议

### 平均绩点（加权平均分）计算规则

- 定义：`平均绩点 = Σ(学分 × 分数) / Σ(学分)`
- 计算范围：默认使用当前返回的全部课程；若课程无学分或无分数，则跳过该课程并在结果中注明。
- 展示格式：保留两位小数，例如 `87.43`。

### 固定输出模板

```markdown
🎓 学深求索结果

## 请求信息
- 接口: <searchLogin|searchScore>
- 账号: <username>
- 时间: <YYYY-MM-DD HH:mm:ss>
- 状态: <成功|失败>

## 核心结果
- 说明: <一句话总结>
- 关键字段:
  - <字段1>: <值1>
  - <字段2>: <值2>
  - 平均绩点(加权): <weighted_avg_score>

## 明细
| 科目 | 成绩 | 学分 | 学期 |
|------|------|------|------|
| <subject> | <score> | <credit> | <term> |

## 下一步
- <建议1>
- <建议2>
```

### 错误输出模板

```markdown
🎓 学深求索结果

## 请求信息
- 接口: <searchLogin|searchScore>
- 账号: <username>
- 状态: 失败

## 错误说明
- 错误类型: <网络错误|鉴权失败|参数错误|网关限流>
- 错误信息: <message>

## 排查建议
1. 检查 `key` 是否正确且权限包含目标接口。
2. 确认账号密码正确，并先执行 `searchLogin`。
3. 30 秒后重试，避免触发限流。
```

## 快速上手

### 使用脚本（推荐）

依赖：`pip install pycryptodome`

```bash
# 登录
python scripts/aes_request.py login \
  --key <your_key_value> \
  --username <学号> \
  --password <密码>

# 查成绩（需先登录成功）
python scripts/aes_request.py score \
  --key <your_key_value> \
  --username <学号> \
  --password <密码>
```

脚本自动完成：生成 16 位随机 `content`（数字+英文，AES-128 密钥）→ 明文 JSON 构造 → AES-CBC 加密 → URL 编码 → GET 请求 → 打印响应。无需用户提供 `aes_key`。

### 手动加密流程

1. 构造明文 JSON（结构见 `references/api.md`）
2. AES-CBC + PKCS7 加密，IV = `wn0ZfU4qmbhHE1lo`，密钥 = `content`（16 字符随机数字+英文，与请求里 `content` 查询参数一致）
3. Base64 编码 → URL 编码 → 作为 `data` 参数
4. GET/POST 提交 `data` + `content`

## 接口速查

| 接口 | 路径 | 所需权限 |
|------|------|---------|
| searchLogin | `/api/searchLogin` | `search-login` |
| searchScore | `/api/searchScore` | `search-score` |

> searchScore 需先 searchLogin 成功，且使用同一组账号密码。

## 输出示例（成绩查询）

```markdown
🎓 学深求索结果

## 请求信息
- 接口: searchScore
- 账号: 2023xxxxxx
- 时间: 2026-03-24 15:22:09
- 状态: 成功

## 核心结果
- 说明: 本学期共返回 6 门课程成绩。
- 关键字段:
  - 学年学期: 2025-2026-1
  - 通过门数: 6
  - 平均绩点(加权): 90.50

## 明细
| 科目 | 成绩 | 学分 | 学期 |
|------|------|------|------|
| 高等数学 | 92 | 5.0 | 2025-2026-1 |
| 大学英语 | 88 | 3.0 | 2025-2026-1 |

## 下一步
- 如需导出，可将明细复制为 CSV。
- 如需历史成绩，请切换学年学期后重试。
```

## 详细文档

完整加密约定、明文结构、限流说明见 [`references/api.md`](references/api.md)。
