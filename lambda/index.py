# lambda/index.py
import json
import urllib.request

def lambda_handler(event, context):
    try:
        # リクエストボディの取得と解析
        body = json.loads(event['body'])
        user_message = body['message']

        # Colab上のFastAPIのURL（ご自身の ngrok URL に置き換えてください）
        url = "https://26dd-34-80-1-154.ngrok-free.app/chat"
        data = json.dumps({"message": user_message}).encode("utf-8")

        req = urllib.request.Request(
            url=url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req) as res:
            response_body = json.loads(res.read())

        assistant_response = response_body['reply']

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
                "conversationHistory": [
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": assistant_response}
                ]
            })
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": False,
                "error": str(e)
            })
        }
