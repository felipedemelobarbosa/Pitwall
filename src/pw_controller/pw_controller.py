import copy

from pw_controller import calander_page_controller, driver_hire_controller
from pw_model import pw_model, update_window_functions
from pw_view import view
from pw_controller import race_controller

class Controller:
	def __init__(self, app, run_directory, mode):
		self.app = app
		self.mode = mode
		roster = "1998_Roster"

		self.calendar_page_controller = calander_page_controller.CalendarPageController(self)
		self.driver_hire_controller = driver_hire_controller.PWDriverHireController(self)
		
		self.model = pw_model.Model(roster, run_directory)

		if self.mode in ["normal"]:
			self.view = view.View(self)
		else:
			self.view = None # running headless tests

		self.update_standings_page()
		self.update_staff_page()

		# if self.mode in ["normal"]:
		# 	self.view.setup_race_pages()

		self.setup_new_season()
		
		# self.update_main_window()
		

	def advance(self):
		self.model.advance()

		if self.mode != "headless":
			self.update_main_window()
			self.update_email_page()

		if self.model.season.current_week == 1:
			self.setup_new_season()

	def update_main_window(self):
		data = update_window_functions.get_main_window_data(self.model)
		self.view.main_window.update_window(data)
		# self.update_email_button()

	def setup_new_season(self):
		
		if self.mode != "headless":
			# Setup the calander page to show the races upcoming in the new season
			self.update_email_page()
			self.update_calendar_page()
			self.update_standings_page()
			self.update_home_page()
			self.update_grid_page()
			self.update_staff_page()
			self.update_main_window()
			self.race_controller = race_controller.RaceController(self)

	def update_home_page(self):
		data = {
			"next_race": self.model.season.next_race,
			"constructors_standings_df": self.model.season.standings_manager.constructors_standings_df.copy(deep=True)
		}
		self.view.home_page.update_page(data)

	def update_email_button(self):
		data = {"number_unread": self.model.inbox.number_unread}
		self.view.main_window.update_email_button(data)

	def update_standings_page(self):
		data = {
			"drivers_standings_df": self.model.season.standings_manager.drivers_standings_df.copy(deep=True),
			"constructors_standings_df": self.model.season.standings_manager.constructors_standings_df.copy(deep=True)
		}

		self.view.standings_page.update_standings(data)

	def update_staff_page(self):
		team_model = self.model.get_team_model(self.model.player_team)
		data = {
			"driver1": team_model.driver1,
			"driver1_age": team_model.driver1_model.age,
			"driver1_country": team_model.driver1_model.country,
			"driver1_speed": team_model.driver1_model.speed,
			"driver1_contract_length": team_model.driver1_model.contract.contract_length,
			"driver1_retiring": team_model.driver1_model.retiring,
			"player_requiring_driver1": self.model.driver_market.player_requiring_driver1,

			"driver2": team_model.driver2,
			"driver2_age": team_model.driver2_model.age,
			"driver2_country": team_model.driver2_model.country,
			"driver2_speed": team_model.driver2_model.speed,
			"driver2_contract_length": team_model.driver2_model.contract.contract_length,
			"driver2_retiring": team_model.driver2_model.retiring,
			"player_requiring_driver2": self.model.driver_market.player_requiring_driver2,
		}

		self.view.staff_page.update_page(copy.deepcopy(data))

	def update_car_page(self):
		car_speeds = {}
		for team in self.model.teams:
			car_speeds[team.name] = team.car_model.speed
		
		data = {
			"car_speeds": car_speeds
		}

		self.view.car_page.update_plot(data)

	def update_calendar_page(self):
		data = {
			"calendar": self.model.calendar.copy(deep=True)
		}

		self.view.calendar_page.update_page(data)

	def update_grid_page(self):
		data = {
			"year": self.model.year,
			"grid_this_year_df": self.model.driver_market.grid_this_year_df.copy(deep=True),
			"grid_next_year_df": self.model.driver_market.grid_next_year_df.copy(deep=True),
		}

		self.view.grid_page.update_page(data)
		self.view.grid_page.change_display(None)

	def update_email_page(self):
		data = {
			"emails": copy.deepcopy(self.model.inbox.emails),
		}
		self.view.email_page.update_page(data)

	def go_to_race_weekend(self):
		data = {
			"race_title": self.model.season.current_track_model.title
		}
		self.view.go_to_race_weekend(data)

	def return_to_main_window(self):
		'''
		Post race, remove race weekend, update advance button to allow progress to next week
		'''
		self.update_standings_page()
		# self.update_home_page()

		self.view.return_to_main_window()
		# self.view.main_window.update_advance_btn("advance")