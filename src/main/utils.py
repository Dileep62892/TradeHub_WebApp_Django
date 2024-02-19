def user_listings_path(instance, filename):
    return 'user_{0}/listings/{1}'.format(instance.seller.user.id, filename)