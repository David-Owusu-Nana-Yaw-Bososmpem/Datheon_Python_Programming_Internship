CUSTOMER SUPPORT CHATBOT

========================



1\. PROJECT OVERVIEW

\-------------------

This project is a simple, rule-based customer support chatbot written in Python.

It runs in a command-line/terminal window and responds to user messages by

checking for greetings, exit commands, and questions related to a small set of

frequently asked questions (FAQs).



The chatbot currently supports:

\- Greetings and welcome messages

\- Questions about hours of operation

\- Questions about submitting an internship project

\- Questions about receiving a certificate

\- A fallback response when it cannot recognize a question

\- Exit commands such as bye, goodbye, exit, quit, stop, and close



This is a rule-based chatbot. It does not use machine learning, an AI model,

or an external chatbot API. It identifies likely user intent using keywords

and regular-expression patterns.



2\. PROJECT FILES

\----------------

The project contains two files:



chatbot.py

&#x20;   The main Python program. It loads the FAQ data, processes user input,

&#x20;   identifies the user's intent, generates a response, and runs the

&#x20;   conversation loop.



sample\_faq.json

&#x20;   Stores the greeting phrases and FAQ questions and answers in JSON format.

&#x20;   The chatbot reads this file when it starts.



Keep both files in the same folder so that chatbot.py can locate

sample\_faq.json automatically.



3\. REQUIREMENTS

\---------------

\- Python 3.8 or later is recommended.

\- No third-party Python packages are required.

\- The program uses Python's standard library:

&#x20;   json       - reads the FAQ data from the JSON file

&#x20;   re         - performs text cleaning and pattern matching

&#x20;   sys        - exits when required data cannot be loaded

&#x20;   pathlib    - locates the FAQ file

&#x20;   typing     - provides type hints



4\. HOW TO RUN THE CHATBOT

\-------------------------

Windows:

1\. Extract the project ZIP file to a folder on your computer.

2\. Open the extracted folder.

3\. Open Command Prompt or the terminal in VS Code.

4\. Change directory to the project folder. For example:



&#x20;      cd path\\to\\chatbot



5\. Run the program:



&#x20;      python chatbot.py



&#x20;  If the command above does not work, try:



&#x20;      py chatbot.py



6\. The chatbot will display a welcome message. Type a question and press

&#x20;  Enter to receive a response.

7\. To end the conversation, type bye, goodbye, exit, or quit.



No virtual environment or package installation is necessary for this

project because it has no third-party dependencies. A virtual environment

may still be used if you prefer to keep projects isolated.



5\. HOW THE CHATBOT WORKS

\------------------------

The chatbot follows these main steps:



Step 1: Load FAQ data

&#x20;   When the program starts, it reads sample\_faq.json. The file must contain

&#x20;   two top-level keys: "greetings" and "faqs". If the file is missing or

&#x20;   contains invalid JSON, the program displays an error and stops.



Step 2: Display the welcome message

&#x20;   The chatbot prints a banner and an opening greeting, then waits for

&#x20;   the user to enter a message.



Step 3: Normalize the user's input

&#x20;   The normalize() function:

&#x20;   - Converts the message to lowercase.

&#x20;   - Removes spaces at the beginning and end.

&#x20;   - Replaces repeated whitespace with a single space.

&#x20;   - Removes trailing punctuation such as question marks and full stops.



&#x20;   This helps the chatbot compare messages more consistently.



Step 4: Detect the user's intent

&#x20;   The detect\_intent() function checks the message in this order:

&#x20;   - Exit intent: checks whether the user wants to end the conversation.

&#x20;   - Greeting intent: checks whether the user has entered a greeting.

&#x20;   - FAQ intent: checks whether the message matches a supported FAQ.

&#x20;   - Fallback intent: used when no supported intent is recognized.



Step 5: Match an FAQ

&#x20;   The match\_faq() function uses predefined keyword lists and regular

&#x20;   expressions. Each matching keyword adds to a score, and each matching

&#x20;   regular expression adds to the score as well.



&#x20;   The FAQ with the highest score is selected if its score reaches the

&#x20;   minimum matching threshold. The selected FAQ's answer is then returned.



Step 6: Generate and display a response

&#x20;   The get\_response() function generates the appropriate message. The main

