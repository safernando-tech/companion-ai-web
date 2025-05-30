import datetime
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
# THIS IS VERY IMPORTANT! Flask needs a secret key to keep session data secure.
# Make sure to replace 'drsY4t4GXVFJqcY-r0X3Vf9MhRohKbLw' with the random key you generated.
app.secret_key = 'YOUR_VERY_LONG_AND_RANDOM_SECRET_KEY_HERE' # PASTE YOUR NEW KEY HERE INSIDE DOUBLE QUOTES!

# --- GLOBAL KNOWLEDGE BASE FOR FACT BOT ---
knowledge_base = {
    "what is your name": "My name is Companion! I was created by Savitha F and Gemini.",
    "how old are you": "I don't have an age, I'm a computer program.",
    "what is the capital of australia": "The capital of Australia is Canberra.",
    "what is the largest animal": "The largest animal is the blue whale.",
    "who created python": "Python was created by Guido van Rossum.",
    "where are you from": "I exist in the digital world!",
    "what is 2 + 2": "That's a math question! But 2 + 2 equals 4.",
    "what color is the sky": "The sky is usually blue!",
    "who invented the lightbulb": "Thomas Edison is often credited with inventing the lightbulb.",
    "tell me a joke": "Why don't scientists trust atoms? Because they make up everything!",
}

# --- FUNCTIONS (no change needed here for session) ---
def check_mood_web(user_response):
    user_response_lower = user_response.lower()
    reply = ""
    if any(word in user_response_lower for word in ["amazing", "awesome", "fantastic", "excellent", "super", "great"]):
        reply = "Wow, that's absolutely fantastic! Keep that energy going!"
    elif any(word in user_response_lower for word in ["good", "fine", "happy", "well"]):
        reply = "That's wonderful to hear!"
    elif any(word in user_response_lower for word in ["okay", "alright", "so-so", "meh"]):
        reply = "Alright, sometimes 'okay' is good! I hope your day stays positive."
    elif any(word in user_response_lower for word in ["tired", "sleepy", "exhausted", "drained"]):
        reply = "Sounds like you need some rest! Take it easy."
    elif any(word in user_response_lower for word in ["stressed", "overwhelmed", "busy", "frustrated"]):
        reply = "I understand that feeling. Remember to take breaks when you can!"
    elif any(word in user_response_lower for word in ["bad", "sad", "not good", "unhappy", "terrible"]):
        reply = "I'm really sorry to hear that. I hope your day gets better soon!"
    else:
        reply = "Thanks for sharing how you're doing."
    return reply

def solve_math_problem_web(num1_str, operation, num2_str):
    try:
        num1 = float(num1_str)
        num2 = float(num2_str)
    except ValueError:
        return "Error: Invalid input. Please enter numbers only for calculations."
    result = ""
    if operation == "+":
        result = f"{num1} + {num2} = {num1 + num2}"
    elif operation == "-":
        result = f"{num1} - {num2} = {num1 - num2}"
    elif operation == "*":
        result = f"{num1} * {num2} = {num1 * num2}"
    elif operation == "/":
        if num2 == 0:
            return "Error: Cannot divide by zero!"
        else:
            result = f"{num1} / {num2} = {num1 / num2}"
    else:
        return "Sorry, I don't recognize that operation. Please use +, -, *, or /."
    return f"Result: {result}"

def answer_fact_question_web(user_question):
    user_question_lower = user_question.lower()
    for question_key, answer in knowledge_base.items():
        if question_key in user_question_lower:
            return answer
    return "I'm sorry, I don't know the answer to that question yet. Try asking something else!"

