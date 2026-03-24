---
name: szpu-api-search
description: 深圳职业技术大学（SZPU）网关 API 对接技能，支持 searchLogin（登录绑定）与 searchScore（成绩查询）两个接口。请求需将明文 JSON 经 AES-CBC/PKCS7 加密后作为 data 参数，AES 密钥作为 content 参数提交。baseUrl 为 https://api.cloudslow.com/szpu。触发场景：(1) 调用/对接/调试 searchLogin 或 searchScore 接口；(2) 说「API 搜索登录」「search-login」「执行 searchLogin」；(3) 说「API 查成绩」「search-score」「执行 searchScore」；(4) 需要对 SZPU 网关请求进行 AES 加密或解密。
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
  --password <密码> \
  --content <aes_key>

# 查成绩（需先登录成功）
python scripts/aes_request.py score \
  --key <your_key_value> \
  --username <学号> \
  --password <密码> \
  --content <aes_key>
```

脚本自动完成：明文 JSON 构造 → AES-CBC 加密 → URL 编码 → GET 请求 → 打印响应。

### 手动加密流程

1. 构造明文 JSON（结构见 `references/api.md`）
2. AES-CBC + PKCS7 加密，IV = `wn0ZfU4qmbhHE1lo`，密钥 = `content` 参数（16字节）
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
