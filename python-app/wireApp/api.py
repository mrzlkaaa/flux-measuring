from flask import Blueprint, session
from .consumer import ApiRequest
import json

api = Blueprint('api', __name__)

# @api.route("/api/chart", methods=['GET'])
# def chart():
#     id = r.get("api_ID")
#     print(f" [x] Requesting {id})")
#     response = ApiRequest().call(id)
#     decoded = response.decode('utf-8').replace("'", '"')
#     jsn_loads = json.loads(decoded)
#     jsn_dumps = json.dumps(jsn_loads, indent=4, sort_keys=True)
#     print(" [.] Got %r" % jsn_dumps)
#     return jsn_dumps
    # return {"Hello": f"World its <{id}>"}