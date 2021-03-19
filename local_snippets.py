# # @app.route('/login', methods=['POST', 'GET'])
#     # def login():
#     #     if request.method == 'POST':
#     #         user = get_user_by_email(request.form['email'])
#     #         password = check_password_hash(user.psw, request.form['psw'])
#     #         if user and password:
#     #             user_login = UserLogin().create(user)
#     #
#     #             login_user(user_login)
#     #             return redirect(url_for('gpu'))
#     #         flash("Email or password is wrong.")
#     #
#     #     return render_template('login.html', menu=menu, title='Авторизация')
#
#
# class Profiles(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(50), nullable=True)
#     lastname = db.Column(db.String(50), nullable=True)
#     city = db.Column(db.String(100))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return f'<profiles {self.id}>'
#
#
#
# <div class="form-group">
#                     <label for="email">Email address:</label>
#                     <input type="email" name="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email">
#                     <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
#                     <label for="psw">Password</label>
#                     <input type="password" name="psw" class="form-control" id="exampleInputPassword1" placeholder="Password">
#                 </div>
#             <button type="submit" class="btn btn-primary">Submit</button>
#             </form>
#
# { %
# for category, message in get_flashed_messages(True) %}
# < span
#
#
# class ="badge bg-{{category}}" > {{message}} < / span >
#
#
# { % endfor %}

# reg_form = RegistrationForm()
# if reg_form.validate_on_submit():
#     print('from validated!')
#     try:
#         password_hash = generate_password_hash(request.form['password'])
#
#         pprint(reg_form)
#         user = User(email=reg_form['email'],
#                     password=password_hash,
#                     firstname=reg_form['firstname'],
#                     lastname=reg_form['lastname'],
#                     city=reg_form['city'],
#                     role='user')
#
#         db.session.add(user)
#         db.session.commit()
#         print('user ready')
#         login_user(user)
#         print('user logged in')
#         flash('User registered successfully', 'success')
#         return redirect(url_for('index'))
#     except Exception as exp:
#         db.session.rollback()  # откатываем изменения
#         print(f"Ошибка добавления в БД: {exp}")
#         flash('Something goes wrong!', 'error')
#         return redirect(url_for('register'))
# print('something else!')
# return redirect(url_for('register'))
