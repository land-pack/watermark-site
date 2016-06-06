from fabric import *

env.hosts = ["127.0.0.1"]
env.user = "frank"
env.password = "openos"


def prepare_deploy():
    sudo('mkdir /var/lib/watermark-site')
    sudo('chmod a+w /var/lib/watermark-site')

def deploy():
    with cd('/home/frank/ak/supervisor/watermark-site'):
        run('git pull')
        sudo('supervisorctl restart app')
        sudo('supervisorctl status')

        # fab deploy
