from enum import Enum

class Situation(Enum):
    FailedByAbsences = 1
    FailedByGrade = 2
    FinalExam = 3
    Approved = 4