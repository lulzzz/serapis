"""
Steps:
-get the summer.ai.pem key
-login to the env.host machine and add your public key to the machine's authorized keys

http://www.perrygeo.com/running-python-with-compiled-code-on-aws-lambda.html
"""

from fabric.api import local, sudo, run, warn_only, env, put, cd
import time

# the user to use for the remote commands
env.user = 'ec2-user'
# the servers where the commands are executed
env.hosts = ['52.91.194.132']

gitfile = 'wordnik.git.zip'
lambdafile = 'wordnik.lambda.zip'
lambdafunction = 'WordTask'


def upgrade():
    # Make sure machine and dev tools are up to date
    sudo('sudo yum -y update')
    sudo('yum -y upgrade')
    sudo('yum -y install python27-devel python27-pip')


def pack():
    # create a new source distribution zipfile
    local('git archive --format=zip HEAD -o %s' % gitfile, capture=False)

    # upload the source zipfile to the temporary folder on the server
    deploy_filename = '/tmp/wordnik.%s.zip' % str(time.time())
    put(gitfile, deploy_filename)
    local('rm %s' % gitfile)

    # create a place where we can unzip the zipfile, then enter
    # that directory and unzip it
    with warn_only():
        run('rm -rf ~/lambda')
    run('mkdir ~/lambda')
    with cd('~/lambda'):
        run('unzip %s' % deploy_filename)
        # now setup the package with our virtual environment's
        # python interpreter
        # run('/var/www/yourapplication/env/bin/python setup.py install')

        """
        TODO: compile all the dependencies locally on the ec2 machine,
        making sure any extensions are in a subdirectory of ~/lambda so that they are zipped
        """
        run('virtualenv venv')
        run('source venv/bin/activate && pip install -r requirements.txt -t .')

        run('zip -9r wordnik.zip *')

    # Get the file back onto our local machine
    local('scp %s@%s:~/lambda/wordnik.zip %s' % (env.user, env.hosts[0], lambdafile))


def update():
    local('git archive --format=zip HEAD -o %s' % gitfile, capture=False)
    local('unzip -d git_tmp -o -u %s' % gitfile)
    local('zip -9r %s git_tmp/*' % lambdafile)
    local('rm -r git_tmp')


def deploy():
    # If this says that the function is not found, create it first:
    # aws lambda create-function --region us-east-1 --function-name WordTask --zip-file fileb://wordnik.lambda.zip --handler lambda_handler.handler --runtime python2.7 --timeout 10 --memory-size 512 --role arn:aws:iam::054978852993:role/lambda_basic_execution
    cwd = local('pwd', capture=True).strip()
    local('aws lambda update-function-code --region us-east-1 --function-name %s --zip-file fileb://%s/%s' % (lambdafunction, cwd, lambdafile))