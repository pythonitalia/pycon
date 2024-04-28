def get_ip(request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(", ")[0]
    return request.META.get("REMOTE_ADDR")
