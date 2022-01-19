properties([
  parameters([
    gitParameter(
        branch: '',
        branchFilter: 'origin/(.*)',
        defaultValue: 'origin/main',
        description: '',
        name: 'GIT_BRANCH',
        quickFilterEnabled: true,
        listSize: 1,
        selectedValue: 'DEFAULT',
        sortMode: 'NONE',
        tagFilter: '*',
        useRepository: 'git@github.com:DarkflameUniverse/NexusDashboard.git',
        type: 'PT_BRANCH'
    )
  ])
])

node('worker'){
    currentBuild.setDescription(params.GIT_BRANCH)

    stage('Clone Code'){
        checkout([
            $class: 'GitSCM',
            branches: [[name: params.GIT_BRANCH]],
            extensions: [],
            userRemoteConfigs: [
                [
                    credentialsId: 'aronwk',
                    url: 'git@github.com:DarkflameUniverse/NexusDashboard.git'
                ]
            ]
        ])
    }
    def tag = ''
    stage('Build Container'){
        if (params.GIT_BRANCH.contains('main')){
            tag = 'latest'
        } else {
            tag = params.GIT_BRANCH.replace('\\', '-')
        }
        sh "docker build -t aronwk/nexus-dashboard:$tag ."
    }
    stage('Push Container'){
        withCredentials([usernamePassword(credentialsId: 'docker-hub-token', passwordVariable: 'password', usernameVariable: 'username')]) {
            sh "docker login -u $username -p $password"
            sh "docker push aronwk/nexus-dashboard:$tag"
            sh "docker logout"
        }
    }
}
