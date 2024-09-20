# functions.py

# Python function
optimize_me = """def find_top_students(students, grades):
    # Combine student names with their grades
    student_grades = []
    for i in range(len(students)):
        student_grades.append((students[i], grades[i]))

    # Sort students by their grades in descending order
    for i in range(len(student_grades)):
        for j in range(i + 1, len(student_grades)):
            if student_grades[i][1] < student_grades[j][1]:
                student_grades[i], student_grades[j] = student_grades[j], student_grades[i]

    # Return the top 3 students
    return student_grades[:3]

students = ["Alice", "Bob", "Charlie", "David", "Eve"]
grades = [85, 92, 88, 91, 76]

top_students = find_top_students(students, grades)
print(top_students)"""

# JavaScript function
optimize_me2 = """
function findTopStudents(students, grades) {
    // Combine student names with their grades
    let studentGrades = [];
    for (let i = 0; i < students.length; i++) {
        studentGrades.push([students[i], grades[i]]);
    }

    // Sort students by their grades in descending order
    for (let i = 0; i < studentGrades.length; i++) {
        for (let j = i + 1; j < studentGrades.length; j++) {
            if (studentGrades[i][1] < studentGrades[j][1]) {
                [studentGrades[i], studentGrades[j]] = [studentGrades[j], studentGrades[i]];
            }
        }
    }

    // Return the top 3 students
    return studentGrades.slice(0, 3);
}

let students = ["Alice", "Bob", "Charlie", "David", "Eve"];
let grades = [85, 92, 88, 91, 76];

let topStudents = findTopStudents(students, grades);
console.log(topStudents);
"""

# C++ function
optimize_me3 = """
#include <iostream>
#include <vector>
#include <string>

using namespace std;

vector<pair<string, int>> findTopStudents(vector<string> students, vector<int> grades) {
    // Combine student names with their grades
    vector<pair<string, int>> studentGrades;
    for (size_t i = 0; i < students.size(); i++) {
        studentGrades.push_back(make_pair(students[i], grades[i]));
    }

    // Sort students by their grades in descending order
    for (size_t i = 0; i < studentGrades.size(); i++) {
        for (size_t j = i + 1; j < studentGrades.size(); j++) {
            if (studentGrades[i].second < studentGrades[j].second) {
                swap(studentGrades[i], studentGrades[j]);
            }
        }
    }

    // Return the top 3 students
    vector<pair<string, int>> topStudents(studentGrades.begin(), studentGrades.begin() + 3);
    return topStudents;
}

int main() {
    vector<string> students = {"Alice", "Bob", "Charlie", "David", "Eve"};
    vector<int> grades = {85, 92, 88, 91, 76};

    vector<pair<string, int>> topStudents = findTopStudents(students, grades);
    for (auto &student : topStudents) {
        cout << student.first << ": " << student.second << endl;
    }
    return 0;
}
"""

# Java function
optimize_me4 = """
import java.util.*;

public class Main {
    public static List<Map.Entry<String, Integer>> findTopStudents(List<String> students, List<Integer> grades) {
        // Combine student names with their grades
        List<Map.Entry<String, Integer>> studentGrades = new ArrayList<>();
        for (int i = 0; i < students.size(); i++) {
            studentGrades.add(new AbstractMap.SimpleEntry<>(students.get(i), grades.get(i)));
        }

        // Sort students by their grades in descending order
        for (int i = 0; i < studentGrades.size(); i++) {
            for (int j = i + 1; j < studentGrades.size(); j++) {
                if (studentGrades.get(i).getValue() < studentGrades.get(j).getValue()) {
                    Collections.swap(studentGrades, i, j);
                }
            }
        }

        // Return the top 3 students
        return studentGrades.subList(0, 3);
    }

    public static void main(String[] args) {
        List<String> students = Arrays.asList("Alice", "Bob", "Charlie", "David", "Eve");
        List<Integer> grades = Arrays.asList(85, 92, 88, 91, 76);

        List<Map.Entry<String, Integer>> topStudents = findTopStudents(students, grades);
        for (Map.Entry<String, Integer> student : topStudents) {
            System.out.println(student.getKey() + ": " + student.getValue());
        }
    }
}
"""

