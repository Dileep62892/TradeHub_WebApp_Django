import uuid


def user_listings_path(instance, filename):
    ext = filename.split(".")[-1]
    return f"user_{instance.seller.user.id}/listings/{uuid.uuid4()}.{ext}"
