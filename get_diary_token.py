import os
import msal


tenant_id = os.environ["ENTRA_TENANT_ID"]
client_id = os.environ["ENTRA_LOCAL_CLIENT_ID"]

authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = [
    f"api://{os.environ['ENTRA_API_CLIENT_ID']}/Diary.ReadWrite"
]

app = msal.PublicClientApplication(
    client_id=client_id,
    authority=authority,
)

result = app.acquire_token_interactive(scopes=scopes)


if "access_token" in result:
    print("Token acquisition successful.")
    print("Token type:", result.get("token_type", "unknown"))
    print("Expires in seconds:", result.get("expires_in", "unknown"))

    with open(".diary_access_token", "w", encoding="utf-8") as f:
        f.write(result["access_token"])

    print("Access token saved for local API testing.")
else:
    print("Token acquisition failed.")
    print("Error:", result.get("error", "unknown"))
    print("Description:", result.get("error_description", "No details"))
