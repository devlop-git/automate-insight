import requests
import json

import urllib
from app.core.config import settings
from app.utils.helpers import extract_form_data


class SupersetClient:
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls._instance = super(SupersetClient, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        self.base_url = settings.SUPERSET_BASE_URL
        self.username = settings.SUPERSET_USERNAME
        self.password = settings.SUPERSET_PASSWORD

        self.session = requests.Session()
        self.session.cookies.set(
            "session",
            ".eJw1kdtum0AURX-l4rmu5gYDecMkgG1sxxB8SVWhYS5gg-0EBhMT5d9L1fbxbGlJ--z1aWSqkW1pPOimk9-N7CiMB8PiCNsKk5xRRQXljrIAyxXJFVeECqkUznHOCQeQI2nSHAgCGBCCSIWACQAGhDKHijwX2MyhcqDAhEIIeW5TCizAHQlNKBWBFqQEM0QcU3EBbWBTBxljka6Vzd82EDtjwNtGZfpaycsYmcgWDrYQBhbMAbUgIIBjkymLAZNzSSwLMUnkyNVXzmo5MiP43biyTo_PfhrftPHw07gz5PxwgftSXT1uqVMStuYqTZAf3aT0Kk7T5nRa-Wn5fp6J1VTz2lYvwweEKHldTpl_r1DaYHBxjzD2G0ou-bqaBG04Dy9BP7DJ4nIGr2ew0GLTtG0WPKHtPEN9aW9fOYgjP6LiXiYHHXp9PWVFFOx4vQGrbFq-3M-1t0-yKgZN-TgnfChWC3ZIT0MSIlesMyC60HtLs3p728esb4kojjRwNYyrzWK2Xdwdtv1Q3uGs54NXbm_KS_anJTNj6ML1EcPJeK-UP3vOunSWoF0XDGywPyJYRv3BQXehMyz5c1n0zCsOCzdZJm68SfxNGOzR8ijWkxSW0yf3bWfROh-S3WO07wFy8Liy8evr39TZW3O9HYVsRgHF9VrU8r-ErNVM__HSXTTV0zl9907vpFOw21R-XybljdIb2hlfvwEThNRU.aZ6ReA.EcfO7gUuJ-eggXLPj-zaY9zV9C8",
            domain="superset.nevejewels.org",
        )
        # self.login()

    def login(self):

        login = self.session.post(
            f"{self.base_url}/security/login",
            json={
                "username": self.username,
                "password": self.password,
                "provider": "db",
                "refresh": True
            },
        )

        login.raise_for_status()

        access_token = login.json()["access_token"]
        
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}"
        })

        
    def getDashboardInfo(self,id):
        url = f"{self.base_url}/dashboard/{id}"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()["result"]

        return data
    
    def getChartList(self,id):
        url = f"{self.base_url}/dashboard/{id}/charts"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()["result"]

        sliceData = []
        for items in data:
            sliceData.append(
                {
                    "chart_id": items["id"],
                    "chart_name": items["slice_name"],
                    "chart_url": items["slice_url"],
                    "dashboard_id":id,
                }
            )

        return sliceData

    def explore(self, sliceData):
        sliceUrl = sliceData.get("chart_url")
        url = f"{self.base_url}{sliceUrl}"
        response = self.session.get(url)
        response.raise_for_status()
        result = response.json()["result"]
        query_context = result["slice"]["query_context"]
        return sliceData,query_context
    
    def explore_v1(self, chartData):
        # print(chartData)
        # sliceUrl = chartData.get("chart_url")
        url = f"{self.base_url}{chartData.get("chart_url")}"
        response = self.session.get(url)
        response.raise_for_status()
        result = response.json()["result"]
        query_context = result["slice"]["query_context"]
        return query_context


    def chartDetails(self, sliceInfo,query_context=None):
        url = f"{self.base_url}/chart/data"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if isinstance(query_context, str):
            query_context = json.loads(query_context)
    
        response = self.session.post(url,headers=headers, json=query_context)
      
        response.raise_for_status()
        data = response.json()["result"][0]['data']
        sliceInfo['data'] = data
        
        return sliceInfo
    
    def chartDetails_v1(self, chart_detail):
        url = f"{self.base_url}/chart/data"
        query_context = chart_detail['query_context']
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if isinstance(query_context, str):
            query_context = json.loads(query_context)
    
        response = self.session.post(url,headers=headers, json=query_context)
      
        response.raise_for_status()
        data = response.json()["result"][0]['data']
        chart_detail['data'] = data
        
        return chart_detail
    
    
    def getAllDashboards(self):
        url = f"{self.base_url}/dashboard/?q=(order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:25,select_columns:!(id,dashboard_title,published,url,slug,changed_by,changed_by.id,changed_by.first_name,changed_by.last_name,changed_on_delta_humanized,owners,owners.id,owners.first_name,owners.last_name,tags.id,tags.name,tags.type,status,certified_by,certification_details,changed_on))"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()["result"]
        dashboardInfo = [
            {
                "dashboard_id": d["id"],
                "name": d["dashboard_title"]
            }
            for d in data
        ]
        return dashboardInfo
