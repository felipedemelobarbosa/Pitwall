
import flet as ft

from pw_view import main_window, home_page, email_page, standings_page, grid_page
from pw_view.race_weekend import race_weekend_window, results_window
from pw_view.calendar_page import calendar_page
from pw_view.staff_page import staff_page, hire_driver_page

class View:
	def __init__(self, controller):
		self.controller = controller

		self.main_app = self.controller.app

		self.page_header_style = ft.TextThemeStyle.DISPLAY_MEDIUM
		self.header2_style = ft.TextThemeStyle.DISPLAY_SMALL
		
		self.header3_style = ft.TextThemeStyle.LABEL_MEDIUM

		self.dark_grey = "#23232A"

		self.vscroll_buffer = 100
		
		self.setup_pages()
		self.setup_windows()

		self.main_app.views.append(self.main_window)

	def setup_pages(self):
		self.home_page = home_page.HomePage(self)
		self.email_page = email_page.EmailPage(self)
		self.standings_page = standings_page.StandingsPage(self)
		self.calendar_page = calendar_page.CalendarPage(self)
		self.staff_page = staff_page.StaffPage(self)
		self.hire_driver_page = hire_driver_page.HireDriverPage(self)
		self.grid_page = grid_page.GridPage(self)

		self.results_window = results_window.ResultsWindow(self)

	def setup_windows(self):
		self.main_window = main_window.MainWindow(self)

	def go_to_race_weekend(self, data):

		self.race_weekend_window = race_weekend_window.RaceWeekendWindow(self, data)
		self.main_app.views.append(self.race_weekend_window)

		self.main_app.update()

	def show_simulated_session_results(self):
		self.results_window.continue_btn.disabled = True
		self.main_app.views.append(self.results_window)

		self.main_app.update()
		self.results_window.continue_btn.disabled = False
		self.main_app.update() # update again, this is to avoid a problem where the continue button on the results page would not work if the user clicked on it too quickly (on_click not fully assigned by flet?????)

	def return_to_main_window(self):
		self.main_app.views.clear()
		self.main_app.views.append(self.main_window)

		self.main_window.nav_sidebar.update_advance_button("advance")

		self.main_app.update()