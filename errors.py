import json

class APIError(Exception):
    httpcode = 400

    @property
    def json(self):
        raise NotImplementedError("subclasses gotta implement this!")

class NoUserFoundError(APIError):
    @property
    def json(self):
        return json.dumps({"error": "ERRNOUSERFOUND"})

# This really isn't an error per-se.
# We just use it to return an error on methods that don't return anything else.
class NoError(APIError):
    httpcode = 200

    @property
    def json(self):
        return json.dumps({"error": "None", "result": "ok"})
