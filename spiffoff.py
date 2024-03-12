from spiffworkflow import Workflow
from spiffworkflow.activities import PythonActivity


# Define the activities
class HelloWorldActivity(PythonActivity):
    def run(self, context):
        print("Hello, World!")

# Create a workflow
workflow = Workflow()

# Add the "Hello World" activity to the workflow
workflow.add_activity(HelloWorldActivity(name="hello_world"))

# Run the workflow
workflow.run()
