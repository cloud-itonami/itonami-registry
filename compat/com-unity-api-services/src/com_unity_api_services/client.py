from __future__ import annotations
import base64,json,os,re
from dataclasses import dataclass,asdict
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode

@dataclass(frozen=True)
class Config:
    key_id:str=""; secret:str=""; organization_id:str=""; campaign_set_id:str=""; currency:str=""; max_budget_jpy:int=3000
    @classmethod
    def from_env(cls): return cls(os.getenv("UNITY_ADS_SERVICE_KEY_ID",""),os.getenv("UNITY_ADS_SERVICE_SECRET",""),os.getenv("UNITY_ADS_ORGANIZATION_ID",""),os.getenv("UNITY_ADS_CAMPAIGN_SET_ID",""),os.getenv("UNITY_ADS_ACCOUNT_CURRENCY","").upper(),int(os.getenv("UNITY_ADS_MAX_BUDGET_JPY","3000")))
    def validate(self):
        if not all((self.key_id,self.secret,self.organization_id,self.campaign_set_id,self.currency)): raise ValueError("incomplete Unity Ads credential configuration")
        if not self.organization_id.isdigit() or not re.fullmatch(r"[0-9a-fA-F]{24}",self.campaign_set_id): raise ValueError("invalid Unity resource identity")

@dataclass(frozen=True)
class Plan:
    operation:str; organization_id:str; campaign_set_id:str; campaign_id:str; changes:dict; dry_run:bool=True
    def dict(self): return asdict(self)

class UnityAdsClient:
    host="services.api.unity.com"
    def __init__(self,config,opener=urlopen): self.config,self.opener=config,opener
    def _cid(self,value):
        if not re.fullmatch(r"[0-9a-fA-F]{24}",value or ""): raise ValueError("campaign ID must be 24 hex characters")
        return value
    def _request(self,method,path,payload=None,query=None):
        self.config.validate()
        url=f"https://{self.host}/advertise/v1/organizations/{self.config.organization_id}/apps/{self.config.campaign_set_id}{path}"
        if query:url+="?"+urlencode(query)
        data=json.dumps(payload,separators=(",",":")).encode() if payload is not None else None
        auth=base64.b64encode(f"{self.config.key_id}:{self.config.secret}".encode()).decode()
        req=Request(url,data=data,method=method,headers={"authorization":f"Basic {auth}","content-type":"application/json"})
        try:
            with self.opener(req) as response:return json.loads(response.read() or b"{}")
        except HTTPError as e: raise RuntimeError(f"Unity Advertising API HTTP {e.code}: {e.read().decode(errors='replace')}") from e
    def list_campaigns(self,enabled=None): return self._request("GET","/campaigns",query={"filter[enabled]":str(enabled).lower()} if enabled is not None else None)
    def status(self,campaign_id,enabled,apply=False):
        cid=self._cid(campaign_id); changes={"enabled":bool(enabled)}
        plan=Plan("campaigns.resume" if enabled else "campaigns.pause",self.config.organization_id,self.config.campaign_set_id,cid,changes)
        return self._request("PATCH",f"/campaigns/{cid}",changes) if apply else plan.dict()
    def budget(self,campaign_id,amount_jpy,kind="total",apply=False):
        cid=self._cid(campaign_id)
        if kind not in {"total","daily"}: raise ValueError("kind must be total or daily")
        if self.config.currency!="JPY": raise ValueError("JPY cap cannot authorize a non-JPY account")
        if not 1<=amount_jpy<=self.config.max_budget_jpy: raise ValueError(f"budget must be 1..{self.config.max_budget_jpy} JPY")
        changes={kind:f"{amount_jpy:.2f}"}; plan=Plan("budgets.update",self.config.organization_id,self.config.campaign_set_id,cid,changes)
        return self._request("PATCH",f"/campaigns/{cid}/budget",changes) if apply else plan.dict()
