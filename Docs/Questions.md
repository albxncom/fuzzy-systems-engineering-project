# Course Finder Documentation

## Questions to be answered by the user

### General Questions

This criterias will act as strict filters.

#### 1. To which track should the courses belong to?

Every course belongs to one or more tracks, specified on at <https://mcs.unibnf.ch>.

**Possible answers** (mulitple choice)

- t0: General
- t1: Distributed Systems
- t2: Advanced Software Engineering
- t3: Advanced Information Processing
- t4: Logic
- t5: Information Systems and Decision Support
- t6: Data Science


#### 2. Are you ok with mandatory exercises?

**Possible answers**

- yes
- no

#### 3. What languages would you prefer?

**Possible answers** (mulitple choice)

- German
- French
- English


### Questions concerning the Language

#### 1. How important is the language of the lectures for you?

This includes how good the lecturers speak the language in which they holds the course as well as the learning material.

**Possible answers**

- Very Important
- Important
- Moderately Important
- Slightly Important
- Unimportant

#### 2. How important is the language of the exercises for you?

This includes how good the assistants speak the language in which they hold the exercise class as well as the exercise material.

**Possible answers**

- Very Important
- Important
- Moderately Important
- Slightly Important
- Unimportant


### Questions concering the contents of the course


#### 1. How important is it for you that the course is understandable?

This includes that the contents are conveyed in an understandable way and the material is illustrated with examples.

**Possible answers**

- Very Important
- Important
- Moderately Important
- Slightly Important
- Unimportant


#### 2. How difficult do you want the lectures and exercices to be?

This includes how difficult it is to follow the exercise classes as well as how difficult the exercises are.

**Possible answers**

- Very difficult
- Difficult
- Neutral
- Easy
- Very easy


#### 3. How important is the commitment of the lecturers and assistants?

This includes how well the lectureres and assistants listen to students' inputs and how responsive they are.

**Possible answers**

- Very Important
- Important
- Moderately Important
- Slightly Important
- Unimportant

### Questions concering effort

#### 1. How much effort are you willing to put into the course?

This includes how much effort it requires to prepare a lecture, the after work and how much time is needed to solve the exercises.

**Possible answers**

- None
- Only a little
- To some extent
- Rather much
- Very much


## Questions to be answered by students who evaluated the course

### General Information

- Course Name: Name of the course 
	- `q_1: string`
- Course ID: ID of the course (e.g. IN.0534..) 
	- `q_2: string`
- Course Category: Category to which course belongs (t0, t1, t2, t3, t4, t5, t6) 
	- `q_3: list of strings`
- Course Language: In which language is the course given? (German, French, English)) 
	- `q_4: in [German, French, English]`
- Exercices Mandatory: Are the exercises mandatory in order to register for the test? (yes, no) 
	- `q_5: in [yes,no]`


### Language 

- How important is the language of the lectures for you? (aggregated to $q_6, w = (0.5, 0.5)$) 
	- Language Professor: How good does the professor know the language he gives the course in? (very poor, poor, moderate, good, very good) 
		- `q_6_1: in [very poor...very good]`
	- Quality Language Lectures: Rate the quality of the language in lectures. (very poor, poor, moderate, good, very good) 
		- `q_6_2: in [very poor...very good]`

- How important is the language of the exercises for you?(aggregated to $q_7, w = (0.5, 0.5)$)
	- Language Assistant: How good does the assistant know the language he gives the exercise classes in? (very poor, poor, moderate, good, very good)
		- `q_7_1: in [very poor...very good]`
	- Quality Language Exercises: Rate the quality of the language in exercises. (very poor, poor, moderate, good, very good)
		- `q_7_2: in [very poor...very good]`

### Course Quality

