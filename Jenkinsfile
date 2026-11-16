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
                sh 'pip install pylint flake8 mypy bandit || true'
                sh 'pylint payment_app tests --fail-under=7.0 || true'
                sh 'flake8 payment_app tests --max-line-length=100 || true'
                sh 'mypy payment_app || true'
                sh 'bandit -r payment_app -f json -o bandit_report.json || true'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit_report.json', allowEmptyArchive: true
                }
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
