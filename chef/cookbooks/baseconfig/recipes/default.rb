# Make sure the Apt package lists are up to date, so we're downloading versions that exist.
cookbook_file "apt-sources.list" do
  path "/etc/apt/sources.list"
end
execute 'apt_update' do
  command 'apt-get update'
end

package "postgresql"
package "postgresql-server-dev-all"
package "libpython-dev"
package "python-pip"

execute "pip-install" do 
  command "pip install -r /home/ubuntu/project/chef/cookbooks/baseconfig/files/default/requirements.txt"
end

execute "create_db" do
    command "echo \"CREATE DATABASE mydb; CREATE USER ubuntu; GRANT ALL PRIVILEGES ON DATABASE mydb TO ubuntu;\" | sudo -u postgres psql"
end
execute "migrate" do
  user "ubuntu"
  cwd "/home/ubuntu/project"
    command "python manage.py migrate"
end
execute "init-db" do
  user "ubuntu"
  cwd "/home/ubuntu/project"
    command "python manage.py loaddata chef/cookbooks/baseconfig/files/default/init.json"
end

execute "get-static-files" do
  user "ubuntu"
  cwd "/home/ubuntu/project"
    command "python manage.py collectstatic --noinput"
end

package "nginx"
cookbook_file "nginx-default" do
  path "/etc/nginx/sites-available/default"
end
execute "nginx_restart" do
  command "nginx -s reload"
end

cookbook_file "rc.local" do
  path "/etc/rc.local"
end
execute "start-uwsgi" do
  command "sudo /bin/sh /etc/rc.local"
end