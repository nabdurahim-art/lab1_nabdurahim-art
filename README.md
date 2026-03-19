Grade evaluator

Program overview

This is a Python program that reads a CSV file of students' assignments and calculates:
Formative, summative, and total score. 
GPA (0-5 scale)
Final decision(Passed/Failed)
Resubmission option. 

                               Usability

Start by running a Python program (e.g., python3 grade-evaluator.py 
Enter the CSV file name when prompted. 
View student transcript with:
GPA
Decision 
Resubmission information. 

N.B: 
Score must be 0-100
Formative weight= 60%, summative weight=40%, total=100%
Students pass only if they score >=50% in both categories. 
Failed formatives assignments with the highest weight are eligible for resubmission. 
If both failed assignments have equal weight are eligible for resubmission. 


                           Environment setup (organizer.sh)

 Run the shell script to initialize your workspace (bash organizer.sh)
After running the script :
Creates an archive/ folder if it doesn’t exist
Moves the current grades.csv to archive/ and appends a timestamp
Generates a new empty grades.csv ready for new grades
Records the action in organizer.log




              

