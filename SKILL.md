---
name: deep-learn-x-api-search
description: 通过对话查询 SZPU searchLogin/searchScore；AES content 为 16 位随机数字英文串，由工具自动生成
---

# SZPU API Search 技能

对接 SZPU 网关的 `searchLogin` 与 `searchScore` 接口。

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

## 详细文档

完整加密约定、明文结构、限流说明见 [`references/api.md`](references/api.md)。