# Ruby function
optimize_me5 = """
def find_top_students(students, grades)
    # Combine student names with their grades
    student_grades = []
    for i in 0...students.length
        student_grades << [students[i], grades[i]]
    end

    # Sort students by their grades in descending order
    for i in 0...student_grades.length
        for j in (i+1)...student_grades.length
            if student_grades[i][1] < student_grades[j][1]
                student_grades[i], student_grades[j] = student_grades[j], student_grades[i]
            end
        end
    end

    # Return the top 3 students
    student_grades[0...3]
end

students = ["Alice", "Bob", "Charlie", "David", "Eve"]
grades = [85, 92, 88, 91, 76]

top_students = find_top_students(students, grades)
puts top_students.inspect
"""

# PHP function
optimize_me6 = """
<?php
function findTopStudents($students, $grades) {
    // Combine student names with their grades
    $studentGrades = [];
    for ($i = 0; $i < count($students); $i++) {
        $studentGrades[] = [$students[$i], $grades[$i]];
    }

    // Sort students by their grades in descending order
    for ($i = 0; $i < count($studentGrades); $i++) {
        for ($j = $i + 1; $j < count($studentGrades); $j++) {
            if ($studentGrades[$i][1] < $studentGrades[$j][1]) {
                $temp = $studentGrades[$i];
                $studentGrades[$i] = $studentGrades[$j];
                $studentGrades[$j] = $temp;
            }
        }
    }

    // Return the top 3 students
    return array_slice($studentGrades, 0, 3);
}

$students = ["Alice", "Bob", "Charlie", "David", "Eve"];
$grades = [85, 92, 88, 91, 76];

$topStudents = findTopStudents($students, $grades);
print_r($topStudents);
?>
"""

# Go function
optimize_me7 = """
package main

import (
    "fmt"
)

func findTopStudents(students []string, grades []int) [][2]interface{} {
    // Combine student names with their grades
    studentGrades := make([][2]interface{}, len(students))
    for i := 0; i < len(students); i++ {
        studentGrades[i] = [2]interface{}{students[i], grades[i]}
    }

    // Sort students by their grades in descending order
    for i := 0; i < len(studentGrades); i++ {
        for j := i + 1; j < len(studentGrades); j++ {
            if studentGrades[i][1].(int) < studentGrades[j][1].(int) {
                studentGrades[i], studentGrades[j] = studentGrades[j], studentGrades[i]
            }
        }
    }

    // Return the top 3 students
    return studentGrades[:3]
}

func main() {
    students := []string{"Alice", "Bob", "Charlie", "David", "Eve"}
    grades := []int{85, 92, 88, 91, 76}

    topStudents := findTopStudents(students, grades)
    fmt.Println(topStudents)
}
"""

# C# function
optimize_me8 = """
using System;
using System.Collections.Generic;

class Program
{
    static List<Tuple<string, int>> FindTopStudents(List<string> students, List<int> grades)
    {
        // Combine student names with their grades
        var studentGrades = new List<Tuple<string, int>>();
        for (int i = 0; i < students.Count; i++)
        {
            studentGrades.Add(Tuple.Create(students[i], grades[i]));
        }

        // Sort students by their grades in descending order
        for (int i = 0; i < studentGrades.Count; i++)
        {
            for (int j = i + 1; j < studentGrades.Count; j++)
            {
                if (studentGrades[i].Item2 < studentGrades[j].Item2)
                {
                    var temp = studentGrades[i];
                    studentGrades[i] = studentGrades[j];
                    studentGrades[j] = temp;
                }
            }
        }

        // Return the top 3 students
        return studentGrades.GetRange(0, 3);
    }

    static void Main()
    {
        var students = new List<string> { "Alice", "Bob", "Charlie", "David", "Eve" };
        var grades = new List<int> { 85, 92, 88, 91, 76 };

        var topStudents = FindTopStudents(students, grades);
        foreach (var student in topStudents)
        {
            Console.WriteLine($"{student.Item1}: {student.Item2}");
        }
    }
}
"""

