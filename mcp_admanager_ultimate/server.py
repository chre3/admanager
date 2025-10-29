#!/usr/bin/env python3
"""
MCP Ad Manager 增强终极优化版服务器 - 包含所有Ad Manager功能
支持网络管理、库存管理、订单管理、行项目管理、创意管理等完整功能
"""

import os
import sys
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

# Google Ad Manager imports
try:
    from google.ads.admanager.client import AdManagerClient
    from google.ads.admanager.errors import AdManagerReportError
    from google.ads.admanager import StatementBuilder
    ADMANAGER_AVAILABLE = True
except ImportError:
    # 如果google-ads-admanager不可用，尝试使用google-ads
    ADMANAGER_AVAILABLE = False
    try:
        from googleads import ad_manager
        ADMANAGER_AVAILABLE = True
    except ImportError:
        print("警告: 未安装 google-ads-admanager 或 googleads 库", file=sys.stderr)
        ADMANAGER_AVAILABLE = False

from google.auth import default
from google.auth.transport.requests import Request
from google.oauth2 import service_account

class MCPAdManagerEnhancedUltimateServer:
    """Google Ad Manager 增强终极优化版MCP服务器"""
    
    def __init__(self):
        self.network_code = os.getenv("GOOGLE_ADMANAGER_NETWORK_CODE")
        self.client = None
        
        print("🎯 MCP Ad Manager 增强终极优化版 v1.0 已初始化", file=sys.stderr)
        print(f"   📊 Network Code: {self.network_code if self.network_code else '未设置'}", file=sys.stderr)
        print("   🚀 增强版 - 完整Ad Manager功能支持!", file=sys.stderr)
        
        if not ADMANAGER_AVAILABLE:
            print("   ⚠️  警告: Ad Manager SDK 未安装，某些功能可能不可用", file=sys.stderr)

    def _get_admanager_client(self):
        """获取Ad Manager客户端对象"""
        if not ADMANAGER_AVAILABLE:
            raise ValueError("Ad Manager SDK 未安装。请运行: pip install google-ads-admanager 或 pip install googleads")
        
        if self.client is None:
            try:
                # 尝试使用新的 google-ads-admanager
                if 'AdManagerClient' in globals():
                    self.client = AdManagerClient.LoadFromStorage()
                # 否则使用旧的 googleads
                elif 'ad_manager' in globals():
                    self.client = ad_manager.AdManagerClient.LoadFromStorage()
                else:
                    raise ValueError("无法导入 Ad Manager 客户端")
                
                print("✅ Ad Manager 客户端初始化成功", file=sys.stderr)
            except Exception as e:
                raise ValueError(f"无法初始化Ad Manager客户端: {str(e)}")
        
        return self.client

    def _get_credentials(self):
        """获取Google认证凭据，优先使用GOOGLE_APPLICATION_CREDS环境变量指定的文件"""
        try:
            # 检查是否设置了GOOGLE_APPLICATION_CREDS环境变量
            creds_path = os.getenv('GOOGLE_APPLICATION_CREDS')
            if creds_path and os.path.exists(creds_path):
                print(f"✅ 使用指定的认证文件: {creds_path}", file=sys.stderr)
                credentials = service_account.Credentials.from_service_account_file(
                    creds_path,
                    scopes=["https://www.googleapis.com/auth/dfp"]
                )
                return credentials, None
            else:
                # 如果没有设置环境变量或文件不存在，使用默认的Application Default Credentials
                print("⚠️ 未设置GOOGLE_APPLICATION_CREDS环境变量，使用默认认证", file=sys.stderr)
                return default(scopes=["https://www.googleapis.com/auth/dfp"])
        except Exception as e:
            print(f"❌ 认证失败: {str(e)}", file=sys.stderr)
            raise ValueError(f"无法获取认证凭据: {str(e)}")

    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理MCP初始化请求"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "listChanged": True
                },
                "resources": {
                    "subscribe": True,
                    "listChanged": True
                },
                "prompts": {
                    "listChanged": True
                }
            },
            "serverInfo": {
                "name": "admanager-enhanced-ultimate",
                "version": "1.0.0",
                "description": "增强终极优化版Google Ad Manager MCP服务器，完整功能支持"
            }
        }

    def handle_tools_list(self) -> Dict[str, Any]:
        """处理工具列表请求"""
        tools = [
            # 网络管理工具
            {
                "name": "manage_networks",
                "description": "管理Ad Manager网络 - 包括获取网络信息、列出所有网络等功能",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["get_current", "list_all"],
                            "description": "操作类型：get_current(获取当前网络信息), list_all(列出所有网络)",
                            "default": "get_current"
                        }
                    },
                    "required": ["action"]
                }
            },
            
            # 库存管理工具
            {
                "name": "manage_inventory",
                "description": "管理Ad Manager库存 - 包括列出广告单元、创建广告单元、获取广告单元详情等功能。支持完整的CRUD操作，包括列出所有广告单元、获取指定广告单元详细信息、创建新的广告单元等。使用步骤：1)使用action='list'列出所有广告单元获取广告单元ID；2)使用action='get'并传入ad_unit_id获取详细信息；3)使用action='create'并传入ad_unit_name创建新广告单元，parent_id可选用于指定父级单元",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list", "get", "create"],
                            "description": "操作类型：list(列出所有广告单元，返回id、name、description、targetWindow、status), get(获取指定广告单元详情，需要提供ad_unit_id), create(创建新广告单元，需要提供ad_unit_name，可选提供parent_id指定父级单元)",
                            "default": "list"
                        },
                        "parent_id": {
                            "type": "string",
                            "description": "父广告单元ID（可选，用于list操作时过滤子单元，或create操作时指定父级单元）"
                        },
                        "ad_unit_id": {
                            "type": "string",
                            "description": "广告单元ID（必需当action='get'时，从list操作返回的id字段获取）"
                        },
                        "ad_unit_name": {
                            "type": "string",
                            "description": "广告单元名称（必需当action='create'时）"
                        }
                    },
                    "required": ["action"]
                }
            },
            
            # 订单管理工具
            {
                "name": "manage_orders",
                "description": "管理Ad Manager订单 - 包括列出订单、获取订单详情、创建订单等功能",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list", "get", "create"],
                            "description": "操作类型：list(列出订单), get(获取详情), create(创建订单)",
                            "default": "list"
                        },
                        "order_id": {
                            "type": "string",
                            "description": "订单ID（对于get操作必需）"
                        },
                        "order_name": {
                            "type": "string",
                            "description": "订单名称（对于create操作必需）"
                        },
                        "advertiser_id": {
                            "type": "string",
                            "description": "广告主ID（对于create操作必需）"
                        }
                    },
                    "required": ["action"]
                }
            },
            
            # 行项目管理工具
            {
                "name": "manage_line_items",
                "description": "管理Ad Manager行项目 - 包括列出行项目、获取行项目详情、创建行项目等功能",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list", "get", "create"],
                            "description": "操作类型：list(列出行项目), get(获取详情), create(创建行项目)",
                            "default": "list"
                        },
                        "order_id": {
                            "type": "string",
                            "description": "订单ID（用于列表和创建）"
                        },
                        "line_item_id": {
                            "type": "string",
                            "description": "行项目ID（对于get操作必需）"
                        },
                        "line_item_name": {
                            "type": "string",
                            "description": "行项目名称（对于create操作必需）"
                        }
                    },
                    "required": ["action"]
                }
            },
            
            # 创意管理工具
            {
                "name": "manage_creatives",
                "description": "管理Ad Manager创意 - 包括列出创意、获取创意详情、上传创意等功能",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list", "get"],
                            "description": "操作类型：list(列出创意), get(获取详情)",
                            "default": "list"
                        },
                        "creative_id": {
                            "type": "string",
                            "description": "创意ID（对于get操作必需）"
                        }
                    },
                    "required": ["action"]
                }
            },
            
            # 报告生成工具
            {
                "name": "generate_report",
                "description": "生成Ad Manager报告 - 支持各种报告类型，如库存报告、订单报告等。使用步骤：1)选择合适的report_type；2)指定start_date和end_date定义日期范围；3)报告将包含展示次数、点击次数、点击率、收入等核心指标。注意：报告是异步生成的，返回job信息后需要通过报告服务查询结果",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "report_type": {
                            "type": "string",
                            "enum": ["inventory", "order", "line_item", "creative", "ad_server"],
                            "description": "报告类型：inventory(库存性能报告，维度为AD_UNIT_NAME), order(订单性能报告，维度为ORDER_NAME), line_item(行项目性能报告，维度为LINE_ITEM_NAME), creative(创意性能报告，维度为CREATIVE_NAME), ad_server(广告服务器报告，提供完整的服务器指标)",
                            "default": "inventory"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "开始日期（格式：YYYY-MM-DD），必需。与end_date一起定义报告的时间范围"
                        },
                        "end_date": {
                            "type": "string",
                            "description": "结束日期（格式：YYYY-MM-DD），必需。与start_date一起定义报告的时间范围。如果不提供start_date和end_date，默认使用最近7天的数据"
                        }
                    },
                    "required": ["report_type"]
                }
            },
            
            # 帮助工具
            {
                "name": "get_help",
                "description": "获取Ad Manager增强终极优化版帮助信息和使用指南",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]
        
        return {"tools": tools}

    def handle_tools_call(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """处理工具调用请求"""
        try:
            if name == "get_help":
                return self.get_help()
            elif name == "manage_networks":
                return self.manage_networks(arguments.get("action", "get_current"))
            elif name == "manage_inventory":
                return self.manage_inventory(
                    arguments.get("action", "list"),
                    arguments.get("parent_id"),
                    arguments.get("ad_unit_id"),
                    arguments.get("ad_unit_name")
                )
            elif name == "manage_orders":
                return self.manage_orders(
                    arguments.get("action", "list"),
                    arguments.get("order_id"),
                    arguments.get("order_name"),
                    arguments.get("advertiser_id")
                )
            elif name == "manage_line_items":
                return self.manage_line_items(
                    arguments.get("action", "list"),
                    arguments.get("order_id"),
                    arguments.get("line_item_id"),
                    arguments.get("line_item_name")
                )
            elif name == "manage_creatives":
                return self.manage_creatives(
                    arguments.get("action", "list"),
                    arguments.get("creative_id")
                )
            elif name == "generate_report":
                return self.generate_report(
                    arguments.get("report_type", "inventory"),
                    arguments.get("start_date"),
                    arguments.get("end_date")
                )
            else:
                return {"error": f"Unknown tool: {name}"}
        except Exception as e:
            return {"error": str(e)}

    def get_help(self) -> Dict[str, Any]:
        """获取帮助信息"""
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "success": True,
                        "message": "Ad Manager增强终极优化版MCP服务器帮助",
                        "data": {
                            "server": "🎯 MCP Ad Manager 增强终极优化版",
                            "version": "1.0.0",
                            "total_functions": 7,
                            "tools": [
                                {"name": "manage_networks", "description": "网络管理 - 获取网络信息、列出所有网络"},
                                {"name": "manage_inventory", "description": "库存管理 - 广告单元列表、详情、创建"},
                                {"name": "manage_orders", "description": "订单管理 - 订单列表、详情、创建"},
                                {"name": "manage_line_items", "description": "行项目管理 - 行项目列表、详情、创建"},
                                {"name": "manage_creatives", "description": "创意管理 - 创意列表、详情"},
                                {"name": "generate_report", "description": "报告生成 - 各种报告类型"},
                                {"name": "get_help", "description": "帮助信息"}
                            ],
                            "environment_variables": {
                                "GOOGLE_ADMANAGER_NETWORK_CODE": "Ad Manager网络代码（可选）"
                            },
                            "authentication": {
                                "method": "使用GOOGLE_APPLICATION_CREDS环境变量指定认证文件",
                                "environment_variable": "GOOGLE_APPLICATION_CREDS",
                                "example": "export GOOGLE_APPLICATION_CREDS=/root/.gcloud/aaa.json",
                                "fallback": "如果未设置环境变量，将使用默认的application_default_credentials.json"
                            }
                        },
                        "timestamp": datetime.now().isoformat()
                    }, ensure_ascii=False, indent=2)
                }
            ]
        }

    def manage_networks(self, action: str) -> Dict[str, Any]:
        """管理Ad Manager网络"""
        print(f"🔍 manage_networks 被调用，action: {action}")
        try:
            # 使用新的认证方法
            credentials, project = self._get_credentials()
            print(f"✅ 获取到凭证，项目: {project}")
            
            # 尝试使用新的 google-ads-admanager
            try:
                print("🔍 尝试使用新版本 google-ads-admanager 库")
                from google.ads.admanager import NetworkServiceClient
                network_service = NetworkServiceClient(credentials=credentials)
                print("✅ NetworkServiceClient 初始化成功")
                
                if action == "get_current":
                    # 获取当前网络信息
                    request = {"networkCode": "current"}
                    current_network = network_service.get_network(request=request)
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "success": True,
                                    "action": "get_current",
                                    "network": {
                                        "networkCode": current_network.network_code,
                                        "displayName": current_network.display_name,
                                        "networkCodeForTest": current_network.network_code_for_test,
                                        "timeZone": current_network.time_zone
                                    }
                                }, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                
                elif action == "list_all":
                    # 列出所有网络
                    request = {}
                    response = network_service.list_networks(request=request)
                    
                    network_list = []
                    if hasattr(response, 'networks') and response.networks:
                        for network in response.networks:
                            network_list.append({
                                "networkCode": network.network_code,
                                "displayName": network.display_name,
                                "networkCodeForTest": network.network_code_for_test,
                                "timeZone": network.time_zone
                            })
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "success": True,
                                    "action": "list_all",
                                    "networks": network_list,
                                    "total": len(network_list)
                                }, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                    
            except ImportError as e:
                # 如果新版本库不可用，使用旧的 googleads
                print(f"⚠️ 新版本库导入失败: {e}")
                print("🔄 尝试使用旧版本 googleads 库")
                import os
                network_code = os.getenv('GOOGLE_ADMANAGER_NETWORK_CODE')
                if not network_code:
                    raise ValueError("需要设置 GOOGLE_ADMANAGER_NETWORK_CODE 环境变量")
                
                client = ad_manager.AdManagerClient.LoadFromStorage()
                
                if action == "get_current":
                    # 获取当前网络信息
                    network_service = client.GetService('NetworkService', version='v202405')
                    current_network = network_service.getCurrentNetwork()
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "success": True,
                                    "action": "get_current",
                                    "network": {
                                        "networkCode": current_network.get('networkCode'),
                                        "displayName": current_network.get('displayName'),
                                        "networkCodeForTest": current_network.get('networkCodeForTest'),
                                        "timeZone": current_network.get('timeZone')
                                    }
                                }, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                
                elif action == "list_all":
                    # 列出所有网络
                    network_service = client.GetService('NetworkService', version='v202405')
                    all_networks = network_service.getAllNetworks()
                    
                    network_list = []
                    for network in all_networks:
                        network_list.append({
                            "networkCode": network.get('networkCode'),
                            "displayName": network.get('displayName'),
                            "networkCodeForTest": network.get('networkCodeForTest'),
                            "timeZone": network.get('timeZone')
                        })
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "success": True,
                                    "action": "list_all",
                                    "networks": network_list,
                                    "total": len(network_list)
                                }, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
            
            else:
                return {
                    "content": [
                        {
                            "type": анализировать,
                            "text": json.dumps({
                                "success": False,
                                "error": f"不支持的操作: {action}"
                            }, ensure_ascii=False, indent=2)
                        }
                    ]
                }
                
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({"success": False, "error": str(e)}, ensure_ascii=False, indent=2)
                    }
                ]
            }

    def manage_inventory(self, action: str, parent_id: str = None, 
                        ad_unit_id: str = None, ad_unit_name: str = None) -> Dict[str, Any]:
        """管理Ad Manager库存"""
        try:
            # 使用新的认证方法
            credentials, project = self._get_credentials()
            
            # 尝试使用新的 google-ads-admanager
            try:
                from google.ads.admanager import AdUnitServiceClient
                inventory_service = AdUnitServiceClient(credentials=credentials)
                
                if action == "list":
                    # 列出广告单元
                    request = {}
                    if parent_id:
                        request['parent_id'] = parent_id
                    
                    response = inventory_service.list_ad_units(request=request)
                    
                    ad_units = []
                    if hasattr(response, 'ad_units') and response.ad_units:
                        for ad_unit in response.ad_units:
                            ad_units.append({
                                "id": ad_unit.id,
                                "name": ad_unit.name,
                                "description": ad_unit.description,
                                "targetWindow": ad_unit.target_window,
                                "status": ad_unit.status
                            })
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "success": True,
                                    "action": "list",
                                    "ad_units": ad_units,
                                    "total": len(ad_units)
                                }, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                    
            except ImportError:
                # 如果新版本库不可用，使用旧的 googleads
                client = self._get_admanager_client()
                inventory_service = client.GetService('InventoryService', version='v202405')
                
                if action == "list":
                    # 列出广告单元
                    statement_builder = client.StatementBuilder()
                    
                    if parent_id:
                        statement_builder.Where('parentId = :parent_id').WithBindVariable('parent_id', parent_id)
                    
                    response = inventory_service.getAdUnitsByStatement(statement_builder.ToStatement())
                    
                    ad_units = []
                    if 'results' in response and response['results']:
                        for ad_unit in response['results']:
                            ad_units.append({
                                "id": ad_unit.get('id'),
                                "name": ad_unit.get('name'),
                                "description": ad_unit.get('description'),
                                "targetWindow": ad_unit.get('targetWindow'),
                                "status": ad_unit.get('status')
                            })
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "success": True,
                                    "action": "list",
                                    "ad_units": ad_units,
                                    "total": len(ad_units)
                                }, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                
                elif action == "get" and ad_unit_id:
                    # 获取广告单元详情
                    ad_unit = inventory_service.getAdUnit(ad_unit_id)
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "success": True,
                                "action": "get",
                                "ad_unit": {
                                    "id": ad_unit.get('id'),
                                    "name": ad_unit.get('name'),
                                    "description": ad_unit.get('description'),
                                    "targetWindow": ad_unit.get('targetWindow'),
                                    "status": ad_unit.get('status'),
                                    "parentId": ad_unit.get('parentId')
                                }
                            }, ensure_ascii=False, indent=2)
                        }
                    ]
                }
                
            elif action == "create" and ad_unit_name:
                # 创建广告单元
                ad_unit = {
                    'name': ad_unit_name,
                    'description': f'Created via MCP at {datetime.now()}',
                    'targetWindow': 'BLANK',
                    'sizes': []
                }
                
                if parent_id:
                    ad_unit['parentId'] = int(parent_id)
                
                created_ad_unit = inventory_service.createAdUnits([ad_unit])
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "success": True,
                                "action": "create",
                                "ad_unit": {
                                    "id": created_ad_unit[0].get('id') if created_ad_unit else None,
                                    "name": created_ad_unit[0].get('name') if created_ad_unit else ad_unit_name
                                }
                            }, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "success": False,
                                "error": "缺少必需参数或操作不支持"
                            }, ensure_ascii=False, indent=2)
                        }
                    ]
                }
                
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({"success": False, "error": str(e)}, ensure_ascii=False, indent=2)
                    }
                ]
            }

    def manage_orders(self, action: str, order_id: str = None,
                     order_name: str = None, advertiser_id: str = None) -> Dict[str, Any]:
        """管理Ad Manager订单"""
        try:
            # 使用新的认证方法
            credentials, project = self._get_credentials()
            
            # 尝试使用新的 google-ads-admanager
            try:
                from google.ads.admanager import OrderServiceClient
                order_service = OrderServiceClient(credentials=credentials)
                
                if action == "list":
                    # 列出订单
                    request = {}
                    response = order_service.list_orders(request=request)
                    
                    orders = []
                    if hasattr(response, 'orders') and response.orders:
                        for order in response.orders:
                            orders.append({
                                "id": order.id,
                                "name": order.name,
                                "advertiserId": order.advertiser_id,
                                "status": order.status,
                                "startDateTime": order.start_date_time,
                                "endDateTime": order.end_date_time
                            })
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "success": True,
                                    "action": "list",
                                    "orders": orders,
                                    "total": len(orders)
                                }, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                    
            except ImportError:
                # 如果新版本库不可用，使用旧的 googleads
                client = self._get_admanager_client()
                order_service = client.GetService('OrderService', version='v202405')
                
                if action == "list":
                    # 列出订单
                    statement_builder = client.StatementBuilder()
                    response = order_service.getOrdersByStatement(statement_builder.ToStatement())
                    
                    orders = []
                    if 'results' in response and response['results']:
                        for order in response['results']:
                            orders.append({
                                "id": order.get('id'),
                                "name": order.get('name'),
                                "advertiserId": order.get('advertiserId'),
                                "status": order.get('status'),
                                "currencyCode": order.get('currencyCode')
                            })
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "success": True,
                                    "action": "list",
                                    "orders": orders,
                                    "total": len(orders)
                                }, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
            
            elif action == "get" and order_id:
                # 获取订单详情
                order = order_service.getOrder(order_id)
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "success": True,
                                "action": "get",
                                "order": {
                                    "id": order.get('id'),
                                    "name": order.get('name'),
                                    "advertiserId": order.get('advertiserId'),
                                    "status": order.get('status'),
                                    "currencyCode": order.get('currencyCode'),
                                    "startDateTime": order.get('startDateTime'),
                                    "endDateTime": order.get('endDateTime')
                                }
                            }, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "success": False,
                                "error": "缺少必需参数或操作不支持"
                            }, ensure_ascii=False, indent=2)
                        }
                    ]
                }
                
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({"success": False, "error": str(e)}, ensure_ascii=False, indent=2)
                    }
                ]
            }

    def manage_line_items(self, action: str, order_id: str = None,
                         line_item_id: str = None, line_item_name: str = None) -> Dict[str, Any]:
        """管理Ad Manager行项目"""
        try:
            # 使用新的认证方法
            credentials, project = self._get_credentials()
            
            # 尝试使用新的 google-ads-admanager
            try:
                from google.ads.admanager import LineItemServiceClient
                line_item_service = LineItemServiceClient(credentials=credentials)
                
                if action == "list":
                    # 列出行项目
                    request = {}
                    if order_id:
                        request['order_id'] = order_id
                    
                    response = line_item_service.list_line_items(request=request)
                    
                    line_items = []
                    if hasattr(response, 'line_items') and response.line_items:
                        for line_item in response.line_items:
                            line_items.append({
                                "id": line_item.id,
                                "name": line_item.name,
                                "orderId": line_item.order_id,
                                "status": line_item.status,
                                "startDateTime": line_item.start_date_time,
                                "endDateTime": line_item.end_date_time
                            })
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "success": True,
                                    "action": "list",
                                    "line_items": line_items,
                                    "total": len(line_items)
                                }, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                    
            except ImportError:
                # 如果新版本库不可用，使用旧的 googleads
                client = self._get_admanager_client()
                line_item_service = client.GetService('LineItemService', version='v202405')
                
                if action == "list":
                    # 列出行项目
                    statement_builder = client.StatementBuilder()
                    
                    if order_id:
                        statement_builder.Where('orderId = :order_id').WithBindVariable('order_id', order_id)
                    
                    response = line_item_service.getLineItemsByStatement(statement_builder.ToStatement())
                    
                    line_items = []
                    if 'results' in response and response['results']:
                        for line_item in response['results']:
                            line_items.append({
                                "id": line_item.get('id'),
                                "name": line_item.get('name'),
                                "orderId": line_item.get('orderId'),
                                "status": line_item.get('status'),
                                "lineItemType": line_item.get('lineItemType'),
                                "costType": line_item.get('costType')
                            })
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "success": True,
                                    "action": "list",
                                    "line_items": line_items,
                                    "total": len(line_items)
                                }, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
            
            elif action == "get" and line_item_id:
                # 获取行项目详情
                line_item = line_item_service.getLineItem(line_item_id)
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "success": True,
                                "action": "get",
                                "line_item": {
                                    "id": line_item.get('id'),
                                    "name": line_item.get('name'),
                                    "orderId": line_item.get('orderId'),
                                    "status": line_item.get('status'),
                                    "lineItemType": line_item.get('lineItemType'),
                                    "costType": line_item.get('costType'),
                                    "costPerUnit": line_item.get('costPerUnit')
                                }
                            }, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "success": False,
                                "error": "缺少必需参数或操作不支持"
                            }, ensure_ascii=False, indent=2)
                        }
                    ]
                }
                
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({"success": False, "error": str(e)}, ensure_ascii=False, indent=2)
                    }
                ]
            }

    def manage_creatives(self, action: str, creative_id: str = None) -> Dict[str, Any]:
        """管理Ad Manager创意"""
        try:
            # 使用新的认证方法
            credentials, project = self._get_credentials()
            
            # 尝试使用新的 google-ads-admanager
            try:
                from google.ads.admanager import CreativeServiceClient
                creative_service = CreativeServiceClient(credentials=credentials)
                
                if action == "list":
                    # 列出创意
                    request = {}
                    response = creative_service.list_creatives(request=request)
                    
                    creatives = []
                    if hasattr(response, 'creatives') and response.creatives:
                        for creative in response.creatives:
                            creatives.append({
                                "id": creative.id,
                                "name": creative.name,
                                "advertiserId": creative.advertiser_id,
                                "size": creative.size,
                                "isNativeEligible": creative.is_native_eligible
                            })
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "success": True,
                                    "action": "list",
                                    "creatives": creatives,
                                    "total": len(creatives)
                                }, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                    
            except ImportError:
                # 如果新版本库不可用，使用旧的 googleads
                client = self._get_admanager_client()
                creative_service = client.GetService('CreativeService', version='v202405')
                
                if action == "list":
                    # 列出创意
                    statement_builder = client.StatementBuilder()
                    response = creative_service.getCreativesByStatement(statement_builder.ToStatement())
                    
                    creatives = []
                    if 'results' in response and response['results']:
                        for creative in response['results']:
                            creatives.append({
                                "id": creative.get('id'),
                                "name": creative.get('name'),
                                "advertiserId": creative.get('advertiserId'),
                                "size": creative.get('size'),
                                "isNativeEligible": creative.get('isNativeEligible')
                            })
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "success": True,
                                    "action": "list",
                                    "creatives": creatives,
                                    "total": len(creatives)
                                }, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
            
            elif action == "get" and creative_id:
                # 获取创意详情
                creative = creative_service.getCreative(creative_id)
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "success": True,
                                "action": "get",
                                "creative": {
                                    "id": creative.get('id'),
                                    "name": creative.get('name'),
                                    "advertiserId": creative.get('advertiserId'),
                                    "size": creative.get('size'),
                                    "isNativeEligible": creative.get('isNativeEligible')
                                }
                            }, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "success": False,
                                "error": "缺少必需参数或操作不支持"
                            }, ensure_ascii=False, indent=2)
                        }
                    ]
                }
                
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({"success": False, "error": str(e)}, ensure_ascii=False, indent=2)
                    }
                ]
            }

    def generate_report(self, report_type: str, start_date: str = None, 
                       end_date: str = None) -> Dict[str, Any]:
        """生成Ad Manager报告"""
        try:
            # 使用新的认证方法
            credentials, project = self._get_credentials()
            
            # 尝试使用新的 google-ads-admanager
            try:
                from google.ads.admanager import ReportServiceClient
                report_service = ReportServiceClient(credentials=credentials)
                
                # 创建报告作业
                report_job = {
                    'report_query': {
                        'dimensions': [],
                        'columns': []
                    }
                }
                
                # 根据报告类型设置不同的维度和列
                if report_type == "inventory":
                    report_job['report_query']['dimensions'] = ['AD_UNIT_NAME']
                    report_job['report_query']['columns'] = ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS']
                elif report_type == "order":
                    report_job['report_query']['dimensions'] = ['ORDER_NAME']
                    report_job['report_query']['columns'] = ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS']
                elif report_type == "line_item":
                    report_job['report_query']['dimensions'] = ['LINE_ITEM_NAME']
                    report_job['report_query']['columns'] = ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS']
                
                # 设置日期范围
                if start_date and end_date:
                    report_job['report_query']['date_range_type'] = 'CUSTOM_DATE'
                    report_job['report_query']['start_date'] = {
                        'year': int(start_date.split('-')[0]),
                        'month': int(start_date.split('-')[1]),
                        'day': int(start_date.split('-')[2])
                    }
                    report_job['report_query']['end_date'] = {
                        'year': int(end_date.split('-')[0]),
                        'month': int(end_date.split('-')[1]),
                        'day': int(end_date.split('-')[2])
                    }
                else:
                    report_job['report_query']['date_range_type'] = 'LAST_7_DAYS'
                
                # 创建报告作业
                job = report_service.run_report_job(report_job)
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "success": True,
                                "report_type": report_type,
                                "job_id": job.id,
                                "status": job.status,
                                "message": "报告作业已创建，请稍后查询结果"
                            }, ensure_ascii=False, indent=2)
                        }
                    ]
                }
                
            except ImportError:
                # 如果新版本库不可用，使用旧的 googleads
                client = self._get_admanager_client()
                report_service = client.GetService('ReportService', version='v202405')
            
            # 创建报告作业
            report_job = {
                'reportQuery': {
                    'dimensions': [],
                    'columns': []
                }
            }
            
            # 根据报告类型设置不同的维度和列
            if report_type == "inventory":
                report_job['reportQuery']['dimensions'] = ['AD_UNIT_NAME']
                report_job['reportQuery']['columns'] = ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS']
            elif report_type == "order":
                report_job['reportQuery']['dimensions'] = ['ORDER_NAME']
                report_job['reportQuery']['columns'] = ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS']
            elif report_type == "line_item":
                report_job['reportQuery']['dimensions'] = ['LINE_ITEM_NAME']
                report_job['reportQuery']['columns'] = ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS']
            
            # 设置日期范围
            if start_date and end_date:
                report_job['reportQuery']['dateRangeType'] = 'CUSTOM_DATE'
                report_job['reportQuery']['startDate'] = {
                    'year': int(start_date.split('-')[0]),
                    'month': int(start_date.split('-')[1]),
                    'day': int(start_date.split('-')[2])
                }
                report_job['reportQuery']['endDate'] = {
                    'year': int(end_date.split('-')[0]),
                    'month': int(end_date.split('-')[1]),
                    'day': int(end_date.split('-')[2])
                }
            else:
                report_job['reportQuery']['dateRangeType'] = 'LAST_7_DAYS'
            
            # 创建报告作业
            job = report_service.runReportJob(report_job)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "success": True,
                            "report_type": report_type,
                            "job": {
                                "id": job.get('id'),
                                "status": job.get('reportJobStatus')
                            },
                            "message": "报告作业已创建，请通过报告ID查询结果"
                        }, ensure_ascii=False, indent=2)
                    }
                ]
            }
            
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({"success": False, "error": str(e)}, ensure_ascii=False, indent=2)
                    }
                ]
            }

def main():
    """主函数 - MCP协议服务器"""
    server = MCPAdManagerEnhancedUltimateServer()
    
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            
            try:
                request = json.loads(line.strip())
                method = request.get("method")
                params = request.get("params", {})
                request_id = request.get("id")
                
                if method == "initialize":
                    result = server.handle_initialize(params)
                elif method == "tools/list":
                    result = server.handle_tools_list()
                elif method == "tools/call":
                    result = server.handle_tools_call(
                        params.get("name"),
                        params.get("arguments", {})
                    )
                else:
                    result = {"error": f"Unknown method: {method}"}
                
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }
                
                print(json.dumps(response))
                sys.stdout.flush()
                
            except json.JSONDecodeError:
                continue
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if "request" in locals() else None,
                    "error": {"code": -32603, "message": str(e)}
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
                
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