- How important is it for you that the course is understandable? (aggregated to $q_8, w = (0.5, 0.5)$)
	- Content is understandable: The contents are conveyed in an understandable way. (strongly disagree, disagree, neither agree nor disagree, agree, strongly agree)
		- `q_8_1: in [strongly disagree...strongly agree]`
	- Examples: The material is illustrated with examples. (strongly disagree, disagree, neither agree nor disagree, agree, strongly agree)
		- `q_8_2: in [strongly disagree...strongly agree]`

- How difficult do you want the lectures and exercices to be? (aggregated to $q_9, w = (0.5, 0.5)$)
	- Difficulty Lectures: How difficult is it to follow the lectures? (very difficult, difficult, moderate, easy, very easy)
		- `q_9_1: in [very difficult...very easy]`
	- Difficulty Exercices: How difficult is it to follow the exercises? (very difficult, difficult, moderate, easy, very easy)
		- `q_9_2: in [very difficult...very easy]`

- How important is the commitment of the lecturers and assistants? (aggregated to $q_10, w = (\frac{1}{3}, \frac{1}{3}, \frac{1}{3})$)

	- Listening Professor: How well does the teacher listen to students’ inputs? (very poor, poor, moderate, good, very good) 
		- `q_10_1: in [very poor...very good]`
	- Responsiveness Professor: Rate the responsiveness of the professor (very poor, poor, moderate, good, very good)
		- `q_10_2: in [very poor...very good]`
	- Responsiveness Assistant: Rate the responsiveness of the assistant (very poor, poor, moderate, good, very good)
		- `q_10_3: in [very poor...very good]`
	
- *User not asked, implicated that the user wants maximum quality.* Quality of the course (aggregated to $q_{11}, w = (\frac{1}{6}, ... , \frac{1}{6})$)

	- Course Structure: The course has a clear structure (strongly disagree, disagree, neither agree nor disagree, agree, strongly agree)
		- `q_11_1: in [strongly disagree...strongly agree]`
	- Course Independently: The course enabled me to deepen the contents independently. (strongly disagree, disagree, neither agree nor disagree, agree, strongly agree)
		- `q_11_2: in [strongly disagree...strongly agree]`
	- Course Evaluation Modalities: The evaluation modalities (examination, paper, etc.) were coherent with the learning objectives. (strongly disagree, disagree, neither agree nor disagree, agree, strongly agree)
		- `q_11_3: in [strongly disagree...strongly agree]`
	- Course Activities: The activities offered (reading, group work, excursions, etc.) benefited my learning. (strongly disagree, disagree, neither agree nor disagree, agree, strongly agree)
		- `q_11_4: in [strongly disagree...strongly agree]`
	- Expectations_lectures: The lectures have met my expectations. (strongly disagree, disagree, neither agree nor disagree, agree, strongly agree)
		- `q_11_5: in [strongly disagree...strongly agree]`
	- Course Prepared Exam: The course prepared me well for the test (exam, paper, etc.) (strongly disagree, disagree, neither agree nor disagree, agree, strongly agree)
		- `q_11_6: in [strongly disagree...strongly agree]`

	
### Effort

- How much effort are you willing to put into the course? (aggregated to $q_{12}, w = (\frac{1}{3}, \frac{1}{3}, \frac{1}{3})$)
	- Effort Lectures: How much effort did you personally put in for every lecture? (very few, a few, moderate, some, very much)
		- `q_12_1: in [very few...very very much]`
	- Effort Exercises: How much effort did you personally put in for every exercise? (very few, a few, moderate, some, very much)
		- `q_12_2: in [very few...very very much]`
	- Effort Exam Preperation: How much effort did you personally put into studying for the exam? (very few, a few, moderate, some, very much)
		- `q_12_3: in [very few...very very much]`



### Exam
- Exam Difficulty: Rate the difficulty of the exam.  (very difficult, difficult, moderate, easy, very easy)
	- `q_13: in [very difficult...very easy]`
- Open Book Exam: Was the exam open book? (yes, no)
	- `q_14: in [yes,no]`



<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  }
};
</script>
<script id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">
</script>
