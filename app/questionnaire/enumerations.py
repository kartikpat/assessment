from enum import Enum, unique

@unique
class AuthorType(Enum):
	ADMIN = 1
	RECRUITER = 2

@unique
class QuestionnaireStatus(Enum):
	ACTIVE = 1
	SAVED = 2
	INACTIVE = 3
	DELETED = 4
	FLAGGED = 5

