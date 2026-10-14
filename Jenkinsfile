pipeline {
  agent any
  options { disableConcurrentBuilds() }
  environment {
    AWS_REGION   = 'ap-northeast-1'
    AWS_PAGER    = ''
    ACCOUNT_ID   = '633212682575'
    REGISTRY     = "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    REPO         = 'shoplite-api'
    CLUSTER      = 'shoplite-prod'
    AWS_CREDS    = credentials('aws-jenkins-ci')   // ID khai báo trong Jenkins
    AWS_ACCESS_KEY_ID     = "${AWS_CREDS_USR}"
    AWS_SECRET_ACCESS_KEY = "${AWS_CREDS_PSW}"
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
        script { env.SHA = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim() }
      }
    }
    stage('Test') {
      steps {
        sh '''
          docker run --rm -v "$PWD":/w -w /w python:3.12-slim \
            sh -c "pip install -q -r app/requirements.txt pytest && pytest -q tests"
        '''
      }
    }
    stage('Build') {
      steps { sh 'docker build --pull -t $REGISTRY/$REPO:$SHA .' }
    }
    stage('Push to ECR') {
      steps {
        sh '''
          aws ecr get-login-password --region $AWS_REGION | \
            docker login --username AWS --password-stdin $REGISTRY
          docker push $REGISTRY/$REPO:$SHA
        '''
      }
    }
    stage('Approve') {
      when { branch 'main' }
      steps { input message: "Deploy ${env.SHA} lên EKS prod?", ok: 'Deploy' }
    }
    stage('Deploy EKS') {
      when { branch 'main' }
      steps {
        sh '''
          aws eks update-kubeconfig --name $CLUSTER --region $AWS_REGION
          kubectl -n shoplite set image deploy/api api=$REGISTRY/$REPO:$SHA
          kubectl -n shoplite rollout status deploy/api --timeout=180s
        '''
      }
    }
  }
  post { always { sh 'docker image prune -f || true' } }
}
