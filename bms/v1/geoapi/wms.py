# -*- coding: utf-8 -*-
from bms.v1.handlers import Viewer
from tornado.httpclient import (
    AsyncHTTPClient,
    HTTPError,
    HTTPRequest
)


class Wms(Viewer):
    
    async def get(self):
        http_client = AsyncHTTPClient()
        lang = self.get_argument('lang', 'en')
        try:
            self.set_header("Content-Type", "text/xml")
            url = (
                # "https://wms.swisstopo.admin.ch"
                "http://wms.geo.admin.ch"
                "?request=getCapabilities&service=WMS&lang={}"
            ).format(lang)
            print(f"Fetching WMS GetCapability: {url}")
            response = await http_client.fetch(
                HTTPRequest(
                    url=url,
                    # auth_username='user_br82a',
                    # auth_password='co4l94qqzf23ne9m'
                )
            )

            print(" > Done.")
            self.write(response.body)

        except HTTPError as e:
            print(" > Error: " + str(e))

        except Exception as e:
            # Other errors are possible, such as IOError.
            print(" > Error: " + str(e))

        http_client.close()
