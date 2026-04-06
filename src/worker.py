import json

async def on_fetch(request, env):
    return new_response({"message": "Hello", "status": "ok"})

def new_response(data, status=200):
    from js import Response
    body = json.dumps(data)
    return Response.new(body, status=status, headers={"Content-Type": "application/json"})