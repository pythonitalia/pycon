def get_image_url_from_request(request, image):
    if not image:
        return None

    return request.build_absolute_uri(image.url)
