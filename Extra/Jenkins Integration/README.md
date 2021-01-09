## Use Jenkins to run Ansible playbook that deploys nginx

* Installed Jenkins on the control node; as per the official docs page:
```
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > \
    /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins
```

* We need Java as well since Jenkins is built on it
```
sudo apt update
sudo apt search openjdk
sudo apt install openjdk-11-jdk
sudo apt install openjdk-11-jdk
java -version
```

* Once installed, set the Ansible plugin from Manage Jenkins --> Manage Plugins
And then configure with Global Tool Configuration setting the ansible home dir

* Setup Jenkinsfile like so:
```
pipeline {
    agent any
    stages{
        stage('SCM Checkout'){
            steps{
                git 'https://github.com/deeprony7/devops-practical-challenge'
            }
        }
        stage('Execute Ansible PB'){
            steps{
                ansiblePlaybook become: true, credentialsId: '7022a5e7-e749-4d17-9883-a159e506be65', disableHostKeyChecking: true, installation: 'ansible', inventory: 'With-Playbook/inv.ini', playbook: 'With-Playbook/nginx_install.yml'
            }
        }
    }
}
```

* The credentials id here is built with the Pipeline syntax where node access config is set and paths to inventory file and the actual playbook need to be saved

* Thats all, we need to run the build nad this would go ahead  execute playbook and have nginx deployed on the managed node.