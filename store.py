from app import create_app

app = create_app()

# TODO change all assertEquals to assertIsInstance, and remove all type annotations in the app/models.py file before going further.

@app.cli.command('test')
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity = 2).run(tests)