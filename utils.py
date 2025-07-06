import uuid

def generate_collection_name(url):
    return f"site-{uuid.uuid5(uuid.NAMESPACE_URL, url)}"
