import collections
from datetime import datetime, timedelta

def calculate_prize_money(finishing_position):
	'''
	finishing position should be zero indexed
	'''

	prize_money =  [
		33_000_000,
		31_000_000,
		27_000_000,
		23_000_000,
		13_000_000,
		11_000_000,
		9_000_000,
		7_000_000,
		5_000_000,
		3_000_000,
		1_000_000,
	]
	
	return prize_money[finishing_position]

class FinanceModel:
	def __init__(self, model, team_model, opening_balance, total_sponsorship):
		self.model = model
		self.team_model = team_model
		self.balance = opening_balance

		self.staff_yearly_cost = 28_000

		self.prize_money = 13_000_000
		self.total_sponsorship = total_sponsorship

		self.balance_history = collections.deque(maxlen=130) # 130 weeks (2.5 years) in length
		self.balance_history_dates = collections.deque(maxlen=130)

	@property
	def total_staff_costs_per_year(self):
		return self.staff_yearly_cost * self.team_model.number_of_staff
	
	def weekly_update(self):
		
		# add prize money
		self.balance += int(self.prize_money / 52)

		# add sponsorship
		self.balance += int(self.total_sponsorship / 52)

		# staff cost
		self.balance -= int((self.staff_yearly_cost / 52) * self.team_model.number_of_staff)

		# Drivers cost
		self.balance -= int(self.team_model.driver1_model.contract.salary / 52)
		self.balance -= int(self.team_model.driver2_model.contract.salary / 52)

		self.update_balance_history()
		
	def apply_race_costs(self, race_cost=500_000):
		self.balance -= race_cost
	
	def update_balance_history(self):
		self.balance_history.append(self.balance)
		self.balance_history_dates.append(datetime(self.model.year, 1, 1) + timedelta(weeks=self.model.season.current_week - 1))

	def update_prize_money(self, finishing_position):
		self.prize_money = calculate_prize_money(finishing_position)

		self.model.inbox.new_prize_money_email(self.prize_money)
