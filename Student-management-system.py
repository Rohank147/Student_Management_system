import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os


# -------------------------------
# Student Class
# -------------------------------
class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "grade": self.grade
        }


# -------------------------------
# Student Manager Class
# -------------------------------
class StudentManager:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = []
        self.load_students()

    def load_students(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)
                for item in data:
                    self.students.append(
                        Student(
                            item["student_id"],
                            item["name"],
                            item["grade"]
                        )
                    )

    def save_students(self):
        with open(self.filename, "w") as file:
            json.dump(
                [student.to_dict() for student in self.students],
                file,
                indent=4
            )

    def add_student(self, student):
        if self.get_student(student.student_id):
            return False
        self.students.append(student)
        self.save_students()
        return True

    def get_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def update_student(self, student_id, name, grade):
        student = self.get_student(student_id)
        if student:
            student.name = name
            student.grade = grade
            self.save_students()
            return True
        return False

    def delete_student(self, student_id):
        student = self.get_student(student_id)
        if student:
            self.students.remove(student)
            self.save_students()
            return True
        return False


# -------------------------------
# GUI Class
# -------------------------------
class StudentGUI:
    def __init__(self, root):
        self.manager = StudentManager()
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("600x450")

        # Labels
        tk.Label(root, text="Student ID").pack()
        self.id_entry = tk.Entry(root)
        self.id_entry.pack()

        tk.Label(root, text="Name").pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        tk.Label(root, text="Grade").pack()
        self.grade_entry = tk.Entry(root)
        self.grade_entry.pack()

        # Buttons
        tk.Button(root, text="Add Student", command=self.add_student).pack(pady=5)
        tk.Button(root, text="Update Student", command=self.update_student).pack(pady=5)
        tk.Button(root, text="Delete Student", command=self.delete_student).pack(pady=5)

        # Table
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Grade"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Grade", text="Grade")
        self.tree.pack(pady=10, fill="both", expand=True)

        self.tree.bind("<ButtonRelease-1>", self.select_student)

        self.load_table()

    def load_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for student in self.manager.students:
            self.tree.insert("", "end", values=(
                student.student_id,
                student.name,
                student.grade
            ))

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)

    def add_student(self):
        student_id = self.id_entry.get()
        name = self.name_entry.get()
        grade = self.grade_entry.get()

        if not student_id or not name or not grade:
            messagebox.showerror("Error", "All fields are required!")
            return

        student = Student(student_id, name, grade)

        if self.manager.add_student(student):
            messagebox.showinfo("Success", "Student added successfully!")
            self.load_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Student ID already exists!")

    def update_student(self):
        student_id = self.id_entry.get()
        name = self.name_entry.get()
        grade = self.grade_entry.get()

        if self.manager.update_student(student_id, name, grade):
            messagebox.showinfo("Success", "Student updated successfully!")
            self.load_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Student not found!")

    def delete_student(self):
        student_id = self.id_entry.get()

        if self.manager.delete_student(student_id):
            messagebox.showinfo("Success", "Student deleted successfully!")
            self.load_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Student not found!")

    def select_student(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if values:
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, values[0])

            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])

            self.grade_entry.delete(0, tk.END)
            self.grade_entry.insert(0, values[2])


# -------------------------------
# Run Application
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentGUI(root)
    root.mainloop()
