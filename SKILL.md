---
name: deep-learn-x
description: 通过对话查询学深求索信息。
---

# 🎓 Deep Learn X API Search 技能

对接 SZPU 网关的 `searchLogin`、`searchScore` 与 `searchTimetable` 接口。

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
4. **明细表格块**：成绩明细、课表明细或错误详情
5. **下一步建议块**：可执行命令或排查建议

### 平均绩点（加权平均分）计算规则

- 定义：`平均绩点 = Σ(学分 × 分数) / Σ(学分)`
- 计算范围：默认使用当前返回的全部课程；若课程无学分或无分数，则跳过该课程并在结果中注明。
- 展示格式：保留两位小数，例如 `87.43`。

### 固定输出模板

```markdown
🎓 学深求索结果

## 请求信息
- 接口: <searchLogin|searchScore|searchTimetable>
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

课表查询场景可将表头改为「课程 / 时间 / 教师 / 教室」等，与接口返回字段对齐。

## 下一步
- <建议1>
- <建议2>
```

### 错误输出模板

```markdown
🎓 学深求索结果

## 请求信息
- 接口: <searchLogin|searchScore|searchTimetable>
- 账号: <username>
- 状态: 失败

## 错误说明
- 错误类型: <网络错误|鉴权失败|参数错误|网关限流>
- 错误信息: <message>

## 排查建议
1. 检查 `key` 是否正确且权限包含目标接口。
2. 确认账号密码正确，并先执行 `searchLogin`（`searchScore` / `searchTimetable` 均需已登录且账号密码与库中记录一致）。
3. 30 秒后重试，避免触发限流。
```

## 快速上手

### 使用脚本（推荐）

依赖：`pip install pycryptodome`

```bash
# 登录
python scripts/aes_request.py login \
  [--key <your_key_value>] \
  --username <学号> \
  --password <密码>

# 查成绩（需先登录成功）
python scripts/aes_request.py score \
  [--key <your_key_value>] \
  --username <学号> \
  --password <密码>

# 查课表（需先登录成功；--term 见下文「课表学期格式」）
python scripts/aes_request.py timetable \
  [--key <your_key_value>] \
  --username <学号> \
  --password <密码> \
  --term 2025-2026-2
```

脚本自动完成：生成 16 位随机 `content`（数字+英文，AES-128 密钥）→ 明文 JSON 构造 → AES-CBC 加密 → URL 编码 → GET 请求 → 打印响应。无需用户提供 `aes_key`。

### API Key（`key`）默认行为

- **默认 key**：当用户**没有主动**表达要自行提供 API key（例如未说「我提供 key」「用我的 key」「换 key」「不要默认 key」等）时，一律使用：`WS2HAsx5XkiopoU08Aa8nqZz72y9kiOe`。无需因缺 key 向用户追问。
- **覆盖**：用户显式给出 `--key <值>` 或在对话中明确指定 key 时，优先使用该值，不使用上述默认。

`key` 使用规则：与上节一致；命令行未传 `--key` 且对话未要求自备 key 时，即采用默认 key。

### 课表学期（`term`）格式

- **形态**：与教务一致，**`起始学年-结束学年-学期序号`**（三段用英文连字符 `-` 连接，一般为纯数字）。
- **示例**：`2025-2026-1`（第一学期）、`2025-2026-2`（第二学期）。
- **用法**：`searchTimetable` 明文 JSON 里的 `term` 与脚本 `--term` 填**同一字符串**；须与教务/云端约定完全一致（勿改连字符、勿多空格）。

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
| searchTimetable | `/api/searchTimetable` | `search-timetable` |

> `searchScore` / `searchTimetable` 均需先 `searchLogin` 成功，且使用同一组账号密码；`searchTimetable` 额外传入 `term`，格式见上文「课表学期（`term`）格式」（例：`2025-2026-2`）。

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
