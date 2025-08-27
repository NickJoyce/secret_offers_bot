from typing import Optional
from starlette_admin.contrib.sqla import Admin as BaseAdmin
from fastapi import Request

class Admin(BaseAdmin):
    def custom_render_js(self, request: Request) -> Optional[str]:
        return request.url_for("static", path="js/custom_render.js")