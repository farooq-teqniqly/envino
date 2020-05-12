import uuid

from app import app, db, User, OAuth

if __name__ == "__main__":
    app.run()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, OAuth=OAuth, uuid=uuid)
