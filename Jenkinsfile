pipeline {
    agent any
    environment {
        SERVER_IP = '3.83.116.76'
    }
    stages {
        stage('Build') {
            steps{
                echo 'Building app......'
            }
        }
        stage('Deploy') {
            steps{
                echo 'Deploying app......'
                withCredentials([usernamePassword(credentialsId: 'deploy_cred', usernameVariable: 'USER', passwordVariable: 'PASSWD')]){
                    sh '''
                    pwd
                    ls -ltr
                    sshpass -p "$PASSWD" scp -pr "$(pwd)" ${USER}@${SERVER_IP}:/home/${USER}
                    sshpass -p "$PASSWD" ssh -tt ${USER}@${SERVER_IP}<<EOF
                    ls -ltr
                    cd nifty50
                    ls -ltr
                    exit
                    EOF
                '''
                }
            }
        }
        stage('Test') {
            steps{
                echo 'Testing app.......'
            }
        }
    }
}