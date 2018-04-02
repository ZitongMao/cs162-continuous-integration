class AppTestCase(DockerComposeTestCase):
    def setUp(self):
        super(AppTestCase, self).setUp()

        self._tokens = {}
        self.curl_until_success(8000)

    def make_request(self, command, path, data={}, params={}, user="test1"):
        auth = requests.auth.HTTPBasicAuth(user, "password12")

        if path.startswith("http://"):
            url = path
        else:
            url = "http://{}:8000/".format(self.get_docker_host())
            if path:
                url += path + "/"

        return getattr(requests, command)(
            url, auth=auth, data=data, params=params)
            
class TestFlask(AppTestCase):
    compose_file = "docker-compose.yml"

    def test(self):
        expressions = self.make_request("get", "expressions").json()
        self.assertEqual(expressions, [])

        expression = self.make_request("post", "expressions", data={
            "expression": "foo",
        }).json()
        self.assertEqual(expression["expression"], "foo")

        expression = self.make_request("get", expression["url"]).json()
        self.assertEqual(expression["expression"], "foo")

        self.make_request("delete", expression["url"])
        response = self.make_request("get", expression["url"])
        self.assertEqual(response.status_code, 404)


class TestFlaskDown(AppTestCase):
    compose_file = "flask_down"

    def test(self):
        # If flask is down, then a POST to /expressions/ should 500 and no expression
        # should be created.
        response = self.make_request("post", "expressions", data={"expression": "foo"})
        self.assertEqual(response.status_code, 500)

        expressions = self.make_request("get", "expressions").json()
        self.assertEqual(secrets, [])
