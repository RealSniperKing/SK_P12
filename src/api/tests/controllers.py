from .models import Api
from accounts.models import ManagementGroupName


class ApiTest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

        self.api = Api(self.email, self.password)

    def assign_permissions_to_user(self, management_permissions, group_name):
        self.api.create_group_with_permissions(management_permissions)
        self.api.add_user_in_group(group_name)

    def launch_signin_signout(self):
        # Connection
        self.api.signin()

        # Logout
        self.api.signout()

    def set_management_group_name(self, group_name):
        management_group_name = ManagementGroupName.objects.all()

        if len(management_group_name) == 0:
            management_team = ManagementGroupName.objects.create(name=group_name)
            management_team.save()
        else:
            management_team = management_group_name.first()
            management_team.name = group_name
            management_team.save()
        # print("ManagementGroupName ==== ", ManagementGroupName.objects.all())

    def launch_user_crud_actions(self, view_name, crud_actions):
        """Test CRUD operations : create, read, update, delete"""
        # Connection
        self.api.signin()

        # GET
        self.api.view_get(f"api:{view_name}-list", crud_actions["read-list"])

        # POST
        new_user_email = "vente_2@test.fr"
        new_user_password = "pwTEST?_741."
        data = {"email": new_user_email, "password": new_user_password, "confirm_password": new_user_password}
        json_content = self.api.view_post(f"api:{view_name}-list", crud_actions["create"], data=data)
        user_id = json_content.get('user_id', "0")

        # GET DETAIL
        self.api.view_get(f"api:{view_name}-detail", crud_actions["read-detail"], user_id=user_id)

        # PUT
        new_user_password = "pwTEST?_741."
        data = {"email": new_user_email, "password": new_user_password, "confirm_password": new_user_password}
        self.api.view_put(f"api:{view_name}-detail", crud_actions["update"], data=data, user_id=user_id)

        # DELETE
        self.api.view_delete(f"api:{view_name}-detail", crud_actions["delete"], user_id=user_id)

        # Logout
        self.api.signout()

    def launch_customer_crud_actions(self, view_name, crud_actions):
        """Test CRUD operations : create, read, update, delete"""
        # Connection
        self.api.signin()

        # GET
        self.api.view_get(f"api:{view_name}-list", crud_actions["read-list"])

        # POST
        compagny_name = "company_1"
        compagny_email = "company@mail.fr"
        data = {"company_name": compagny_name, "email": compagny_email}
        json_content = self.api.view_post(f"api:{view_name}-list", crud_actions["create"], data=data)
        client_id = json_content.get('client_id', "0")

        # GET DETAIL
        self.api.view_get(f"api:{view_name}-detail", crud_actions["read-detail"], client_id=client_id)

        # PUT
        data = {"email": "company_edit@mail.fr"}
        self.api.view_put(f"api:{view_name}-detail", crud_actions["update"], data=data, client_id=client_id)

        # DELETE
        self.api.view_delete(f"api:{view_name}-detail", crud_actions["delete"], client_id=client_id)

        # Logout
        self.api.signout()

    def launch_contract_crud_actions(self, view_name, crud_actions):
        """Test CRUD operations : create, read, update, delete"""
        # Connection
        self.api.signin()

        # GET
        self.api.view_get(f"api:{view_name}-list", crud_actions["read-list"])

        # POST
        title = "contract1"
        data = {"title": title, "client": "", "contract_manager": ""}
        json_content = self.api.view_post(f"api:{view_name}-list", crud_actions["create"], data=data)
        contract_id = json_content.get('contract_id', "0")

        # GET DETAIL
        self.api.view_get(f"api:{view_name}-detail", crud_actions["read-detail"], contract_id=contract_id)

        # PUT
        data = {"title": "contract1_edit"}
        self.api.view_put(f"api:{view_name}-detail", crud_actions["update"], data=data, contract_id=contract_id)

        # DELETE
        self.api.view_delete(f"api:{view_name}-detail", crud_actions["delete"], contract_id=contract_id)

        # Logout
        self.api.signout()

    def launch_event_crud_actions(self, view_name, crud_actions):
        """Test CRUD operations : create, read, update, delete"""
        # Connection
        self.api.signin()

        # GET
        self.api.view_get(f"api:{view_name}-list", crud_actions["read-list"])

        # POST
        name = "Event_1"
        data = {"name": name, "contract": "", "event_manager": ""}
        json_content = self.api.view_post(f"api:{view_name}-list", crud_actions["create"], data=data)
        event_id = json_content.get('event_id', "0")

        # GET DETAIL
        self.api.view_get(f"api:{view_name}-detail", crud_actions["read-detail"], event_id=event_id)

        # PUT
        data = {"name": "Event_1_edit"}
        self.api.view_put(f"api:{view_name}-detail", crud_actions["update"], data=data, event_id=event_id)

        # DELETE
        self.api.view_delete(f"api:{view_name}-detail", crud_actions["delete"], event_id=event_id)

        # Logout
        self.api.signout()
