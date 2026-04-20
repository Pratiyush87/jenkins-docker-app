pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REPO = '988698481528.dkr.ecr.ap-south-1.amazonaws.com/my-app'
        IMAGE_TAG = 'latest'
        EC2_IP = '52.201.87.198'
    }

    stages {

        stage('Clone Code') {
            steps {
                git credentialsId: 'github-creds', url: 'https://github.com/your-username/your-repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-app .'
            }
        }

        stage('Tag Image') {
            steps {
                sh 'docker tag my-app:latest $ECR_REPO:$IMAGE_TAG'
            }
        }

        stage('Login to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                    sh '''
                    aws ecr get-login-password --region $AWS_REGION | \
                    docker login --username AWS --password-stdin $ECR_REPO
                    '''
                }
            }
        }

        stage('Push to ECR') {
            steps {
                sh 'docker push $ECR_REPO:$IMAGE_TAG'
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@$EC2_IP << EOF
                    docker pull $ECR_REPO:$IMAGE_TAG
                    docker stop my-app || true
                    docker rm my-app || true
                    docker run -d -p 80:80 --name my-app $ECR_REPO:$IMAGE_TAG
                    EOF
                    '''
                }
            }
        }
    }
}
