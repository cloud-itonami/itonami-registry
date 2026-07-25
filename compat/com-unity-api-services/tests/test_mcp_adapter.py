import json,pytest
from com_unity_api_services.client import Config,UnityAdsClient
from com_unity_api_services.mcp_server import TOOLS,call_tool,dispatch
CID="5eb26a338a232100e4bb6361"
def c(currency="JPY"):return UnityAdsClient(Config("key","credential-value-9f3a","5772680389521","5eb26a338a232100e4bb5893",currency,3000),opener=lambda _:None)
def test_boundary():
    assert all(x["name"].startswith("unity-ads.") for x in TOOLS)
    assert dispatch({"id":1,"method":"initialize"},c())["result"]["serverInfo"]["name"]=="unity-ads"
    assert call_tool(c(),"unity-ads.capabilities.get",{})["canonicalApiHost"]=="services.api.unity.com"
def test_status_dry_run():
    assert c().status(CID,False)["changes"]=={"enabled":False}
    with pytest.raises(ValueError):c().status("bad",False)
def test_budget_guard():
    assert c().budget(CID,3000,"daily")["changes"]=={"daily":"3000.00"}
    with pytest.raises(ValueError):c().budget(CID,3001)
    with pytest.raises(ValueError):c("USD").budget(CID,100)
def test_registration_secret_free():
    r=call_tool(c(),"unity-ads.registration.start",{"business_id":"b","email":"a@example.test","country":"JPN"})
    assert r["state"]=="waiting_human" and not r["secretMaterialExposed"] and c().config.secret not in json.dumps(r)
