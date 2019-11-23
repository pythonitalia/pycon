def force_pycon_host(get_response):
    def middleware(request):
        request.META["HTTP_HOST"] = "pycon.it"

        return get_response(request)

    return middleware
