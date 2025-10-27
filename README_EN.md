# MCP Ad Manager Ultimate

The most powerful Google Ad Manager MCP (Model Context Protocol) server with complete ad management functionality.

## Features

- 🎯 Complete Ad Manager API functionality support
- 🚀 Optimized tool structure to reduce redundant calls
- 🔐 Support for Application Default Credentials authentication (via gcloud)
- 📊 Reporting & Analytics: Inventory reports, performance data, revenue analysis
- ⚙️ Configuration Management: Ad units, orders, line items
- 💰 Account Management: Network information, order management
- 📈 Intelligent parameter validation and error handling
- 🎯 AI LLM-friendly with clear parameter descriptions

## Functional Modules

### 1. Network Management (manage_networks)
- Get current network information
- List all networks

### 2. Inventory Management (manage_inventory)
- List ad units
- Get ad unit details
- Create new ad units

### 3. Order Management (manage_orders)
- List all orders
- Get order details
- Create new orders

### 4. Line Item Management (manage_line_items)
- List all line items
- Get line item details
- Create new line items

### 5. Creative Management (manage_creatives)
- List all creatives
- Get creative details

### 6. Report Generation (generate_report)
- Inventory reports
- Order reports
- Line item reports
- Creative reports
- Ad server reports

## Installation

### 1. Install Dependencies

```bash
cd admanager
pip install -r requirements.txt
```

Or install using setup.py:

```bash
pip install -e .
```

### 2. Install Google Ad Manager SDK

You need to install the Google Ad Manager Python SDK. There are two options:

**Option 1: google-ads-admanager (Recommended)**
```bash
pip install google-ads-admanager
```

**Option 2: googleads (Legacy)**
```bash
pip install googleads
```


## Usage

### Run MCP Server

```bash
python -m mcp_admanager_ultimate.server
```

Or use the command-line entry point:

```bash
mcp-admanager-ultimate
```

### Configure in MCP Client

Add to your MCP client configuration file:

```json
{
  "mcpServers": {
    "admanager": {
      "command": "python",
      "args": ["-m", "mcp_admanager_ultimate.server"],
      "env": {
        "GOOGLE_ADMANAGER_NETWORK_CODE": "your_network_code"
      }
    }
  }
}
```

## Tool Usage Examples

### 1. Get Current Network Information

```json
{
  "name": "manage_networks",
  "arguments": {
    "action": "get_current"
  }
}
```

### 2. List All Ad Units

```json
{
  "name": "manage_inventory",
  "arguments": {
    "action": "list"
  }
}
```

### 3. List Line Items for a Specific Order

```json
{
  "name": "manage_line_items",
  "arguments": {
    "action": "list",
    "order_id": "123456"
  }
}
```

### 4. Generate Inventory Report

```json
{
  "name": "generate_report",
  "arguments": {
    "report_type": "inventory",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  }
}
```

## API Version

Currently using Google Ad Manager API v202405 (latest version)

## Documentation References

- [Google Ad Manager API Official Documentation](https://developers.google.com/ad-manager/api/start)
- [google-ads-admanager PyPI](https://pypi.org/project/google-ads-admanager/)

## License

MIT License

## Author

chre3 - chremata3@gmail.com

## Version History

- v1.0.0 - Initial version with complete functionality support

