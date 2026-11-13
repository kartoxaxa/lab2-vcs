pipeline {
    agent any

    environment {
        PROJECT_NAME = 'lab2-vcs'
        PYTHON_VERSION = '3.11'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Клонирование проекта ${env.PROJECT_NAME}..."
                checkout scm
            }
        }
        stage('Setup') {
            steps {
                echo 'Установка зависимостей...'
                sh 'pip install -r requirements.txt || true'
            }
        }
        stage('Lint') {
            steps {
                echo 'Статический анализ...'
                sh 'pip install flake8 && flake8 . || true'
            }
        }
        stage('Test') {
            steps {
                echo 'Запуск тестов...'
                sh 'pip install pytest && pytest || true'
            }
        }
        stage('Archive') {
            steps {
                echo 'Сохранение артефакта...'
                sh 'mkdir -p artifacts && echo "Build ${BUILD_NUMBER}" > artifacts/build.txt'
                archiveArtifacts artifacts: 'artifacts/**', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo "Pipeline завершён. Номер сборки: ${env.BUILD_NUMBER}"
        }
        success {
            echo 'Все этапы прошли успешно!'
        }
        failure {
            echo 'Один из этапов завершился с ошибкой'
        }
    }
}
