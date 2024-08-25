from abc import ABC, abstractmethod

class UserView(ABC):
	@abstractmethod
	def display_massage(self, message):
		pass

	@abstractmethod
	def get_input(self, prompt):
		pass

	@abstractmethod
	def display_contacts(self, contacts):
		pass

	@abstractmethod
	def display_contact(self, contact):
		pass

	@abstractmethod
	def display_help(self):
		pass