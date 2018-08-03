from enum import Enum, unique

@unique
class QuestionType(Enum):
	MULTI = 1
	SINGLE = 2
	YESNO = 3
	SHORT = 4
	LONG = 5

@unique
class QuestionOrigin(Enum):
	CSV = 1
	APP = 2
	OTHERS = 3 

@unique
class QuestionLevel(Enum):
	EASY = 1
	MEDIUM = 2
	DIFFICULT = 3

