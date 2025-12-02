from pages.admin_users_page import AdminUsersPage
from utils import unique_username, EMPLOYEE_NAME


def test_search_existing_user(admin_users_page: AdminUsersPage):
    """
    1) Create a user
    2) Search by username
    3) Verify exactly one result appears with same username
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

    # Search
    admin_users_page.search_by_username(username)
    admin_users_page.assert_single_result_with_username(username)
