from pages.admin_users_page import AdminUsersPage
from utils import unique_username, EMPLOYEE_NAME


def test_delete_user(admin_users_page: AdminUsersPage):
    """
    1) Create a user
    2) Search and verify it exists
    3) Delete the user
    4) Search again and verify 'No Records Found'
    """
    username = unique_username()

    # Create user
    admin_users_page.click_add_user()
    admin_users_page.fill_add_user_form(
        employee_name=EMPLOYEE_NAME,
        username=username,
        password="P@ssword123",
        user_role="ESS",
        status="Enabled",
    )
    admin_users_page.save_user()

    # Ensure it's there
    admin_users_page.search_by_username(username)
    admin_users_page.assert_single_result_with_username(username)

    # Delete
    admin_users_page.delete_user(username)
