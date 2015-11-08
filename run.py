import sys
# Run a test server.
try:
    port = int(sys.argv[1])
    from app import app
    app.run(host='0.0.0.0', port=port, debug=True)
except:
    from app import app
    port = 3000
    app.run(host='0.0.0.0', port=port, debug=True)

