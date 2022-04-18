from rest_framework import views, response, exceptions

from djadmin.base.flow import Flow
from djadmin.base.models import Accounts
from djadmin.api.serializers import AccountSerializer, AccountRegisterSerializer, AccountExtendedSerializer


flow = Flow()


class AccountView(views.APIView):
    @staticmethod
    def get(request):
        """Retrieve a list of accounts."""
        data = Accounts.objects.get_all_from_flow()
        if not data:
            raise exceptions.server_error(request=request)
        serialized_data = AccountSerializer(instance=data, many=True)
        return response.Response(serialized_data.data)

    @staticmethod
    def post(request):
        """Create a new account."""
        data = Accounts.objects.add_on_flow()
        if not data:
            raise exceptions.server_error(request=request)
        serialized_data = AccountRegisterSerializer(instance=data, many=False)
        return response.Response(serialized_data.data)


class AccountExtendedView(views.APIView):
    @staticmethod
    def get(request, address):
        """Retrieve single account by address."""
        data = Accounts.objects.get_one_from_flow(address=address)
        if not data:
            raise exceptions.NotFound(detail=f"Address is not found: {address}")
        serialized_data = AccountExtendedSerializer(instance=data, many=False)
        return response.Response(serialized_data.data)
