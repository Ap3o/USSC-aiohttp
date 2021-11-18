from aiohttp.test_utils import AioHTTPTestCase
import json

import application


class USSCTestCase(AioHTTPTestCase):
    async def get_application(self):
        return application.create_app()

    async def test_get_1(self):
        async with self.client.request("GET", "/convert/?from=RRR&to=USD&amount=42") as response:
            self.assertEqual(response.status, 200)
            text = await response.text()
            self.assertTrue("error" in json.loads(text))

    async def test_get_2(self):
        async with self.client.request("GET", "/convert/?from=RUB&to=USD&amount=42") as response:
            self.assertEqual(response.status, 200)
            text = await response.text()
            self.assertTrue("result" in json.loads(text))

    async def test_get_3(self):
        async with self.client.request("GET", "/convert/?from=RUB&to=RRR&amount=42") as response:
            self.assertEqual(response.status, 200)
            text = await response.text()
            self.assertTrue("error" in json.loads(text))

    async def test_get_4(self):
        async with self.client.request("GET", "/convert/?from=RUB&to=USD&amount=fff") as response:
            self.assertEqual(response.status, 200)
            text = await response.text()
            self.assertTrue("error" in json.loads(text))

    async def test_flush(self):
        async with self.client.request("POST", "/database/", params={"merge": 0}) as response:
            self.assertEqual(response.status, 200)
            text = await response.text()
            self.assertTrue("result" in json.loads(text))
        async with self.client.request("GET", "/convert/?from=RUB&to=USD&amount=42") as response:
            self.assertEqual(response.status, 200)
            text = await response.text()
            self.assertTrue("result" in json.loads(text))

    async def test_post_1(self):
        async with self.client.request("POST", "/database/", params={"merge": 1}) as response:
            self.assertEqual(response.status, 200)
            text = await response.text()
            self.assertTrue("result" in json.loads(text))

    async def test_post_2(self):
        async with self.client.request("POST", "/database/", params={"merge": "ff"}) as response:
            self.assertEqual(response.status, 200)
            text = await response.text()
            self.assertTrue("error" in json.loads(text))

    async def test_post_3(self):
        async with self.client.request("POST", "/database/") as response:
            self.assertEqual(response.status, 200)
            text = await response.text()
            self.assertTrue("error" in json.loads(text))
