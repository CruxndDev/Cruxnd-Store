from app import create_app

app = create_app()

# TODO Work on JWT implmentation 
@app.cli.command("test")
def test():
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
