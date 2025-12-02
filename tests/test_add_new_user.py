from pages.admin_users_page import AdminUsersPage
from utils import unique_username, EMPLOYEE_NAME


def test_add_new_user(admin_users_page: AdminUsersPage):
    """
    1) Add new user
    2) Search the user
    3) Verify it exists
    """
    username = unique_username()

    # ---- CREATE ----
    admin_users_page.click_add_user()
    admin_users_page.fill_add_user_form(
        employee_name=EMPLOYEE_NAME,
        username=username,
        password="P@ssword123",
        user_role="ESS",
        status="Enabled",
    )
    admin_users_page.save_user()

    # ---- VERIFY ----
    admin_users_page.search_by_username(username)
    admin_users_page.assert_single_result_with_username(username)
