# Import required libraries
from flask import Flask, render_template, request
import subprocess
import platform
import re

# Create Flask application
app = Flask(__name__)


# Function to ping a host
def ping(host):

    # Check the operating system
    # Windows and Linux/macOS use different ping commands
    if platform.system().lower() == "windows":
        command = ["ping", "-n", "4", host]
    else:
        command = ["ping", "-c", "4", host]

    # Execute the ping command
    result = subprocess.run(
        command,
        capture_output=True,   # Store output instead of printing it
        text=True              # Return output as normal text
    )

    # Save command output
    output = result.stdout

    # If return code is 0, host is reachable
    if result.returncode == 0:
        status = "Reachable"
    else:
        status = "Unreachable"

    # Default value
    avg_time = "N/A"

    # Extract average ping time using Regular Expression
    if platform.system().lower() == "windows":
        match = re.search(r"Average = (\d+)ms", output)
    else:
        match = re.search(r"min/avg/max.* = .*?/([\d\.]+)/", output)

    # If average time is found
    if match:
        avg_time = match.group(1) + " ms"

    # Return both values
    return status, avg_time


# Home page
@app.route("/", methods=["GET", "POST"])
def index():

    # Initially no result
    status = None
    avg_time = None

    # When user clicks the Ping button
    if request.method == "POST":

        # Get value entered by user
        host = request.form["host"]

        # Call ping function
        status, avg_time = ping(host)

    # Send data to HTML page
    return render_template(
        "index.html",
        status=status,
        avg_time=avg_time
    )


# Start Flask server
if __name__ == "__main__":
    app.run(debug=True)