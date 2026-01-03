import jpype
import jaydebeapi
import os
import sys

# Start JVM if not already started
if not jpype.isJVMStarted():
    # Locate h2 jar file
    h2_jar = r"C:\Users\athom\.m2\repository\com\h2database\h2\2.3.232\h2-2.3.232.jar"

    if not os.path.exists(h2_jar):
        print(f"H2 JAR file not found at: {h2_jar}")
        print("Please download H2 database jar from Maven repository")
        sys.exit(1)

    jpype.startJVM(jpype.getDefaultJVMPath(), f"-Djava.class.path={h2_jar}")

try:
    # Connect to H2 database (file-based or in-memory)
    # Note: You need to know the actual database file location or connection string
    # This is a template - adjust the connection string based on your application.properties

    # For file-based database:
    # conn = jaydebeapi.connect("org.h2.Driver",
    #                           "jdbc:h2:file:./data/quizdb",
    #                           ["SA", ""],
    #                           h2_jar)

    # For checking if app is running with in-memory database, we can't access it externally
    print("INFO: The application uses an in-memory H2 database.")
    print("INFO: We need to update users through the application itself or by restarting.")
    print("\nTo link users to countries, you have two options:")
    print("1. Stop the application and delete the database file (if file-based)")
    print("2. Add a migration script that runs on startup")
    print("\nLet's add a migration script instead...")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if jpype.isJVMStarted():
        jpype.shutdownJVM()

