from app import app,address,port

DEBUG=True

if __name__ == "__main__":
    app.run(host=address, port=port, debug=DEBUG)
