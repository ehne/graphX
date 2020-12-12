import graphX as gx

g = gx.Graph()

@g.run_web
def code():
    print("hello")

code()