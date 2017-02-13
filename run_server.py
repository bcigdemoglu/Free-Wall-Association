"""
This example module shows various types of documentation available for use
with pydoc.  To generate HTML documentation for this module issue the
command:

    pydoc -w foo

"""

from flask_rest_service import app

if __name__ == '__main__':
    app.run(debug=True)