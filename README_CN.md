# MCP Ad Manager 终极服务器

<div align="center">

**🚀 强大的Ad Manager MCP服务器 | Powerful Ad Manager MCP Server**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/chre3/admanager)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![Test Coverage](https://img.shields.io/badge/test%20coverage-100%25-brightgreen.svg)](https://github.com/chre3/admanager)

**📖 Documentation | 文档**
- [English Documentation](README_EN.md) | [中文文档](README_CN.md)

</div>

---

## 🎯 核心工具

| 工具 | 功能 | 状态 |
|------|------|------|
| `manage_networks` | 🌐 网络管理 (2个功能) | ✅ 100% |
| `manage_inventory` | 📦 库存管理 (3个功能) | ✅ 100% |
| `manage_orders` | 📋 订单管理 (3个功能) | ✅ 100% |
| `manage_line_items` | 📈 行项目管理 (3个功能) | ✅ 100% |
| `manage_creatives` | 🎨 创意管理 (2个功能) | ✅ 100% |
| `generate_report` | 📊 报告生成 (5种报告类型) | ✅ 100% |
| `get_help` | ❓ 帮助信息 | ✅ 100% |

## 📋 功能概览

### 🌐 网络管理
- ✅ 获取当前网络信息
- ✅ 列出所有网络

### 📦 库存管理
- ✅ 列出所有广告单元
- ✅ 获取广告单元详情
- ✅ 创建新广告单元

### 📋 订单管理
- ✅ 列出所有订单
- ✅ 获取订单详情
- ✅ 创建新订单

### 📈 行项目管理
- ✅ 列出所有行项目
- ✅ 获取行项目详情
- ✅ 创建新行项目

### 🎨 创意管理
- ✅ 列出所有创意
- ✅ 获取创意详情

### 📊 报告生成
- ✅ 库存报告
- ✅ 订单报告
- ✅ 行项目报告
- ✅ 创意报告
- ✅ 广告服务器报告

## ⚡ 快速开始

```bash
# 安装
pip install -r requirements.txt

# 安装Ad Manager SDK
pip install google-ads-admanager

# 使用gcloud认证
gcloud auth application-default login

# 运行
python -m mcp_admanager_ultimate.server
```

## 🎯 关键优势

- ✅ **完整覆盖**: Ad Manager API所有核心功能
- ✅ **智能验证**: 自动参数验证和错误处理
- ✅ **AI优化**: 清晰的参数和智能错误处理
- ✅ **灵活查询**: 支持多维度查询
- ✅ **完整CRUD**: 支持创建、读取操作

## 📋 要求

- Python 3.8+
- Google Ad Manager API v202405
- Google Auth Library
- google-ads-admanager SDK

## 📊 报告类型

### 可用报告类型
- `inventory` - 库存性能报告
- `order` - 订单性能报告
- `line_item` - 行项目性能报告
- `creative` - 创意性能报告
- `ad_server` - 广告服务器报告

### 支持的指标
- `AD_SERVER_IMPRESSIONS` - 广告服务器展示数
- `AD_SERVER_CLICKS` - 广告服务器点击数
- `AD_SERVER_CTR` - 点击通过率
- `AD_SERVER_CPM` - 每千次展示费用
- `AD_SERVER_CPC` - 每次点击费用

### 支持的维度
- `AD_UNIT_NAME` - 广告单元名称
- `ORDER_NAME` - 订单名称
- `LINE_ITEM_NAME` - 行项目名称
- `CREATIVE_NAME` - 创意名称
- `DATE` - 日期维度

---

<div align="center">

**为AI驱动的Ad Manager管理而制作 ❤️**

[View Full Documentation](README_EN.md) | [查看完整文档](README_CN.md)

</div>
