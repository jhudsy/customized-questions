# customized-questions

This is a work in progress to create customised questions for students based on their student-id.

## Creating questions

The system is designed to (at the moment) not rely on any external systems. Therefore, all questions are visible to everyone. Questions are created using Python, and require 
  1. question text
  2. a set/list of functions which initialise values in the question (based on student id)
  3. a dictionary of functions for checking answers

### Question text

The question text is a string containing the usual python curly bracket substitutions. The text is interpreted as a HTML string.  E.g., 
```qs="What is <p>(a) {x}+{y}?</p> <p> {x}*{y}?</p>"```

### Question value initialisers

A sample function could take the form

```
def set_values(dict):
   dict["x"]=random.randint(0,5)
   dict["y"]=random.randint(5,7)
```

Note that the idea behind the system as a whole is to use a student's student-id as the seed for the random number generator, creating reproducible questions based on this seed.

The `dict` dictionary stores the parameters to be substituted into the string.

Finally, multiple value initialisers are possible, and these will be passed as a list into the constructor (see below).

### Answers

Multiple answer checkers are possible. These are passed in via a dictionary and displayed based on the dictionary key. Each function is passed in the dictionary used to generate the question, as well as a dictionary containing the user's answer. E.g.,

```
def check_add(dict,answers):
  return int(answers["add"])==(int(dict["x"])+int(dict["y"]))

def check_multiply(dict,answers):
  return int(answers["mult"])==(int(dict["x"])*int(dict["y"]))
```

### Putting it all together

To create a question, you need to create a `Question` object, e.g., as follows (the first parameter is the question name):

```
Question("Add and multiply",qs,[set_values],{"add":check_add,"mult":check_multiply}
```

You can pass an optional `marks_dict` dictionary mapping subquestion names to numbers. These will be the marks assigned to that subquestion.

You can pass an optional final "info" function which will also be passed the dictionary of values, and which will also be logged to the CSV file. This can be used to - for example - record correct answers.

The file containing the question should be placed in the `/questions` sub-directory.


## Using the system

### Configuration

Create a config.ini file within the `config/` subdirectory. The system accepts the following parameters

- `mark_file` the name and location of the marks file to write
- `question_path` the path to the questions to be used
- `secret_key` the Flask secret key to use
- `public_key_file` the location of the public key to use for mark file encryption. A public/private key pair can be generated using the `make_key.py` script.

Navigating into the system will ask for a student id before displaying anything. This can be changed by selecting "Change ID" in the top right of the site.

Navigating to the root of the website will display all questions.

Selecting a question will display it and provide a form where answers can be submitted. Submitting an answer will simply give the user a "Submission received" confirmation. At the same time, a marks.csv file will be created/appended.

The format if the CSV file is as follows:
- Question (by name)
- student id of the submitter
- total marks obtained for the question
- A dictionary containing the answer name and 1/0 depending if the user got the answer correct or not
- A dictionary containing the answer name and the value put in by the user
- The output of the "info" function (if the function exists).
- The time (using `time.time()`) the answer was submitted

### Encryption

The system encrypts the marks file so that even if a breach occurs, no information can be gained. You should keep the private key safe. To decrypt the marks file, use the `decrypt.py` script. Parameters for this script are (1) the private key file; (2) the location of the encrypted marks file; (3) the location to write the decrypted marks file to.


## TODO

- lots of refactoring
- integrate with LTI
- Per course questions etc 
- Nicer error handling and reporting (there isn't any right now)