# --- WEB ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def home():
    # We now store and get the name from the 'session' (unique to each user's browser)
    if request.method == 'POST':
        name_input = request.form.get('user_name_input')
        if name_input:
            session['user_name'] = name_input.capitalize() # Store name in the user's session

    # Get user_name from session, default to empty string if not set
    current_user_name = session.get('user_name', '')

    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        time_greeting = "Good morning"
    elif current_hour < 18:
        time_greeting = "Good afternoon"
    else:
        time_greeting = "Good evening"

    menu_html = """
    <p>What would you like to do today?</p>
    <ul>
        <li><a href="/mood_checker">Chat about my mood</a></li>
        <li><a href="/math_solver">Solve a math problem</a></li>
        <li><a href="/fact_bot">Ask a fact question</a></li>
    </ul>
    """
    forget_name_link = "<p><a href='/reset_name'>Forget my name</a></p>"

    if not current_user_name:
        return f"""
        <h1>{time_greeting}! Welcome to your Companion!</h1>
        <p>Before we start, what's your name?</p>
        <form method="POST" action="/">
            Your Name: <input type="text" name="user_name_input">
            <input type="submit" value="Submit">
        </form>
        """
    else:
        return f"""
        <h1>{time_greeting}, {current_user_name}! Welcome back to your Companion!</h1>
        {menu_html}
        {forget_name_link}
        """

# New route to reset the user's name
@app.route('/reset_name')
def reset_name():
    # Remove the 'user_name' from the current user's session
    session.pop('user_name', None)
    return redirect(url_for('home')) # Redirect back to the home page

@app.route('/mood_checker', methods=['GET', 'POST'])
def mood_checker():
    if request.method == 'POST':
        user_mood_input = request.form['mood']
        ai_response = check_mood_web(user_mood_input)
        return f"""
        <h1>Your Mood: {user_mood_input}</h1>
        <p>AI says: {ai_response}</p>
        <p><a href="/mood_checker">Ask about mood again</a></p>
        <p><a href="/">Go back to main menu</a></p>
        """
    else:
        return """
        <h1>How are you feeling today?</h1>
        <form method="POST" action="/mood_checker">
            <input type="text" name="mood" placeholder="e.g., happy, tired, sad">
            <input type="submit" value="Tell AI">
        </form>
        <p><a href="/">Go back to main menu</a></p>
        """

@app.route('/math_solver', methods=['GET', 'POST'])
def math_solver():
    if request.method == 'POST':
        num1_input = request.form['num1']
        operation_input = request.form['operation']
        num2_input = request.form['num2']
        ai_response = solve_math_problem_web(num1_input, operation_input, num2_input)
        return f"""
        <h1>Math Problem Solved!</h1>
        <p>{ai_response}</p>
        <p><a href="/math_solver">Solve another math problem</a></p>
        <p><a href="/">Go back to main menu</a></p>
        """
    else:
        return """
        <h1>Math Solver Mode</h1>
        <p>I can do addition (+), subtraction (-), multiplication (*), and division (/).</p>
        <form method="POST" action="/math_solver">
            First Number: <input type="text" name="num1"><br><br>
            Operation (+, -, *, /): <input type="text" name="operation"><br><br>
            Second Number: <input type="text" name="num2"><br><br>
            <input type="submit" value="Calculate">
        </form>
        <p><a href="/">Go back to main menu</a></p>
        """

@app.route('/fact_bot', methods=['GET', 'POST'])
def fact_bot():
    if request.method == 'POST':
        user_question_input = request.form['question']
        ai_response = answer_fact_question_web(user_question_input)
        return f"""
        <h1>Your Question: {user_question_input}</h1>
        <p>AI says: {ai_response}</p>
        <p><a href="/fact_bot">Ask another question</a></p>
        <p><a href="/">Go back to main menu</a></p>
        """
    else:
        return """
        <h1>Fact Bot Mode</h1>
        <p>Ask me a question about facts I know.</p>
        <form method="POST" action="/fact_bot">
            Your question: <input type="text" name="question" placeholder="e.g., what is your name">
            <input type="submit" value="Ask AI">
        </form>
        <p><a href="/">Go back to main menu</a></p>
        """

if __name__ == '__main__':
    app.run(debug=True)
