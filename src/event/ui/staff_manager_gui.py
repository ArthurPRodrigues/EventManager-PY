import FreeSimpleGUI as sg

from event.application.list_staffs_with_email_and_name_use_case import (
    ListStaffsInputDto,
)
from shared.ui.base_gui import BaseGUI
from shared.ui.components.action_buttons_component import ActionButtonsComponent
from shared.ui.components.header_component import HeaderComponent
from shared.ui.components.table_component import TableComponent
from shared.ui.styles import BUTTON_SIZES, COLORS, WINDOW_SIZES
from user.domain.user_role import UserRole


class StaffManagerGUI(BaseGUI):
    def __init__(
        self, use_cases=None, navigator=None, auth_context=None, event_id=None
    ):
        super().__init__(
            title="Staff Management",
            size=WINDOW_SIZES["HORIZONTAL_DEFAULT"],
            use_cases=use_cases,
            navigator=navigator,
            auth_context=auth_context,
        )
        self.event_id = event_id

        self.header = HeaderComponent()

        self.table = TableComponent(
            headers=["ID", "NAME", "EMAIL"],
            data_callback=self._load_staffs_callback,
            key="-STAFF_TABLE-",
            items_per_page=10,
            has_hidden_id_column=True,
        )

        self.action_buttons = ActionButtonsComponent([
            {
                "text": "Add Staff",
                "key": "-ADD_STAFF-",
                "size": BUTTON_SIZES["MEDIUM"],
                "button_color": (COLORS["white"], COLORS["success"]),
            },
            {
                "text": "Disassociate Selected",
                "key": "-REMOVE_STAFF-",
                "size": BUTTON_SIZES["LARGE"],
                "button_color": (COLORS["white"], COLORS["warning"]),
            },
        ])

        self.event_map = {
            "-ADD_STAFF-": self.handle_add_staff,
            "-REMOVE_STAFF-": self.handle_remove_staff,
        }

    def handle_events(self, event, values):
        handler = self.event_map.get(event)
        if handler:
            handler(values)

    def handle_add_staff(self, values):
        input_values = sg.Window(
            "Add Staff",
            [
                [sg.Text("Staff Email:")],
                [sg.Input(key="-EMAIL-")],
                [sg.Button("Add"), sg.Button("Cancel")],
            ],
            modal=True,
            keep_on_top=True,
        ).read(close=True)

        if input_values[0] == "Add" and input_values[1]["-EMAIL-"]:
            email = input_values[1]["-EMAIL-"]
            try:
                staff = self.use_cases.user_repo.get_by_email_and_role(
                    email, UserRole.STAFF
                )
                if not staff:
                    self.show_error_popup(f"No staff found with email: {email}")
                    return

                event = self.use_cases.event_repo.get_by_id(self.event_id)
                if not event:
                    self.show_error_popup("Event not found")
                    return

                updated_event = event.add_staff(str(staff.id))
                self.use_cases.event_repo.update(updated_event)

                self.show_success_popup(f"Staff {staff.name} added successfully!")
                self.table.refresh(self.window)
            except Exception as e:
                self.show_error_popup(f"Error adding staff: {e}")

    def handle_remove_staff(self, values):
        selected_row = self.table.get_selected_row_data(self.window)
        if not selected_row:
            self.show_error_popup("Please select a staff member to remove")
            return

        if (
            sg.popup_yes_no("Are you sure you want to remove this staff member?")
            == "Yes"
        ):
            try:
                staff_id = selected_row[0]

                event = self.use_cases.event_repo.find_by_id(self.event_id)
                if not event:
                    self.show_error_popup("Event not found")
                    return

                updated_event = event.remove_staff(str(staff_id))
                self.use_cases.event_repo.update(updated_event)

                self.show_success_popup("Staff removed successfully!")
                self.table.refresh(self.window)
            except Exception as e:
                self.show_error_popup(f"Error removing staff: {e}")

    def create_layout(self):
        layout = [
            *self.header.create_layout(),
            *self.table.create_layout(),
            *self.action_buttons.create_layout(),
        ]
        return layout

    def _load_staffs_callback(self, page: int, items_per_page: int):
        try:
            input_dto = ListStaffsInputDto(
                page=page, size=items_per_page, event_id=self.event_id
            )

            staffs = self.use_cases.list_staffs_use_case.execute(input_dto)

            if not staffs:
                return {"data": [], "total": 0}

            table_data = [
                [staff.id, staff.name, staff.email] for staff in staffs.staff_list
            ]

            return {"data": table_data, "total": staffs.total_staffs_count}
        except Exception as e:
            self.show_error_popup(f"Error loading staff: {e}")
            return {"data": [], "total": 0}
