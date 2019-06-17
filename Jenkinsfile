#!/usr/bin/groovy
// GitSCM and Attributes

// GIT attributes, which are defined in GitSCM plugin, but can't get
gGIT_BRANCH_NAME = 'none'
gGIT_COMMIT = 'none'

pipeline {
  // parameter directive , to use a parameter with params.<arg-name> or ${params.<arg-name>}
  parameters {
    // string parameter
    string(name: 'BRANCH', defaultValue: 'master', description: 'Which branch to build')
  }

  // define environment variables, to use a env var with env.<arg-name> or ${env.<arg-name>} 
  environment {
    // credential ID created in Credential Store 
    CREDENTIALSID = 'serviceacctsonos'
    REPOURL = 'https://github.com/Sonos-Inc/sonos-token-requester'
  }

  // setup build agent with given Team Jenkins build agent type - BUILD_AGENT
  agent {label 'python'}
  stages {
    // stage - check out source code
    stage ('Checkout Source') {
      steps {
        // catch github credential to allow build script to refer other GitHub repos
        sh "git config --global credential.helper 'cache --timeout=3600'"
        // check out source code with default branch and credential defined in the directive environment
        checkout([$class: 'GitSCM', branches: [[name: "refs/heads/${params.BRANCH}" ]], doGenerateSubmoduleConfigurations: false, 
                extensions: [[$class: 'LocalBranch', localBranch: "**"]], 
                submoduleCfg: [], 
                userRemoteConfigs: [[credentialsId: env.CREDENTIALSID, url: env.REPOURL]]])       
        // need to be script block
        script {
          gGIT_BRANCH_NAME = sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()
          gGIT_COMMIT  = sh(returnStdout: true, script: 'git rev-parse HEAD')
        }
      } 
    }

    stage ('Build Project') {
      steps {
        sh 'python --version'
        build job: 'brandt-no-op-test-code'
      }
    }

    stage ('Deactivate Virtualenv') {
      steps {
        sh 'deactivate'
      }
    }

    // dump out GIT attributes 
    stage ('GIT Attributes') {
      steps {
        echo "GIT_BRANCH_NAME=${gGIT_BRANCH_NAME}"
        echo "GIT_COMMIT=${gGIT_COMMIT}"
      }
    }
  } // end stages
}
