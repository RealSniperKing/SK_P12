from .models import Api


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

    def launch_user_crud_actions(self, view_name, crud_actions):
        """Test CRUD operations : create, read, update, delete"""
        # Connection
        self.api.signin()

        # GET
        self.api.view_get(f"api:{view_name}-list", crud_actions["read"])

        # POST
        new_user_email = "vente_2@test.fr"
        new_user_password = "abcdef"
        data = {"email": new_user_email, "password": new_user_password, "confirm_password": new_user_password}
        json_content = self.api.view_post(f"api:{view_name}-list", crud_actions["create"], data=data)
        user_id = json_content.get('user_id', "0")

        # GET DETAIL
        self.api.view_get(f"api:{view_name}-detail", crud_actions["read"], user_id=user_id)

        # PUT
        new_user_password = "123456"
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
        self.api.view_get(f"api:{view_name}-list", crud_actions["read"])

        # # POST
        compagny_name = "company_1"
        compagny_email = "company@mail.fr"
        data = {"company_name": compagny_name, "email": compagny_email}
        json_content = self.api.view_post(f"api:{view_name}-list", crud_actions["create"], data=data)
        client_id = json_content.get('client_id', "0")

        # GET DETAIL
        self.api.view_get(f"api:{view_name}-detail", crud_actions["read"], client_id=client_id)

        # PUT
        data = {"email": "company_edit@mail.fr"}
        self.api.view_put(f"api:{view_name}-detail", crud_actions["update"], data=data, client_id=client_id)

        # # DELETE
        # self.api.view_delete(f"api:{view_name}-detail", crud_actions["delete"], user_id=user_id)

        # Logout
        self.api.signout()