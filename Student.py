from SituationEnum import Situation;

class Student:
    TotalAllowedAbsences = 60

    def __init__(self, registration, name, absences, p1, p2, p3):
        self.Registration = registration
        self.Name = name
        self.Absences = absences
        self.P1 = p1
        self.P2 = p2
        self.P3 = p3
        self.Mean = (float(p1) + float(p2) + float(p3)) / 3
        self.NAF = 0
        self.Situation = None
    def __str__(self):
        return (
            f"Registration: {self.Registration}, Name: {self.Name}, Absences: {self.Absences}, "
            f"P1: {self.P1}, P2: {self.P2}, P3: {self.P3}, Mean: {self.Mean}, "
            f"Situation: {self.Situation} NAF: {self.NAF} "
        )

    def calculate_situation(self):
        if self.Absences > (self.TotalAllowedAbsences * 0.25):
            self.Situation = Situation.FailedByAbsences
        else:
            if self.Mean < 50:
                self.Situation = Situation.FailedByGrade
            elif 50 <= self.Mean < 70:
                self.Situation = Situation.FinalExam
            elif self.Mean >= 70:
                self.Situation = Situation.Approved

    def verify_situation(self):
        if self.Situation == Situation.FinalExam:
            naf = round(100 - self.Mean)
            self.NAF = naf
        else:
            self.NAF = 0