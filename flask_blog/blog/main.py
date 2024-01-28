from blog import create_app

app = create_app()

if __name__ == '__main__':
    # Create tables
    # app.app_context().push()
    # db.create_all()
    # db.session.commit()
    app.run(debug=True);
