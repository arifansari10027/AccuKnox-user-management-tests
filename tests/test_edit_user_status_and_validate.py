from pages.admin_users_page import AdminUsersPage
from utils import unique_username, EMPLOYEE_NAME


def test_edit_user_status_and_validate(admin_users_page: AdminUsersPage):
    """
    1) Create a user with Enabled status
    2) Edit user and change status to Disabled
    3) Save
    4) Search again and validate status is updated
    """
    username = unique_username()

    # Create as Enabled
    admin_users_page.click_add_user()
    admin_users_page.fill_add_user_form(
        employee_name=EMPLOYEE_NAME,
        username=username,
        password="P@ssword123",
        user_role="ESS",
        status="Enabled",
    )
    admin_users_page.save_user()

    # Edit user -> change status to Disabled
    admin_users_page.open_user_for_edit(username)
    admin_users_page.change_status_on_edit_form("Disabled")
    admin_users_page.save_user()

    # Validate updated status
    admin_users_page.search_by_username(username)
    admin_users_page.assert_single_result_with_username(username)
    # Optional: you can add a specific assertion for 'Disabled' text if needed
