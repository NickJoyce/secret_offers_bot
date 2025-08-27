from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed
import logging.config
from app.admin.auth.models import User
from sqlalchemy import select
from app.database.conn import AsyncSessionLocal
from app.admin.auth.utils import validate_password

logger = logging.getLogger(__name__)



class MyAuthProvider(AuthProvider):
    """"""
    async def get_user_by_email(self, email: str):
        """Получить пользователя по email - оптимизированная версия"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).filter(User.email == email))
            return result.scalar_one_or_none()

    async def get_users(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User))
            return result.scalars().all()


    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        """username = Superuser().email"""
        if len(username) < 3:
            """Form data validation"""
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )
        
        # Оптимизация: ищем пользователя напрямую по email
        user = await self.get_user_by_email(username)
        
        # check username
        if user and user.is_active and validate_password(password, user.hashed_password):
            """Save `username` in session"""
            request.session.update({"username": user.email})
            logger.info(f"logged in:  [{user.id}] {user.email}")
            return response
        raise LoginFailed("Invalid username or password")


    async def is_authenticated(self, request) -> bool:
        username = request.session.get("username", None)
        if not username:
            return False
            
        # Оптимизация: ищем пользователя напрямую по email
        user = await self.get_user_by_email(username)
        if user and user.is_active:
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
            request.state.user = user.config
            return True
        return False


    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user  # Retrieve current user
        # Update logo url according to current_user
        custom_logo_url = None
        if user.get("company_logo_url", None):
            custom_logo_url = request.url_for("static", path=user["company_logo_url"])
        return AdminConfig(
            logo_url=custom_logo_url,
        )


    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        photo_url = None
        if user["avatar"] is not None:
            photo_url = request.url_for("static", path=user["avatar"])
        return AdminUser(username=user["name"], photo_url=photo_url)


    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response


# example register data
# users = {
#     'admin': {
#         "name": "admin",
#         "avatar": "admin/avatar.jpeg",
#         "company_logo_url": None,
#         "roles": ["read", "create", "edit", "delete", "action_make_published"],
#     },
#     "viewer": {"name": "Viewer",
#                "avatar": None,
#                "roles": ["read"]},
# }