&#x20;   conversation loop prints the response and continues until the user exits

&#x20;   or interrupts the program.



6\. CURRENT FAQ TOPICS AND ANSWERS

\---------------------------------

Topic: Hours of operation

Question example:

&#x20;   What are your hours of operation?



Current answer:

&#x20;   We operate Monday through Friday from 9:00 AM to 6:00 PM IST.



Topic: Internship project submission

Question example:

&#x20;   How do I submit my internship project?



Current answer:

&#x20;   You can submit your public GitHub repository link through your Student

&#x20;   Workspace.



Topic: Certificate issuance

Question example:

&#x20;   When will I receive my certificate?



Current answer:

&#x20;   Certificates are reviewed and issued within 3-5 business days after

&#x20;   your code review.



Note: These are the answers currently stored in sample\_faq.json. Update

them if the organization's actual policies or details change.



7\. EXAMPLE CONVERSATION

\-----------------------

Bot: Hello! How can I help you today?



You: Hi



Bot: Hello! Welcome to our support assistant. I can help you with:

&#x20;    - Our hours of operation

&#x20;    - How to submit your internship project

&#x20;    - When you will receive your certificate

&#x20;    How can I assist you today?



You: What time do you close?



Bot: We operate Monday through Friday from 9:00 AM to 6:00 PM IST.



You: How can I submit my internship project?



Bot: You can submit your public GitHub repository link through your

&#x20;    Student Workspace.



You: Bye



Bot: Goodbye! Have a great day. Feel free to come back if you have more

&#x20;    questions.



8\. HOW TO ADD OR EDIT FAQ CONTENT

\---------------------------------

To change an answer:

1\. Open sample\_faq.json in Notepad or another text editor.

2\. Find the relevant FAQ object.

3\. Edit the text inside its "answer" field.

4\. Save the file, making sure it remains a valid JSON file.



To add a new FAQ:

1\. Add a new question-and-answer object to the "faqs" list in

&#x20;  sample\_faq.json.

2\. Add matching keywords and regular-expression patterns for the new topic

&#x20;  inside the patterns list in match\_faq() in chatbot.py.

3\. Set the pattern's "index" to the position of the new FAQ in the JSON

&#x20;  "faqs" list. The first FAQ has index 0, the second has index 1, and so on.

4\. Save both files and test the new question.



IMPORTANT:

The current chatbot uses fixed FAQ indexes in chatbot.py. The order of the

FAQ entries in sample\_faq.json must therefore match the indexes assigned

to the patterns in chatbot.py. If the order changes, update the indexes too.

Adding a question to the JSON file alone will not automatically make the

chatbot recognize it.



9\. ERROR HANDLING AND LIMITATIONS

\---------------------------------

\- If sample\_faq.json cannot be found, the program displays an error and exits.

\- If sample\_faq.json contains invalid JSON, the program displays an error

&#x20; and exits.

\- If the JSON file does not contain both "greetings" and "faqs", the program

&#x20; displays an error and exits.

\- The chatbot only recognizes topics for which matching rules have been

&#x20; written.

\- A question phrased in an unexpected way may receive the fallback response.

\- The chatbot does not learn from conversations or remember previous sessions.

\- The chatbot does not connect to a database, website, live agent, or external

&#x20; service.

\- The FAQ answers are fixed text and must be updated manually.



10\. TESTING CHECKLIST

\---------------------

After making changes, test the following:



\[ ] Run the chatbot using python chatbot.py.

\[ ] Enter a greeting such as "Hello".

\[ ] Ask about opening hours.

\[ ] Ask how to submit an internship project.

\[ ] Ask when a certificate will be issued.

\[ ] Enter an unrelated question and confirm that the fallback response appears.

\[ ] Enter "bye" or "quit" and confirm that the program exits.

\[ ] Temporarily check that the program reports a clear error if the FAQ file

&#x20;   is missing or contains invalid JSON.



11\. PROJECT SUMMARY

\-------------------

Project name: Customer Support Chatbot

Project type: Rule-based, command-line chatbot

Programming language: Python

FAQ data format: JSON

Interface: Command-line / terminal

External dependencies: None



The project demonstrates basic chatbot development concepts, including

input normalization, keyword matching, regular expressions, intent detection,

JSON data loading, response generation, and handling a continuous user

conversation.



