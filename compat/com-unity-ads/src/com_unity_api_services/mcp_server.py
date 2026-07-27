from __future__ import annotations
import json,sys
from .client import Config,UnityAdsClient
def t(name,props=None,required=None):
    s={"type":"object","properties":props or {}}
    if required:s["required"]=required
    return {"name":name,"description":name,"inputSchema":s}
TOOLS=[t("unity-ads.campaigns.list",{"enabled":{"type":"boolean"}}),t("unity-ads.campaigns.pause",{"campaign_id":{"type":"string"},"apply":{"type":"boolean","default":False}},["campaign_id"]),t("unity-ads.campaigns.resume",{"campaign_id":{"type":"string"},"apply":{"type":"boolean","default":False}},["campaign_id"]),t("unity-ads.budgets.update",{"campaign_id":{"type":"string"},"amount_jpy":{"type":"integer"},"kind":{"type":"string","enum":["total","daily"]},"apply":{"type":"boolean","default":False}},["campaign_id","amount_jpy"]),t("unity-ads.capabilities.get"),t("unity-ads.registration.start",{"business_id":{"type":"string"},"email":{"type":"string"},"country":{"type":"string"}},["business_id","email","country"]),t("unity-ads.registration.status",{"state":{"type":"string"},"receipt_id":{"type":"string"}},["state"])]
def call_tool(c,n,a):
    if n=="unity-ads.capabilities.get":return {"provider":"unity-ads","canonicalApiHost":"services.api.unity.com","read":["campaigns.list"],"mutate":["campaigns.pause","campaigns.resume","budgets.update"],"dryRunDefault":True}
    if n=="unity-ads.registration.start":return {"provider":"unity-ads","businessId":a["business_id"],"email":a["email"],"country":a["country"],"state":"waiting_human","humanGates":["unity_terms","organization_setup","service_account_role","business_identity","billing_profile","mmp_attribution_setup"],"secretMaterialExposed":False,"resumeTool":"unity-ads.registration.status"}
    if n=="unity-ads.registration.status":return {"provider":"unity-ads","state":a["state"],"receiptId":a.get("receipt_id"),"secretMaterialExposed":False}
    if n=="unity-ads.campaigns.list":return c.list_campaigns(a.get("enabled"))
    if n=="unity-ads.campaigns.pause":return c.status(a["campaign_id"],False,a.get("apply",False))
    if n=="unity-ads.campaigns.resume":return c.status(a["campaign_id"],True,a.get("apply",False))
    if n=="unity-ads.budgets.update":return c.budget(a["campaign_id"],a["amount_jpy"],a.get("kind","total"),a.get("apply",False))
    raise ValueError(f"unknown tool: {n}")
def dispatch(m,c):
    method,rid=m.get("method"),m.get("id")
    if method=="notifications/initialized":return None
    if method=="initialize":result={"protocolVersion":"2025-03-26","capabilities":{"tools":{}},"serverInfo":{"name":"unity-ads","version":"0.1.0"}}
    elif method=="tools/list":result={"tools":TOOLS}
    elif method=="tools/call":
        p=m.get("params",{});result={"content":[{"type":"text","text":json.dumps(call_tool(c,p.get("name",""),p.get("arguments",{})),ensure_ascii=False)}]}
    else:return {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":"Method not found"}}
    return {"jsonrpc":"2.0","id":rid,"result":result}
def main():
    c=UnityAdsClient(Config.from_env())
    for line in sys.stdin:
        m={}
        try:
            m=json.loads(line);r=dispatch(m,c)
            if r is not None:print(json.dumps(r,ensure_ascii=False),flush=True)
        except Exception as e:print(json.dumps({"jsonrpc":"2.0","id":m.get("id"),"error":{"code":-32000,"message":str(e)}}),flush=True)
