from config import app
import controllers



#master routes
app.add_url_rule('/', view_func=controllers.root, endpoint='root')
app.add_url_rule('/dashboard', view_func=controllers.dashboard, endpoint='dashboard')

#User routes

app.add_url_rule('/users/new', view_func=controllers.new_user, endpoint='users:new_user')
app.add_url_rule('/users/create', view_func=controllers.create_user, endpoint='users:create_user', methods=['POST'])
app.add_url_rule('/users/login', view_func=controllers.login, endpoint='users:login', methods=['POST'])
app.add_url_rule('/logout', view_func=controllers.logout, endpoint='users:logout')

#Event routes
app.add_url_rule('/jobs/<id>/add', view_func=controllers.job_add, endpoint='jobs:add')
app.add_url_rule('/jobs', view_func=controllers.jobs, endpoint='jobs')
app.add_url_rule('/jobs/new', view_func=controllers.job_new, endpoint='jobs:new', methods=['POST'])
app.add_url_rule('/jobs/<id>', view_func=controllers.job_view, endpoint='jobs:view')
app.add_url_rule('/jobs/<id>/edit', view_func=controllers.job_edit_page, endpoint='jobs:edit_page')
app.add_url_rule('/jobs/<id>/update', view_func=controllers.job_edit, endpoint='jobs:edit', methods=['POST'])
app.add_url_rule('/jobs/<id>/delete', view_func=controllers.job_delete, endpoint='jobs:delete')
