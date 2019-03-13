class Person:
      def __init__(self, name, school):
            self.name = name
            self.school = school
            self.reps = []
            self.contacts = []
            self.num = 0
      def __str__(self):
            return self.name + " who goes to " + self.school + " and has " + str(len(self.reps)) + " logs"
      def __lt__(self, other):
            print("in lt")
            return len(self.reps) < len(other.reps)
      def log(self, rep, contact):
            self.reps.append(rep)
            self.contacts.append(contact)
            self.num += 1