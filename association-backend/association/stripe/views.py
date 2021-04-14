from starlette.endpoints import HTTPEndpoint
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="association/stripe/templates")


class PaymentView(HTTPEndpoint):
    async def get(self, request):
        return templates.TemplateResponse("index.html", {"request": request})
