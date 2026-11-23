import boto3, json

client = boto3.client("bedrock-runtime", region_name="us-east-1")
response = client.invoke_model(
    modelId="amazon.nova-micro-v1:0",
    body=json.dumps({
        "messages": [{"role": "user", "content": [{"type": "text", "text": "Hello!"}]}]
    }),
    contentType="application/json",
    accept="application/json"
)
result = json.loads(response["body"].read())

