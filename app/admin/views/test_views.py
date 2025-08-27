from starlette_admin.contrib.sqla import ModelView
from fastapi import Request

# Add views
class TestView(ModelView):
    fields = ["id", "datetime", "str_field"]

    # def is_accessible(self, request: Request) -> bool:
    #     return "admin" in request.state.user["roles"]
    