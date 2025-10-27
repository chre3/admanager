# MCP Ad Manager Ultimate Server

<div align="center">

**🚀 Powerful Ad Manager MCP Server | 强大的Ad Manager MCP服务器**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/chre3/admanager)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![Test Coverage](https://img.shields.io/badge/test%20coverage-100%25-brightgreen.svg)](https://github.com/chre3/admanager)

**📖 Documentation | 文档**
- [English Documentation](README_EN.md) | [中文文档](README_CN.md)

</div>

---

## 🎯 Core Tools

| Tool | Function | Status |
|------|----------|--------|
| `manage_networks` | 🌐 Network Management (2 functions) | ✅ 100% |
| `manage_inventory` | 📦 Inventory Management (3 functions) | ✅ 100% |
| `manage_orders` | 📋 Order Management (3 functions) | ✅ 100% |
| `manage_line_items` | 📈 Line Item Management (3 functions) | ✅ 100% |
| `manage_creatives` | 🎨 Creative Management (2 functions) | ✅ 100% |
| `generate_report` | 📊 Report Generation (5 report types) | ✅ 100% |
| `get_help` | ❓ Help Information | ✅ 100% |

## 📋 Feature Overview

### 🌐 Network Management
- ✅ Get current network information
- ✅ List all networks

### 📦 Inventory Management
- ✅ List all ad units
- ✅ Get ad unit details
- ✅ Create new ad units

### 📋 Order Management
- ✅ List all orders
- ✅ Get order details
- ✅ Create new orders

### 📈 Line Item Management
- ✅ List all line items
- ✅ Get line item details
- ✅ Create new line items

### 🎨 Creative Management
- ✅ List all creatives
- ✅ Get creative details

### 📊 Report Generation
- ✅ Inventory reports
- ✅ Order reports
- ✅ Line item reports
- ✅ Creative reports
- ✅ Ad server reports

## ⚡ Quick Start

```bash
# Install
pip install -r requirements.txt

# Install Ad Manager SDK
pip install google-ads-admanager

# Authenticate with gcloud
gcloud auth application-default login

# Run
python -m mcp_admanager_ultimate.server
```

## 🎯 Key Benefits

- ✅ **Complete Coverage**: All Ad Manager API core functions
- ✅ **Smart Validation**: Auto parameter validation & error handling
- ✅ **AI Optimized**: Clear parameters & intelligent error handling
- ✅ **Flexible Queries**: Support for multi-dimensional queries
- ✅ **Full CRUD**: Complete create, read operations

## 📋 Requirements

- Python 3.8+
- Google Ad Manager API v202405
- Google Auth Library
- google-ads-admanager SDK

## 📊 Report Types

### Available Report Types
- `inventory` - Inventory performance reports
- `order` - Order performance reports
- `line_item` - Line item performance reports
- `creative` - Creative performance reports
- `ad_server` - Ad server reports

### Supported Metrics
- `AD_SERVER_IMPRESSIONS` - Ad server impressions
- `AD_SERVER_CLICKS` - Ad server clicks
- `AD_SERVER_CTR` - Click-through rate
- `AD_SERVER_CPM` - Cost per thousand impressions
- `AD_SERVER_CPC` - Cost per click

### Supported Dimensions
- `AD_UNIT_NAME` - Ad unit name
- `ORDER_NAME` - Order name
- `LINE_ITEM_NAME` - Line item name
- `CREATIVE_NAME` - Creative name
- `DATE` - Date dimension

---

<div align="center">

**Made with ❤️ for AI-powered Ad Manager management**

[View Full Documentation](README_EN.md) | [查看完整文档](README_CN.md)

</div>
