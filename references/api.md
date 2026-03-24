# SZPU API 接口参考

## baseUrl

```
https://api.cloudslow.com/szpu
```

## 加密约定

| 参数 | 值 |
|------|----|
| 算法 | AES-CBC |
| 填充 | PKCS7 |
| IV | `wn0ZfU4qmbhHE1lo`（固定，16字节） |
| 密钥长度 | 128 bit（16字节） |
| `content` 参数 | AES 密钥明文（调用方提供，如 `rsPlAWqcS3yOz9wP`） |
| `data` 参数 | 明文 JSON 经 AES-CBC 加密后的 Base64 字符串，再做 URL 编码 |

**加密流程：**
1. 构造明文 JSON（见各接口说明）
2. `AES.encrypt(plaintext, key, IV)` → Base64 → URL 编码 → `data` 参数
3. `content` = AES 密钥明文（URL 编码后传入）

---

## /api/searchLogin

**路径：** `https://api.cloudslow.com/szpu/api/searchLogin`  
**传参：** GET 查询参数 或 POST 表单（参数需 URL 编码）  
**权限：** `search-login`

### 明文 JSON 结构

```json
{
  "key": "<your_key_value>",
  "data": {
    "username": "学号",
    "password": "密码"
  }
}
```

### 示例请求

```
GET https://api.cloudslow.com/szpu/api/searchLogin?data=<密文>&content=<密钥>
```

---

## /api/searchScore

**路径：** `https://api.cloudslow.com/szpu/api/searchScore`  
**传参：** GET 查询参数 或 POST 表单（参数需 URL 编码）  
**权限：** `search-score`  
**前置：** 须先调用 `searchLogin` 成功，且使用同一组 username/password

### 明文 JSON 结构

```json
{
  "key": "<your_key_value>",
  "data": {
    "username": "学号",
    "password": "密码"
  }
}
```

### 示例请求

```
GET https://api.cloudslow.com/szpu/api/searchScore?data=<密文>&content=<密钥>
```

---

## ApiKey 限流说明

- 小时 / 天 / 月 / 年 / 总次数均可配置，值为 0 表示该维度不限
- 超限返回错误码，以服务端 `RestResult` 为准

## 安全注意

- 勿泄露真实 `key_value` 与账号密码
- 文档中的示例密钥（`WS2HAsx5XkiopoU08Aa8nqZz72y9kiOe`、`rsPlAWqcS3yOz9wP`）仅为格式参考
