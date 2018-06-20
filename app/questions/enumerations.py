from enum import Enum, unique

@unique
class QuestionType(Enum):
	MCQ = 1
	SUBJECTIVE = 2

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

