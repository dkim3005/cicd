node{
    withCredentials([usernamePassword(credentialsId: 'blahblah', passwordVariable: 'password', usernameVariable: 'userName')]) {
    // some block
        def remote = [:]
        remote.name = 'type hostname in terminal'
        remote.host = 'xx.xx.xxx.xxx'//PC ip that u want to ssh
        remote.user = userName //username for username@ip
        remote.password = password //passward after typing username@ip
        remote.allowAnyHosts = true
        remote.agentForwarding = true
    
        sshCommand remote: remote, command: "pwd"
    }
}
