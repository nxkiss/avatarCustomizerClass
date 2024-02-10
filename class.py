import requests
import random
import json
import requests
class AvatarCustomizer:
    def __init__(self, cookie):
        self.cookie = cookie
        self.session = self._create_session()
        self.bundle_ids = [979, 722, 741]
        self.user_id = self.get_user_id()
        self.ArmPack = self.selectRandomItemFromArr([
            {"Pack1": [6445260402, 6445263379]}, 
            {"Pack2": [11572074613, 11572079320]},
            {"Pack3": [6494051962, 6494055013]} 
        ])
        self.LegPack = self.selectRandomItemFromArr([
            {"Pack1": [6494053789, 6494055897]},
            {"Pack2": [6445262286, 6445265102]},
            {"Pack2": [11572076845, 11572081357]}
        ])
        self.heads = self.selectRandomItemFromArr([6340227, 6445269791, 6494064291, 6340213])
        self.torsoIds = self.selectRandomItemFromArr([6445268819, 11572083496, 6494056892])
        self.DisplayNames = self.selectRandomItemFromArr(["Vertex","Blitz","Viper","Cipher","Nova","Xeno","Jet","Zenith","Frost","Raven","Fury","Zero","Lynx","Apex","Quasar","Echo","Blaze","Venom","Phoenix","Spark","Ghost","Bolt","Arctic","Zephyr","Ninja","Sonic","Shadow","Abyss","Zen","Cipher","Rogue","Inferno","Titan","Legend","Neon","Thunder","Storm","Vortex","Titan","Storm","Inferno","Legend","Neon","Thunder","Vortex","Shadow","Ghost","Bolt","Blaze","Venom","Raven","Viper","Apex","Frost","Zenith","Jet","Xeno","Nova","Cipher","Rogue","Lynx","Zero","Fury","Raven","Blitz","Vertex","Echo","Quasar","Arctic","Ninja","Zephyr","Abyss","Phoenix","Sonic","Spark","Venom","Ghost","Zen","Bolt","Frost","Viper","Apex","Titan","Storm","Neon","Thunder","Inferno","Vortex","Shadow","Legend","Jet","Nova","Xeno"])


    def selectRandomItemFromArr(self, arr):
        return random.choice(arr) if isinstance(arr[0], dict) else arr[random.randint(0, len(arr) - 1)]
    def get_user_id(self):
        response = self.session.get("https://users.roblox.com/v1/users/authenticated")
        return response.json()["id"]
    def _create_session(self):
        session = requests.Session()

        xcsrf_token_response = requests.post("https://auth.roblox.com/v2/logout", cookies={".ROBLOSECURITY": self.cookie})
        xcsrf_token = xcsrf_token_response.headers["x-csrf-token"]
        session.cookies.update({".ROBLOSECURITY": self.cookie})
        session.headers.update({"referer": "https://www.roblox.com", "x-csrf-token": xcsrf_token})

        return session
    def is_item_owned(self, product_id):
        response = self.session.get(f'https://inventory.roblox.com/v1/users/{self.user_id}/items/Product/{product_id}')
        return response.status_code == 200

    def get_product_id(self, bundle_id):
        response = self.session.get('https://catalog.roblox.com/v1/bundles/details', params={'bundleIds': bundle_id})
        return response.json()[0]["product"]["id"]
    
    def wear_item(self, asset_id):
        response = self.session.post(f'https://avatar.roblox.com/v1/avatar/assets/{asset_id}/wear')
        return response.json()
    
    def purchase_item(self, product_id, expected_price):
        if self.is_item_owned(product_id):
            print(f'Item {product_id} is already owned.')
            return False

        response = self.session.post('https://economy.roblox.com/v1/purchases/products/' + str(product_id), json={"expectedPrice": expected_price})
        return response.json()
    def purchaseall(self):
        for bundle_id in self.bundle_ids:
            product_id = self.get_product_id(bundle_id)
            purchase = self.purchase_item(product_id, 0)
            if purchase:
                print(purchase)
    def wearall(self):
        asset_ids = [self.torsoIds]
        for pack_name, items in self.ArmPack.items():
            for item in items:
                asset_ids.append(item)
        for pack_name, items in self.LegPack.items():
            for item in items:
                asset_ids.append(item)
        asset_ids.append(self.heads)

        payload = {
            "assetIds": asset_ids
        }

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        response = self.session.post("https://avatar.roblox.com/v1/avatar/set-wearing-assets", headers=headers, data=json.dumps(payload))
        print(response.json())
    def changeDisplayName(self):
            response = self.session.patch(
                f"https://users.roblox.com/v1/users/{self.user_id}/display-names?userId={self.user_id}&newDisplayName={self.DisplayNames}&showAgedUpDisplayName=true",
                json={
                    "newDisplayName": self.DisplayNames
                },
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
                }
            )
    def run(self):
        self.purchaseall()
        self.wearall()
        self.changeDisplayName()
        return


