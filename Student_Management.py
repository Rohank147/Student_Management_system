import json
import os


# =========================
# Student Class
# =========================
class Student:
    def __init__(self, student_id, name, grade):
        """
        Constructor for Student class
        """
        self.id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        """
        Convert Student object to dictionary (for JSON saving)
        """
        return {
            "id": self.id,
            "name": self.name,
            "grade": self.grade
        }

    @staticmethod
    def from_dict(data):
        """
        Create Student object from dictionary
        """
        return Student(data["id"], data["name"], data["grade"])


# =========================
# Student Manager Class
# =========================
class StudentManager:
    def __init__(self, filename="students.json"):
        """
        Constructor loads students from file
        """
        self.filename = filename
        self.students = []
        self.load_students()

    def load_students(self):
        """
        Load students from JSON file
        """
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                try:
                    data = json.load(file)
                    self.students = [Student.from_dict(s) for s in data]
                except json.JSONDecodeError:
                    self.students = []
        else:
            self.students = []

    def save_students(self):
        """
        Save students to JSON file
        """
        with open(self.filename, "w") as file:
            json.dump([s.to_dict() for s in self.students], file, indent=4)

    def add_student(self, student_id, name, grade):
        """
        Add new student (ID must be unique)
        """
        if any(s.id == student_id for s in self.students):
            print("Error: Student ID must be unique.")
            return

        new_student = Student(student_id, name, grade)
        self.students.append(new_student)
        self.save_students()
        print("Student added successfully.")

    def update_student(self, student_id, name=None, grade=None):
        """
        Update existing student
        """
        for student in self.students:
            if student.id == student_id:
                if name:
                    student.name = name
                if grade:
                    student.grade = grade
                self.save_students()
                print("Student updated successfully.")
                return

        print("Student not found.")

    def delete_student(self, student_id):
        """
        Delete student by ID
        """
        for student in self.students:
            if student.id == student_id:
                self.students.remove(student)
                self.save_students()
                print("Student deleted successfully.")
                return

        print("Student not found.")

    def list_students(self):
        """
        Display all students in formatted table
        """
        if not self.students:
            print("No students found.")
            return

        print("\n" + "=" * 40)
        print(f"{'ID':<10}{'Name':<15}{'Grade':<10}")
        print("=" * 40)

        for student in self.students:
            print(f"{student.id:<10}{student.name:<15}{student.grade:<10}")

        print("=" * 40 + "\n")


# =========================
# CLI Menu
# =========================
def main():
    manager = StudentManager()

    while True:
        print("===== Student Management System =====")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. List Students")
        print("5. Exit")

        choice = input("Enter choice (1-5): ")

        if choice == "1":
            student_id = input("Enter Student ID: ")
            name = input("Enter Name: ")
            grade = input("Enter Grade: ")
            manager.add_student(student_id, name, grade)

        elif choice == "2":
            student_id = input("Enter Student ID to update: ")
            name = input("Enter New Name (leave blank to skip): ")
            grade = input("Enter New Grade (leave blank to skip): ")

            name = name if name.strip() != "" else None
            grade = grade if grade.strip() != "" else None

            manager.update_student(student_id, name, grade)

        elif choice == "3":
            student_id = input("Enter Student ID to delete: ")
            manager.delete_student(student_id)

        elif choice == "4":
            manager.list_students()

        elif choice == "5":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
