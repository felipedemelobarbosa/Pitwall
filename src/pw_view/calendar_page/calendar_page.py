import flet as ft

class CalendarPage(ft.Column):
	def __init__(self, view):

		self.view = view

		self.header_text = ft.Text("Calendar", theme_style=self.view.page_header_style)
		contents = [
			self.header_text
		]

		super().__init__(controls=contents, alignment=ft.MainAxisAlignment.START)

	def update_page(self, data):
		calendar = data["calendar"]

		# Add a Round column based on index, maybe this should be added to the model

		calendar.insert(0, "#", calendar.index + 1)

		columns = []
		for col in calendar.columns:
			columns.append(ft.DataColumn(ft.Text(col)))

		data = calendar.values.tolist()
		rows = []

		for row in data:
			cells = []
			for cell in row:
				cells.append(ft.DataCell(ft.Text(cell)))

			rows.append(ft.DataRow(cells=cells))

		self.calendar_table = ft.DataTable(columns=columns, rows=rows, data_row_max_height=30, data_row_min_height=30)

		contents = [
			self.header_text,
			self.calendar_table
		]

		self.controls = contents
		self.view.main_app.update()
