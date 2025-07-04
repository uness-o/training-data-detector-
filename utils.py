def list_available_models():
    if not OPENAI_API_KEY:
        print("No API key found")
        return
    client.api_key = OPENAI_API_KEY
    resp = client.models.list()      # for the newest `openai` client, or openai.Model.list() otherwise
    for m in resp.data:
        print(m.id)

if __name__ == "__main__":
    list_available_models()
