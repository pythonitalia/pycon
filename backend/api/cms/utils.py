from wagtail.models import Site


def get_site_by_host(hostname: str) -> Site | None:
    hostname, port = hostname.split(":") if ":" in hostname else (hostname, 80)
    return Site.objects.filter(hostname=hostname, port=port).first()
