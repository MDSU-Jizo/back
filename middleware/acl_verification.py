"""
    Middleware used to verify user's role on request
"""
import logging
import re

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from contract.constants import Constants
from service.api_response import send_json_response as api_response
from role_aclBundle.models import RoleAclBundle
from aclBundle.models import AclBundle, get_acl_bundle_with_routes

logger = logging.getLogger(__name__)

FORBIDDEN = Constants.HttpResponseCodes.FORBIDDEN
_EXCLUDED_PATHS = Constants.EXCLUDED_PATHS


class AclVerificationMiddleware(MiddlewareMixin):
    def process_request(self, request) -> JsonResponse | None:
        if self.verify_path(request.path):
            return None

        if self.verify_user_acl(request.path, request.role):
            return None

        response = api_response(
            code=FORBIDDEN,
            result='error',
            message="You don't have the right access.",
            user=request.email,
            url=request.path
        )

        return response

    @staticmethod
    def verify_path(path) -> bool:
        for pattern in _EXCLUDED_PATHS:
            if re.match(pattern, path):
                return True
        return False

    @staticmethod
    def verify_user_acl(path, role) -> bool:
        try:
            role_bundle = RoleAclBundle.objects.filter(role=role['id']).values()
            bundle_id = None

            for data in role_bundle:
                bundle_id = data['acl_bundle_id']

            bundle = get_acl_bundle_with_routes(bundle_id)

            for data in bundle:
                routes = data.routes

            for pattern in routes:
                if re.match(pattern, path):
                    return True
        except RoleAclBundle.DoesNotExist:
            return False

        return False
