pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"
        ECR_REPO = "988698481528.dkr.ecr.us-east-1.amazonaws.com/my-app"
        EC2_IP = "52.201.87.198"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-app .'
            }
        }

        stage('Tag Image') {
            steps {
                sh 'docker tag my-app:latest $ECR_REPO:latest'
            }
        }

        stage('Login to ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    sh '''
                    aws ecr get-login-password --region $AWS_REGION | \
                    docker login --username AWS --password-stdin 988698481528.dkr.ecr.us-east-1.amazonaws.com
                    '''
                }
            }
        }

        stage('Push to ECR') {
            steps {
                sh 'docker push $ECR_REPO:latest'
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh '''
ssh -o StrictHostKeyChecking=no ubuntu@$EC2_IP <<EOF
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 988698481528.dkr.ecr.us-east-1.amazonaws.com

docker pull 988698481528.dkr.ecr.us-east-1.amazonaws.com/my-app:latest

docker stop my-app || true
docker rm my-app || true

docker run -d -p 80:8081 --name my-app 988698481528.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
EOF
                    '''
                }
            }
        }
    }
}
