from playwright.sync_api import Page, expect


class AdminUsersPage:
    """
    Page Object for:
    Admin -> User Management -> Users (System Users)
    """

    def __init__(self, page: Page):
        self.page = page

    # -------------------------------------------------------------------------
    # NAVIGATION
    # -------------------------------------------------------------------------
    def goto_admin_users(self):
        """Click the Admin menu and ensure System Users page is visible."""
        self.page.get_by_role("link", name="Admin").click()
        heading = self.page.get_by_role("heading", name="System Users")
        expect(heading).to_be_visible(timeout=15000)

    # -------------------------------------------------------------------------
    # GENERIC HELPERS
    # -------------------------------------------------------------------------
    def _input_group(self, label_text: str):
        """
        Returns the .oxd-input-group that contains the label with given text.
        Uses .first to avoid strict-mode issues when more than one matches.
        """
        group = self.page.locator("div.oxd-input-group").filter(
            has=self.page.locator("label").filter(has_text=label_text)
        ).first
        expect(group).to_be_visible(timeout=10000)
        return group

    def _input_by_label(self, label_text: str):
        """
        Find the <input> inside the .oxd-input-group for the given label.
        """
        group = self._input_group(label_text)
        input_el = group.locator("input").first
        expect(input_el).to_be_visible(timeout=10000)
        return input_el

    def _select_dropdown_option(self, label_text: str, option_text: str):
        """
        For dropdowns like User Role, Status etc, select an option by visible text.
        """
        group = self._input_group(label_text)
        dropdown = group.locator("div.oxd-select-text").first

        dropdown.click()
        listbox = self.page.locator("div[role='listbox']")
        option = listbox.get_by_text(option_text, exact=True).first
        expect(option).to_be_visible(timeout=10000)
        option.click()

    def _select_first_employee_suggestion(self, employee_name: str):
        """
        Type into Employee Name field, wait for suggestions, pick the first option.
        """
        group = self._input_group("Employee Name")
        emp_input = group.locator("input").first

        emp_input.click()
        emp_input.fill("")

        # Type slowly so suggestions appear
        emp_input.type(employee_name, delay=80)

        # Give time for dropdown (independent of global --slowmo)
        self.page.wait_for_timeout(1000)

        listbox = self.page.locator("div[role='listbox']")
        # Prefer exact text if available, else first option
        exact_option = listbox.get_by_text(employee_name, exact=True).first
        if exact_option.count() > 0:
            option = exact_option
        else:
            option = listbox.locator(".oxd-autocomplete-option").first

        expect(option).to_be_visible(timeout=10000)
        option.click()
        self.page.wait_for_timeout(500)

    # -------------------------------------------------------------------------
    # ACTIONS: ADD / EDIT / SAVE
    # -------------------------------------------------------------------------
    def click_add_user(self):
        self.page.get_by_role("button", name="Add").click()
        heading = self.page.get_by_role("heading", name="Add User")
        expect(heading).to_be_visible(timeout=10000)

    def fill_add_user_form(
        self,
        employee_name: str,
        username: str,
        password: str,
        user_role: str,
        status: str,
    ):
        """
        Fill the Add User form:
        - User Role dropdown
        - Employee Name autocomplete (select first suggestion)
        - Status dropdown
        - Username / Password / Confirm Password
        """

        # ---- DROPDOWNS ----
        self._select_dropdown_option("User Role", user_role)
        self._select_first_employee_suggestion(employee_name)
        self._select_dropdown_option("Status", status)

        # ---- USERNAME ----
        username_input = self._input_by_label("Username")
        username_input.click()
        username_input.fill("")
        username_input.type(username, delay=40)

        # ---- PASSWORD ----
        pwd_input = self._input_by_label("Password")
        pwd_input.click()
        pwd_input.fill("")
        pwd_input.type(password, delay=40)

        # ---- CONFIRM PASSWORD ----
        confirm_input = self._input_by_label("Confirm Password")
        confirm_input.click()
        confirm_input.fill("")
        confirm_input.type(password, delay=40)

    def save_user(self):
        """
        Click Save and wait for:
        - optional 'Successfully ...' toast
        - navigation back to System Users table
        """
        self.page.get_by_role("button", name="Save").click()

        # Try to catch any "Successfully Saved/Updated/Deleted" style toast,
        # but DO NOT fail the test if it's not visible.
        try:
            toast = self.page.get_by_text("Successfully").first
            expect(toast).to_be_visible(timeout=8000)
        except AssertionError:
            # Toast can be flaky / too quick; rely on navigation instead
            pass

        # Real assertion: we are back on System Users page
        heading = self.page.get_by_role("heading", name="System Users")
        expect(heading).to_be_visible(timeout=15000)

    # -------------------------------------------------------------------------
    # SEARCH + TABLE HELPERS
    # -------------------------------------------------------------------------
    def search_by_username(self, username: str):
        """
        Search for a user by username in the System Users page.
        """
        heading = self.page.get_by_role("heading", name="System Users")
        expect(heading).to_be_visible(timeout=15000)

        username_input = self._input_by_label("Username")
        username_input.click()
        username_input.fill("")
        username_input.type(username, delay=40)

        self.page.get_by_role("button", name="Search").click()

        # IMPORTANT:
        # Do NOT assert body visibility here because Playwright
        # reports it as 'hidden' sometimes. Just give it time.
        self.page.wait_for_timeout(1000)

    def get_results_rows(self):
        body = self.page.locator("div.oxd-table-body")
        return body.locator("div.oxd-table-card")

    def assert_single_result_with_username(self, username: str):
        rows = self.get_results_rows()
        expect(rows).to_have_count(1, timeout=10000)

        row = rows.first
        username_cell = row.locator("div.oxd-table-cell").nth(1)
        expect(username_cell).to_have_text(username)

    def assert_no_results(self):
        """
        Assert that effectively there are no records:
        - Prefer 'No Records Found' row
        - Fallback to '0 table cards'
        """
        body = self.page.locator("div.oxd-table-body")

        # Let table update
        self.page.wait_for_timeout(500)

        msg = body.get_by_text("No Records Found")
        try:
            expect(msg).to_be_visible(timeout=10000)
            return
        except AssertionError:
            # Fallback: check there are 0 data rows
            rows = body.locator("div.oxd-table-card")
            expect(rows).to_have_count(0, timeout=5000)

    # -------------------------------------------------------------------------
    # EDIT USER
    # -------------------------------------------------------------------------
    def open_user_for_edit(self, username: str):
        """
        Search by username and click the EDIT icon to open Edit User page.
        """
        self.search_by_username(username)
        self.assert_single_result_with_username(username)

        rows = self.get_results_rows()
        row = rows.first

        # Last cell contains action buttons [delete, edit]
        last_cell = row.locator("div.oxd-table-cell").last
        edit_button = last_cell.get_by_role("button").nth(1)  # 2nd button = Edit
        edit_button.click()

        heading = self.page.get_by_role("heading", name="Edit User")
        expect(heading).to_be_visible(timeout=15000)

    def change_status_and_save(self, new_status: str):
        """
        On Edit User page: change Status dropdown and save.
        """
        self._select_dropdown_option("Status", new_status)
        self.save_user()

    # -------------------------------------------------------------------------
    # DELETE USER
    # -------------------------------------------------------------------------
    def delete_user(self, username: str):
        """
        Delete user with given username and verify it is gone.
        """
        # Search and ensure single row
        self.search_by_username(username)
        rows = self.get_results_rows()
        expect(rows).to_have_count(1, timeout=10000)
        row = rows.first

        # Last column -> first button is delete
        last_cell = row.locator("div.oxd-table-cell").last
        delete_button = last_cell.get_by_role("button").first
        delete_button.click()

        # Confirm dialog
        dialog = self.page.locator("div.orangehrm-dialog-popup")
        expect(dialog).to_be_visible(timeout=10000)
        dialog.get_by_role("button", name="Yes, Delete").click()

        # Optional toast
        try:
            toast = self.page.get_by_text("Successfully").first
            expect(toast).to_be_visible(timeout=8000)
        except AssertionError:
            pass

        # Re-search and validate no results
        self.search_by_username(username)
        self.assert_no_results()
