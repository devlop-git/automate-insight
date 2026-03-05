import requests
import json

import urllib
from app.core.config import settings
from app.utils.helpers import extract_form_data


class SupersetClient:
    def __init__(self):
        self.base_url = settings.SUPERSET_BASE_URL
        self.session = requests.Session()
        self.session.cookies.set(
            "session",
            ".eJw1kdtum0AURX-l4rmu5gYDecMkgG1sxxB8SVWhYS5gg-0EBhMT5d9L1fbxbGlJ--z1aWSqkW1pPOimk9-N7CiMB8PiCNsKk5xRRQXljrIAyxXJFVeECqkUznHOCQeQI2nSHAgCGBCCSIWACQAGhDKHijwX2MyhcqDAhEIIeW5TCizAHQlNKBWBFqQEM0QcU3EBbWBTBxljka6Vzd82EDtjwNtGZfpaycsYmcgWDrYQBhbMAbUgIIBjkymLAZNzSSwLMUnkyNVXzmo5MiP43biyTo_PfhrftPHw07gz5PxwgftSXT1uqVMStuYqTZAf3aT0Kk7T5nRa-Wn5fp6J1VTz2lYvwweEKHldTpl_r1DaYHBxjzD2G0ou-bqaBG04Dy9BP7DJ4nIGr2ew0GLTtG0WPKHtPEN9aW9fOYgjP6LiXiYHHXp9PWVFFOx4vQGrbFq-3M-1t0-yKgZN-TgnfChWC3ZIT0MSIlesMyC60HtLs3p728esb4kojjRwNYyrzWK2Xdwdtv1Q3uGs54NXbm_KS_anJTNj6ML1EcPJeK-UP3vOunSWoF0XDGywPyJYRv3BQXehMyz5c1n0zCsOCzdZJm68SfxNGOzR8ijWkxSW0yf3bWfROh-S3WO07wFy8Liy8evr39TZW3O9HYVsRgHF9VrU8r-ErNVM__HSXTTV0zl9907vpFOw21R-XybljdIb2hlfvwEThNRU.aZ6ReA.EcfO7gUuJ-eggXLPj-zaY9zV9C8",
            domain="superset.nevejewels.org",
        )

    def getChartList(self,id):
        url = f"{self.base_url}/dashboard/{id}/charts"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()["result"]

        sliceData = []
        for items in data:
            sliceData.append(
                {
                    "id": items["id"],
                    "slice_name": items["slice_name"],
                    "slice_url": items["slice_url"],
                }
            )

        return sliceData

    def explore(self, sliceData):
        sliceUrl = sliceData.get("slice_url")
        url = f"{self.base_url}{sliceUrl}"
        response = self.session.get(url)
        response.raise_for_status()
        result = response.json()["result"]
        query_context = result["slice"]["query_context"]
        return sliceData,query_context

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

