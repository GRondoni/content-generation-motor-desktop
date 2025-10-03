import os
import requests

def publish_to_wordpress(title: str, html_content: str, status: str = "draft"):
    wp_url = os.getenv("WP_URL", "").rstrip("/")
    wp_user = os.getenv("WP_USER", "")
    wp_app_password = os.getenv("WP_APP_PASSWORD", "")
    status = os.getenv("WP_STATUS", status)

    if not (wp_url and wp_user and wp_app_password):
        print("[WP] Variáveis não configuradas. Pulando publicação.")
        return None

    endpoint = f"{wp_url}/wp-json/wp/v2/posts"
    auth = (wp_user, wp_app_password)
    data = {
        "title": title,
        "content": html_content,
        "status": status
    }
    resp = requests.post(endpoint, auth=auth, json=data, timeout=60)
    if resp.status_code >= 200 and resp.status_code < 300:
        post = resp.json()
        print(f"[WP] Post criado: {post.get('id')} | {post.get('link')}")
        return post
    else:
        print(f"[WP] Erro {resp.status_code}: {resp.text[:300]}")
        return None
