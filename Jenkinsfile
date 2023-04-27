pipeline {
    agent none 
    environment {
        docker_registry = 'mikec1233/spotter'
        docker_user =  'mikec1233'
    }
    stages {
        stage('Publish') {
            agent {
                kubernetes {
                    inheritFrom 'worker'
                }
            }
            steps{
                container('docker') {
                    sh 'echo $DOCKER_TOKEN | docker login --username $DOCKER_USER --password-stdin'
                    sh 'docker build -t $DOCKER_REGISTRY:worker-$BUILD_NUMBER ./worker'
                    sh 'docker push $DOCKER_REGISTRY:worker-$BUILD_NUMBER'
                }
            }
        }
        stage ('Deploy') {
            agent {
                node {
                    label 'deploy'
                }
            }
            steps {
                sshagent(credentials: ['cloudlab']) {
                    sh "sed -i 's/DOCKER_USER/${DOCKER_USER}/g' worker.yaml"
                    sh "sed -i 's/BUILD_NUMBER/${BUILD_NUMBER}/g' worker.yaml"
                    sh 'scp -r -v -o StrictHostKeyChecking=no *.yaml patodo@pcvm767-1.emulab.net:~/'
                    sh 'ssh -o StrictHostKeyChecking=no patodo@pcvm767-1.emulab.net kubectl apply -f /users/patodo/worker.yaml -n centigro'
                    sh 'ssh -o StrictHostKeyChecking=no patodo@pcvm767-1.emulab.net kubectl apply -f /users/patodo/worker-service.yaml -n centigro'                    
                }
            }
        }
    }
}
