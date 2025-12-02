from pages.admin_users_page import AdminUsersPage


def test_search_invalid_user(admin_users_page: AdminUsersPage):
    """
    1) Search with a username that does NOT exist
    2) Verify 'No Records Found'
    """
    invalid_username = "this_user_should_not_exist_12345"

    admin_users_page.search_by_username(invalid_username)
    admin_users_page.assert_no_results()
