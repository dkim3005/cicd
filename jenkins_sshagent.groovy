node{

    def mailRecipients =
    '''
    aaabbb@ddc.com
    //add another
   
    '''


    sshagent(['jenkins-docker']) {
        String numOfPendingContainer = sh (
                script: '''
            echo $(ssh vmadmin@xx.xxx.xxx.xxx "kubectl get pods -n jenkins | grep Pending | awk -F ' ' {'print\\$5'} | awk -F 's' {'if(\\$1>100)print\\$1'} | wc -l")
            '''
                ,returnStdout: true
        ).trim()
        println "[INFO] Schedule Pending Container : ${numOfPendingContainer}"


        if (numOfPendingContainer.toInteger() > 10){
            mail to: mailRecipients,
                    subject: '[Jenkins] K8s Pending Container Warning',
                    body: '''
            Warning ! Please monitor k8s Scheduler !\n
            - Number of pending container (over 100sec) : ''' + numOfPendingContainer +
                            '''
            - IP : xx.xxx.xxx.xxx
            - Node Info : {nodename here} (master node)
            '''
            println "[INFO] E-mail sent!"
        }else {
            println "[INFO] E-mail not sent."
        }
    }
}
